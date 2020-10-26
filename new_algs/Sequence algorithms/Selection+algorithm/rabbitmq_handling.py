import pika
import logging
import json
import uuid
import threading

import taskflow.config as cfg

logger = logging.getLogger("mq_handler")

__config__ = {}
__connection__ = {}
__channel__ = {}
__task_setup__ = False
__request_setup__ = False
__closed__ = False
__log__ = False


__config__ = cfg.load_config()


def _setup_connection():
    global __config__
    global __connection__

    thread_id = threading.get_ident()

    if thread_id in __connection__:
        return __connection__[thread_id]
    rabbit = __config__['message-queue']
    rabbit = rabbit['rabbit-mq']

    server = rabbit['server']
    port = rabbit['port']
    user = rabbit['user']
    password = rabbit['password']

    parameter = pika.ConnectionParameters(
        host=server,
        port=port,
        virtual_host=rabbit['vHost'],
        credentials=pika.PlainCredentials(
            user, password
        )
    )

    __connection__[thread_id] = pika.BlockingConnection(parameter)

    return __connection__[thread_id]


def _reconnect():
    global __closed__
    global __connection__
    global __channel__

    __connection__ = {}
    __channel__ = {}

    if __closed__:
        raise ValueError("Connection is closed!")

    return _setup_channel()


def _setup_channel():
    global __channel__
    thread_id = threading.get_ident()

    if thread_id in __channel__:
        return __channel__[thread_id]

    connection = _setup_connection()
    __channel__[thread_id] = connection.channel()

    return __channel__[thread_id]


def _setup_task_queue():
    global __task_setup__

    if __task_setup__:
        return

    channel = _setup_channel()

    channel.basic_qos(prefetch_count=1)

    channel.queue_declare(
        queue='task_queue',
        durable=True
    )

    __task_setup__ = True


def _setup_request_queue():
    global __request_setup__

    if __request_setup__:
        return

    channel = _setup_channel()

    channel.queue_declare(
        queue='request_queue'
    )

    __request_setup__ = True


def _setup_log_exchange():
    global __log__

    if __log__:
        return

    channel = _setup_channel()

    channel.exchange_declare(
        'worker_logs',
        exchange_type='direct'
    )

    __log__ = True


def _send_task(session_id, task):
    _setup_task_queue()
    channel = _setup_channel()

    message = json.dumps(task)

    properties = pika.BasicProperties(app_id='%s/%s' % ('tasks', session_id),
                                      content_type='application/json',
                                      delivery_mode=2)

    channel.basic_publish(
        exchange='',
        routing_key='task_queue',
        body=message,
        properties=properties
    )
    logger.debug('Send: %s' % message)


def _savely_send(send_func, session_id, msg, tries=5):

    try:
        return send_func(session_id, msg)
    except pika.exception:
        if tries <= 0:
            logger.error('Failed to reconnect.')
            return None
        logger.info("Reconnect to Rabbit-MQ.")
        _reconnect()
        _savely_send(send_func, session_id, msg, tries - 1)


def get_connection():
    return _setup_connection()


def start_session_request(session_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'open_session',
            'session': session_id
        }
    )


def start_job_request(session_id, job_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'start_job',
            'session': session_id,
            'job_id': job_id
        }
    )


def start_fork_request(session_id, run_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'sub_fork',
            'session': session_id,
            'fork_id': run_id
        }
    )


def start_run_request(session_id, run_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'run_fork',
            'session': session_id,
            'fork_id': run_id
        }
    )


def start_join_request(session_id, job_id, run_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'join_forks',
            'session': session_id,
            'job_id': job_id,
            'run_id': run_id
        }
    )


def close_job_request(session_id, job_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'close_job',
            'session': session_id,
            'job_id': job_id
        }
    )


def close_session(session_id):
    _savely_send(
        _send_task, session_id, {
            'type': 'close_session',
            'session': session_id
        }
    )


class BlockingRequest:

    def __init__(self, connection, channel, session_id, request_id):

        self.connection = connection
        self.channel = channel
        self.session_id = session_id
        self.corr_id = request_id
        self.queue = channel.queue_declare(
            '', exclusive=True
        ).method.queue

        channel.basic_consume(
            queue=self.queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def block(self):
        self.response = None

        body = {
            'session_id': self.session_id,
            'request_id': self.corr_id
        }

        body = json.dumps(body)

        self.channel.basic_publish(
            exchange='',
            routing_key='request_queue',
            properties=pika.BasicProperties(
                reply_to=self.queue,
                correlation_id=self.corr_id,
                content_type="application/json"
            ),
            body=body)
        while self.response is None:
            self.connection.process_data_events()
        return self.response


def wait_for_request(session_id, request_id):
    _setup_request_queue()
    channel = _setup_channel()

    global __connection__

    request = BlockingRequest(__connection__,
                              channel, session_id,
                              request_id)
    return request.block().decode('utf-8')


def reply_to_callback(session_id, request_id, callback_q):
    _setup_channel().basic_publish(
        exchange='',
        routing_key=callback_q,
        properties=pika.BasicProperties(
            correlation_id=request_id
        ),
        body="SUCCESS"
    )


def log_event(level, event):
    _setup_log_exchange()
    channel = _setup_channel()

    message = json.dumps(event)

    properties = pika.BasicProperties(content_type='application/json')

    channel.basic_publish(
        exchange='worker_logs',
        routing_key=level,
        body=message,
        properties=properties
    )


def define_request_callback(callback):
    _setup_request_queue()
    channel = _setup_channel()

    channel.basic_consume(
        queue='request_queue',
        on_message_callback=callback,
        auto_ack=False
    )


def define_task_callback(callback):
    _setup_task_queue()
    channel = _setup_channel()

    channel.basic_consume(
        queue='task_queue',
        on_message_callback=callback,
        auto_ack=False
    )


def define_log_callback(callback):
    pass


def consume_loop():
    _setup_channel().start_consuming()


def close_thread():
    global __channel__
    global __connection__
    thread_id = threading.get_ident()

    if thread_id in __channel__:
        __channel__[thread_id].close()
        del __channel__[thread_id]

    if thread_id in __connection__:
        __connection__[thread_id].close()
        del __connection__[thread_id]


def close_connections():
    global __closed__
    __closed__ = True
    global __connection__

    for conn in __connection__.values():
        conn.close()
