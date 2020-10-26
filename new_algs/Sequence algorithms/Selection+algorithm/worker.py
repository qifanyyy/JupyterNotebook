import logging
import json
import traceback
from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from pymongo import InsertOne, ReplaceOne, DeleteOne, UpdateOne
from datetime import datetime
import copy
import uuid
import pika
import time
import importlib

from threading import Thread

import taskflow.rabbitmq_handling as rabbitmq_handling
from taskflow.backend import ForkResource
import taskflow.distributed_io as dio
import taskflow.execution_handler as ex
import taskflow.config as cfg

FORMAT = '%(asctime)s %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO,
                    datefmt='%m/%d/%Y %I:%M:%S %p')
logger = logging.getLogger("worker")

__db__ = None
__client__ = {}

__config__ = {}

__config__ = cfg.load_config()

__flushes__ = []

_process_ = None


class DelayedUpdate(object):

    def __init__(self, coll, threshold=20):
        self._coll = coll
        self._updates = []
        self._threshold = threshold

    def update(self, obj):
        self._updates.append(obj)

        if len(self._updates) > self._threshold:
            self.flush()

    def flush(self):
        c = self._updates
        self._updates = []

        if len(c) > 0:
            self._coll.bulk_write(c)


def setup_client(url, auth=None):
    global __client__
    if url not in __client__:
        if auth is not None:
            uri = 'mongodb://%s:%s@%s/%s' % (
                quote_plus(auth['username']),
                quote_plus(auth['password']),
                url,
                auth['authSource']
            )
        else:
            uri = 'mongodb://%s/' % url

        __client__[url] = MongoClient(uri)
    return __client__[url]


def start_mongo():
    global __config__

    auth = __config__['backend']
    mongodb = auth["mongodb"]
    return setup_client(mongodb["url"], mongodb["auth"])


def get_db():
    global __db__
    global __config__
    if __db__ is None:
        __db__ = start_mongo()

    return __db__[__config__['backend']['mongodb']['database']]


def _ack(channel, delivery_tag, cb, result):
    def call():
        try:
            cb(result)
        except Exception:
            traceback.print_exc()
        finally:
            if channel.is_open:
                channel.basic_ack(delivery_tag)
            else:
                pass
            global _process_
            _process_ = None
    return call


def _long_run(connection, channel, delivery_tag, task, callback):

    try:
        res = task()
    except Exception:
        res = 'exception:\n'+traceback.format_exc()

    rabbitmq_handling.close_thread()

    connection.add_callback_threadsafe(_ack(channel,
                                            delivery_tag,
                                            callback, res))


class MessageHandler(object):

    def __init__(self, channel, delivery_tag):
        self._channel = channel
        self._delivery_tag = delivery_tag
        self._ack = True

    def long_run(self, task, callback):
        global _process_

        if _process_ is not None:
            raise ValueError("Only one process can run at time!")

        _process_ = Thread(
            target=_long_run,
            args=(
                rabbitmq_handling.get_connection(),
                self._channel,
                self._delivery_tag,
                task, callback
            )
        )

        _process_.start()
        self._ack = False

    def ack(self):
        if self._ack:
            self._channel.basic_ack(
                delivery_tag=self._delivery_tag
            )


def consume_task(ch, method, properties, body):
    logger.debug("Retrieve task")

    if properties.content_type != 'application/json':
        logger.error("Reject task as non-json task are not parseable. [%s]" % body)
        ch.basic_reject(delivery_tag=method.delivery_tag)
        return

    obj = json.loads(body)

    if 'type' not in obj:
        logger.error("Cannot handle a task without type [%s]" % body)
        ch.basic_reject(delivery_tag=method.delivery_tag)
        return

    mh = MessageHandler(ch, method.delivery_tag)

    try:
        _execute_task(mh, obj)
    except UnknownTaskException:
        traceback.print_exc()
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    except Exception:
        traceback.print_exc()
        ch.basic_nack(delivery_tag=method.delivery_tag)
        return

    mh.ack()


def log(message):

    if not isinstance(message, dict):
        message = {
            'message': message
        }

    message['time'] = str(datetime.now())

    rabbitmq_handling.log_event("worker", message)


def db_log(delayed, func_id, msg):
    delayed.update(InsertOne({
        'function_id': func_id,
        'message': msg,
        'time_stamp': time.time(),
        'time': str(datetime.now())
    }))


