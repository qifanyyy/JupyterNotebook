from taskflow import TimeoutException
from taskflow.symbolic import ForkResource
import copy
from inspect import signature
from urllib.parse import quote_plus
from pymongo import MongoClient
import os
import logging
from multiprocessing import Process
import sys
import io


import taskflow.config as cfg


__config__ = None

__db__ = None
__client__ = {}

logger = logging.getLogger("mq_handler")


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
    config = get_config()

    if len(config) == 0:
        return None

    if 'execution' not in config:
        return None

    auth = config['execution']
    mongodb = auth["mongodb"]
    return setup_client(mongodb["url"], mongodb["auth"])


def get_db():
    global __db__
    if __db__ is None:
        __db__ = start_mongo()

    config = get_config()
    if 'execution' not in config:
        return None

    return __db__[__config__['execution']['mongodb']['database']]


def get_config():
    global __config__

    if __config__ is None:
        __config__ = cfg.load_config(failing_default={})

    return __config__


def get_environ(config, key):

    if 'environment' in config:
        config = config['environment']
        if key in config:
            return config[key]

    if key in os.environ:
        return os.environ[key]

    return None


def execute_function(function, kwargs, backend_setting):
    if function == '__fork__':
        return execute_fork(kwargs, backend_setting)

    if function == '__merge__':
        return execute_merge(kwargs, backend_setting)

    return _single_execution(function, kwargs, backend_setting)


def execute_fork(kwargs, backend_setting):
    return ForkResource(kwargs['__fork__'])


def _handle_merge(merge_element, flatten):

    merge = []
    next_flatten = []
    if isinstance(merge_element, ForkResource):

        for o in merge_element.obj_:
            element, next_fl = _handle_merge(
                o, flatten
            )
            merge.append(
                element
            )
            next_flatten.append(next_fl)

    else:
        return merge_element, False

    if flatten:
        out = []
        for i, r in enumerate(merge):
            if next_flatten[i]:
                out.extend(r)
            else:
                out.append(r)
        merge = out

    return merge, True


def execute_merge(kwargs, backend_setting):
    res = []
    for k in kwargs:
        if k.startswith('__merge__'):
            res.append(_handle_merge(kwargs[k], backend_setting['flatten'])[0])
    if backend_setting['flatten']:
        out = []
        for r in res:
            try:
                out.extend(r)
            except TypeError:
                out.append(r)
        res = out
    return res


def _inject_env(function, kwargs, environment):

    if 'env' in kwargs:
        return

    sig = signature(function)

    if 'env' in sig.parameters:
        kwargs['env'] = environment


class FunctionEnvironment(object):

    def __init__(self, setting):
        self._config = get_config()
        self._setting = setting

    def is_remote_io_loaded(self):
        return get_db() is not None

    def get_db(self):
        return get_db()

    def get_cache_dir(self):
        return get_environ(self._config, "LOCAL_CACHE_PATH")

    def get_host_cache_dir(self):
        return get_environ(self._config, "HOST_CACHE_PATH")

    def get_logger(self):
        return logger

    def get_environ(self, key):
        if key in self._setting:
            return self._setting[key]
        return None

    def log(self, text):
        if '__logger__' in self._setting:
            self._setting['__logger__'](text)
        logger.info(text)


class LogIO(io.StringIO):

    def __init__(self, logger, orig):
        self._logger = logger
        self.orig_ = orig
        super().__init__()

    def write(self, s):
        sys.stdout = self.orig_
        try:
            line = s.rstrip()
            if len(line) == 0:
                return
            self._logger(line)
        finally:
            sys.stdout = self
        super().write(s)


def _execute_capsuled_function(function, kwargs, backend_setting, result):

    # Bind stdout
    if '__logger__' in backend_setting:
        sys.stdout = LogIO(backend_setting['__logger__'], sys.stdout)
        sys.stderr = LogIO(backend_setting['__logger__'], sys.stdout)

    try:
        result.append(
            function(**kwargs)
        )
    finally:
        if '__logger__' in backend_setting:
            sys.stdout = sys.stdout.orig_
            sys.stderr = sys.stderr.orig_


def _execute_timeout_function(function, kwargs, backend_setting, timeout):
    logger.debug("Execute function with timeout %i. Spawn independent process.")

    result = []

    p = Process(target=_execute_capsuled_function,
                args=(function, kwargs, backend_setting, result))
    p.start()

    p.join(timeout)

    if p.is_alive():
        result = None
        p.terminate()
        p.join()

    if result is None:
        raise TimeoutException("Had to kill execution as timeout of %i was exceeded. " % timeout)

    if len(result) > 0:
        return result[0]


def _single_execution(function, kwargs, backend_setting):
    # Prepare function
    _inject_env(function, kwargs, FunctionEnvironment(backend_setting))

    if 'timeout' in backend_setting:
        return _execute_timeout_function(
            function,
            kwargs,
            backend_setting,
            backend_setting['timeout']
        )

    result = []
    _execute_capsuled_function(function, kwargs, backend_setting, result)

    if len(result) > 0:
        return result[0]