def build_remote_log(db, func_id):

    global __flushes__

    delayed = DelayedUpdate(db.logs)
    __flushes__.append(delayed)

    def remote_log(text):
        print(text)
        log({
            'function_id': func_id,
            'message': text
        })
        db_log(delayed, func_id, text)

    return remote_log


class UnknownTaskException(Exception):
    pass


def _execute_task(mh, task):
    switch = {
        'open_session': open_session,
        'start_job': start_job,
        'sub_fork': sub_fork,
        'run_fork': run_fork,
        'join_forks': join_forks,
        'close_job': close_job,
        'close_session': close_session
    }

    if task['type'] not in switch:
        raise UnknownTaskException(str(task['type'])+' is not implemented.')

    switch[task['type']](mh, task)


# Utils
def get_ingoing(job):

    for i, in_ref in enumerate(job['ingoing']):
        yield in_ref, job['destinations'][i]


def is_finished(graph, job_id):

    job = graph.find_one({'_id': job_id,
                          'result': {'$exists': False},
                          'error': {'$exists': False}}, ['_id'])
    return job is None


def load_results(db, graph, job_id):
    job = graph.find_one({'_id': job_id})

    if 'error' in job:
        if 'optional' in job:
            return None
        return "__ERROR__"

    return dio.load(db, job['result'], partial=True)


def _preprocess_args(kwargs):
    args = {}

    for k, v in kwargs.items():
        if '::list_' in k:
            name, pos = k.rsplit('::list_', 1)
            if name not in args:
                args[name] = []
            arg_list = args[name]
            pos = int(pos)
            while len(arg_list) <= pos:
                arg_list.append([])
            arg_list[pos] = v
        elif '::dict_' in k:
            name, pos = k.rsplit('::dict_', 1)
            if name not in args:
                args[name] = {}
            args[name][pos] = v
        else:
            args[k] = v

    return args


def _build_forks(kwargs):
    resource = None
    for k, variable in kwargs.items():
        if isinstance(variable, ForkResource):
            resource = variable

    if resource:
        keys = set([])
        for k, variable in kwargs.items():
            if isinstance(variable, ForkResource) and\
                    variable.src_ == resource.src_:
                keys.add(k)

        src = resource.src_
        resource = resource.obj_
        if not isinstance(resource, list):
            resource = [resource]

        results = []
        for i in range(len(resource)):
            bind_kwargs = copy.copy(kwargs)
            for k in keys:
                bind_kwargs[k] = kwargs[k].obj_[i]
            results.append(
                bind_kwargs
            )
        return results, src

    return kwargs, None


class UnknownFunctionException(Exception):
    pass


class VarNotBoundException(Exception):
    pass


def _load_func(name):

    parts = name.rsplit(".", 1)
    module = parts[0]

    module = importlib.import_module(module)

    func = getattr(module, parts[1])
    if hasattr(func, '_function'):
        func = getattr(func, '_function')

    return func


def _execute_funcs(run_id, calls, kwargs, bindings):
    db = get_db()
    functions = db.functions

    bind = kwargs

    for i, call in enumerate(calls):
        function = functions.find_one({'_id': call})

        func_ref = _load_func(function['function_name'])

        if function is None:
            raise UnknownFunctionException(
                "Function [id = %s] is unknown." % call
            )

        bind.update(
                _preprocess_args(function['environment'])
                )

        for dep in function['dependency_vars']:
            if dep not in bind:
                raise VarNotBoundException(
                    "Function %s require parameter %s" % (
                        function['function_name'], dep
                    )
                )

        setting = function['backend_setting']

        setting['__logger__'] = build_remote_log(db, run_id)
        setting['__logger__']('START')

        result = ex.execute_function(
            func_ref, bind, setting
        )

        bind = {}

        for B in bindings[i]:
            bind[B] = result

    return bind['__out__']


def _build_and_call(run_id, db, run, kwargs):
    graph = db.function_graph

    job = graph.find_one({'_id': run['job_id']})

    return _execute_funcs(run_id, job['calls'], kwargs, job['bindings'])


# Step 1
def open_session(mh, task):
    session_id = task['session']

    # Open db connection
    db = get_db()
    graph = db.function_graph

    # Find unprocessed jobs
    change = False
    for job in graph.find({'session_id': session_id,
                           'result': {'$exists': False},
                           'error': {'$exists': False},
                           'run_id': {'$exists': False}},
                          ['_id']):
        rabbitmq_handling.start_job_request(
            session_id, job['_id']
        )
        change = True

    if change:
        logger.info("Open session %s" % session_id)

        log({
            'task': 'session',
            'session_id': session_id,
            'state': 'open'
        })

        rabbitmq_handling.close_session(session_id)


# Step 2
def start_job(mh, task):
    session_id = task['session']
    job_id = task['job_id']


    # Open db connection
    db = get_db()
    graph = db.function_graph
    runs = db.function_runs

    # Check if not already started
    job = graph.find_one({'_id': job_id})

    logger.info("Job %s." % job_id)

    if job is None:
        logger.warn("Unknown job %s." % job_id)
        return

    if 'run_id' in job or 'lock' in job:
        logger.info("Reject job %s. It is running" % job_id)
        return

    log({
        'task': 'job_execution',
        'session_id': session_id,
        'job_id': job_id,
        'state': 'started'
    })

    # Set a lock on document
    graph.update_one({'_id': job_id}, {'$set': {'lock': True}})

    try:

        binding = {}

        for pre_id, dests in get_ingoing(job):
            if not is_finished(graph, pre_id):
                rabbitmq_handling.start_job_request(
                    session_id, pre_id
                )
                return
            pre_load = load_results(db, graph, pre_id)
            if pre_load == '__ERROR__':
                logger.error("Cannot run %s because %s has an error" % (job_id, pre_id))
                return
            for d in dests:
                binding[d] = pre_load

        logger.info("Successfully load previous result [id = %s]" % job_id)

        log({
            'task': 'job_execution',
            'session_id': session_id,
            'job_id': job_id,
            'state': 'precondition_satisfied'
        })

        # Merge forks if necessary
        if 'merge' in job:
            merge_result = ex.execute_function(
                '__merge__', binding, {'flatten': 'flatten' in job}
            )
            binding = {}
            for m in job['merge']:
                binding[m] = merge_result

        binding = _preprocess_args(binding)

        # Store bind
        for k in list(binding.keys()):
            binding[k] = dio.store(db, binding[k])

        # Fork tasks
        fork_id = str(uuid.uuid4())
        run_id = str(uuid.uuid4())

        entry = {
            '_id': run_id,
            'fork_id': fork_id,
            'job_id': job_id,
            'binding': binding
        }

        runs.insert_one(entry)
        graph.update_one({'_id': job_id}, {'$set': {'run_id': run_id}})

        logger.info("Request fork for %s." % run_id)
        rabbitmq_handling.start_fork_request(session_id, run_id)

        log({
            'task': 'job_execution',
            'session_id': session_id,
            'job_id': job_id,
            'state': 'request_fork'
        })

    finally:
        # Unlock
        graph.update_one({'_id': job_id}, {'$unset': {'lock': True}})


def sub_fork(mh, task):
    session_id = task['session']
    _id = task['fork_id']

    # Setup db
    db = get_db()
    runs = db.function_runs

    run = runs.find_one({'_id': _id})

    logger.info("Fork %s." % _id)

    if run is None:
        logger.warn("Unknown task %s." % _id)
        return

    if 'result' in run or 'error' in run or 'lock' in run:
        logger.info("Reject fork %s. Either it is running or finished." % _id)
        return

    log({
        'task': 'fork_execution',
        'session_id': session_id,
        'job_id': run['job_id'],
        'fork_id': _id,
        'state': 'started'
    })

    # Set a lock on document
    runs.update_one({'_id': _id}, {'$set': {'lock': True}})

    try:
        binding = run['binding']

        # Load bindings
        for k in list(binding.keys()):
            binding[k] = dio.load(db, binding[k], partial=True)

        forks, sub_id = _build_forks(binding)

        if sub_id is None:
            logger.info("Request execution for %s." % _id)
            rabbitmq_handling.start_run_request(
                session_id, _id
            )
            return

        logger.info("Has to fork %s." % _id)

        runs.update({'_id': _id}, {'$set': {'sub_id': sub_id}})

        run_ids = []
        updates = []

        for bind in forks:

            run_id = str(uuid.uuid4())

            # Store bind
            for k in list(bind.keys()):
                bind[k] = dio.store(db, bind[k])

            entry = {
                '_id': run_id,
                'fork_id': run['fork_id'],
                'job_id': run['job_id'],
                'parent_fork_id': _id,
                'binding': bind
            }

            updates.append(
                InsertOne(entry)
            )
            run_ids.append(run_id)

        runs.bulk_write(updates)

        log({
            'task': 'fork_execution',
            'session_id': session_id,
            'job_id': run['job_id'],
            'fork_id': _id,
            'state': 'sub_fork'
        })

        for run_id in run_ids:
            logger.info("Request fork for %s" % run_id)
            rabbitmq_handling.start_fork_request(
                session_id, run_id
            )

    finally:
        # Unlock
        runs.update_one({'_id': _id}, {'$unset': {'lock': True}})


def run_fork_wrap(session_id, _id, db, run, kwargs):

    def _run():
        return _build_and_call(_id, db, run, kwargs)

    def callback(result):
        runs = db.function_runs
        if isinstance(result, str) and result.startswith("exception:"):
            logger.error('Error in %s: %s' % (_id, result))
            runs.update_one({'_id': _id}, {'$set': {'error': result}})

            log({
                'task': 'fork_execution',
                'session_id': session_id,
                'job_id': run['job_id'],
                'fork_id': _id,
                'state': 'error'
            })
        else:
            result_ref = dio.store(db, result)
            runs.update_one({'_id': _id}, {'$set': {'result': result_ref}})
            logger.info("Successfull finished: %s" % _id)

            log({
                'task': 'fork_execution',
                'session_id': session_id,
                'job_id': run['job_id'],
                'fork_id': _id,
                'state': 'success'
            })
        global __flushes__

        for fl in __flushes__:
            fl.flush()
        __flushes__ = []

        logger.info("Finished fork %s." % _id)
        runs.update_one({'_id': _id}, {'$unset': {'lock': True}})
        rabbitmq_handling.start_join_request(
            session_id, run['job_id'], _id
        )
    return _run, callback


def run_fork(mh, task):
    session_id = task['session']
    _id = task['fork_id']

    # Open db
    db = get_db()
    runs = db.function_runs

    run = runs.find_one({'_id': _id})

    logger.info("Execute %s." % _id)

    if run is None:
        logger.warn("Unknown task %s." % _id)
        return

    if 'result' in run or 'error' in run or 'lock' in run or 'sub_id' in run:
        logger.info("Reject fork %s. Either it is running or finished." % _id)
        return

    log({
        'task': 'fork_execution',
        'session_id': session_id,
        'job_id': run['job_id'],
        'fork_id': _id,
        'state': 'start_run'
    })

    # Set a lock on document
    runs.update_one({'_id': _id}, {'$set': {'lock': True}})

    # Load bindings
    kwargs = run['binding']

    for k in list(kwargs.keys()):
        logger.debug("Load resoruce %s" % kwargs[k])
        kwargs[k] = dio.load(db, kwargs[k])

    logger.info("Finished loading input [id = %s]" % _id)

    task, cb = run_fork_wrap(
        session_id, _id, db, run, kwargs
    )

    mh.long_run(
        task, cb
    )


def join_forks(mh, task):

    session = task['session']
    _id = task['run_id']
    job_id = task['job_id']

    # Open db connection
    db = get_db()
    runs = db.function_runs
    graph = db.function_graph

    # Load fork
    run = runs.find_one({'_id': _id})

    logger.info("Join %s." % _id)

    if run is None:
        logger.warn("Unknown task %s." % _id)
        return

    if 'error' not in run and 'result' not in run:
        logger.info("Reject for fork %s. It is not finished." % _id)
        return

    if 'parent_fork_id' in run:

        parent = run['parent_fork_id']

        # Check if there are jobs to finish
        req = runs.find_one({'parent_fork_id': parent,
                            'result': {'$exists': False},
                             'error': {'$exists': False}})

        if req is not None:
            logger.debug("Parent %s is not finished." % parent)
            return

        # Join task
        logger.info("Start joining task %s" % parent)

        req = runs.find({'parent_fork_id': parent,
                        'error': {'$exists': True}}, ['_id'])
        if req.count() > 0:
            runs.update_one({'_id': parent}, {'$set': {'error': req.count()}})
            logger.info("Failed job as one of its components failed [job_id = %s]" % job_id)
            rabbitmq_handling.start_join_request(
                session, job_id, parent
            )
            return

        sub_id = runs.find_one({'_id': parent}, ['sub_id'])['sub_id']
        req = runs.find({'parent_fork_id': parent,
                        'result': {'$exists': True}}, ['result'])

        results = [dio.Reference(db, r['result']) for r in req]

        if len(results) == 1:
            results = results[0]
        else:
            results = ForkResource(results, src=sub_id)

        result_ref = dio.store(db, results)

        runs.update_one({'_id': parent}, {'$set': {'result': result_ref}})
        rabbitmq_handling.start_join_request(
            session, job_id, parent
        )

        log({
            'task': 'fork_execution',
            'session_id': session,
            'job_id': job_id,
            'fork_id': _id,
            'state': 'finished'
        })
        return

    # Top level run
    setOp = {}
    if 'error' in run:
        setOp['error'] = run['error']

    if 'result' in run:
        result = run['result']

        job = graph.find_one({'_id': run['job_id']})

        if 'fork' in job:
            result = ForkResource(dio.Reference(db, result))
            result = dio.store(db, result)

        setOp['result'] = result

    if len(setOp) > 0:
        graph.update_one({'_id': run['job_id']}, {'$set': setOp})
        rabbitmq_handling.close_job_request(
            session, run['job_id']
        )
        log({
            'task': 'fork_execution',
            'session_id': session,
            'job_id': job_id,
            'fork_id': _id,
            'state': 'finished'
        })


def close_job(mh, task):
    session = task['session']
    job_id = task['job_id']

    # Open db
    db = get_db()
    graph = db.function_graph

    job = graph.find_one({'_id': job_id})

    logger.info("Close job %s." % job_id)

    if job is None:
        logger.warn("Unknown job %s" % job_id)
        return

    if 'result' not in job:
        logger.debug("Job %s is not finished" % job_id)
        return

    log({
        'task': 'job_execution',
        'session_id': session,
        'job_id': job_id,
        'state': 'finished'
    })

    if len(job['outgoing']) == 0:
        rabbitmq_handling.close_session(session)
    else:
        for out in job['outgoing']:
            rabbitmq_handling.start_job_request(
                session, out
            )


def close_session(mh, task):
    session = task['session']

    # Open db
    db = get_db()
    graph = db.function_graph

    logger.info("Close session %s." % session)

    job = graph.find_one({'session_id': session,
                          'result': {'$exists': False},
                          'error': {'$exists': False}}, ['_id'])

    if job is not None:
        logger.info("Cannot close session %s. There are still open jobs." % session)
        return

    # TODO Handle session close
    logger.info("Successfully closed session: %s" % session)

    for callbacks in db.callbacks.find({'session_id': session}):
        rabbitmq_handling.reply_to_callback(
            session, callbacks['request_id'], callbacks['reply_to']
        )
    db.callbacks.delete_many({'session_id': session})

    log({
        'task': 'session',
        'session_id': session,
        'state': 'closed'
    })


def consume_request(ch, method, properties, body):
    logger.debug("Retrieve callback request")

    if properties.content_type != 'application/json':
        logger.error("Reject task as non-json task are not parseable. [%s]" % body)
        ch.basic_reject(delivery_tag=method.delivery_tag)
        return

    obj = json.loads(body)

    db = get_db()

    if db.requests.find_one({'_id': obj['request_id']}) is None:
        logger.info("Request %s does not exist." % obj['request_id'])
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(
                correlation_id=obj['request_id'],
                content_type="application/json"
            ),
            body="Request %s does not exist!" % obj['request_id'])
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return

    entry = {
        'request_id': obj['request_id'],
        'session_id': obj['session_id'],
        'reply_to': properties.reply_to
    }

    logger.info("Save request callback for %s" % obj['request_id'])
    try:
        get_db().callbacks.insert_one(entry)
        rabbitmq_handling.close_session(obj['session_id'])
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def start_worker():
    logger.info("Start Worker.")
    rabbitmq_handling.define_task_callback(consume_task)
    rabbitmq_handling.define_request_callback(consume_request)
    try:
        rabbitmq_handling.consume_loop()
    finally:
        rabbitmq_handling.close_connections()


if __name__ == '__main__':
    start_worker()
