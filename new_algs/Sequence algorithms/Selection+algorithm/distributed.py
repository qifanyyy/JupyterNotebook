from urllib.parse import quote_plus
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, BulkWriteError
from pymongo import InsertOne, ReplaceOne
import json
import datetime
import uuid
import logging

import inspect

import taskflow.rabbitmq_handling as rabbitmq_handling
from taskflow import SessionNotInitializedException, RemoteError
from taskflow.test import dummy_composite
from taskflow.symbolic import hash_str
from taskflow.backend import Session, ForkResource
import taskflow.distributed_io as dio
import taskflow.config as cfg

FORMAT = '%(asctime)s %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT,
                    datefmt='%m/%d/%Y %I:%M:%S %p')

logger = logging.getLogger("session_remote")

__db__ = None
__client__ = {}

__config__ = cfg.load_config()


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


def _func_name(o):
    return inspect.getmodule(o).__spec__.name + "." + o.__name__


def _serialize_func(db, session_id, name, attr):
    if name == 'STOP' or name == 'START':
        return None, None

    if name.startswith('fork_') or name.startswith("merge_"):
        return attr, None

    coll = db.functions

    func_ser = _func_name(attr['function'])

    for func_entry in coll.find({'function_id': name}):
        if func_entry['function_name'] == func_ser and \
            func_entry['version'] == attr['version']:
            return func_entry['_id'], None

    entry = {
        '_id': str(uuid.uuid4()),
        'function_id': name,
        'function_name': func_ser,
        'version': attr['version'],
        'environment': attr['env'],
        'dependency_vars': attr['dependency_vars'],
        'backend_setting': attr['attributes']
    }

    if 'optional' in attr:
        entry['optional'] = True

    return entry['_id'], InsertOne(entry)


def _serialize_node(db, session_id, node_id, node, functions):

    coll = db.function_graph

    is_fork = False
    is_merge = False
    is_flatten = False

    identifier = []
    calls = []
    binds = []

    optional = False

    for call, bind in node['sequence']:
        if call == 'START' or call == 'STOP':
            continue
        if call.startswith('fork_'):
            is_fork = bind
            identifier.append('__fork__')
            continue
        if call.startswith('merge_'):
            is_merge = bind
            is_flatten = 'flatten' in functions[call]
            identifier.append('__merge__')
            continue

        if call in functions:
            call_func = functions[call]
            identifier.append(str(call_func))
            calls.append(call_func)
            binds.append(bind)

            if call.startswith("optional("):
                optional = True

    if len(calls) == 0 and not is_fork and not is_merge:
        return None

    identifier = hash_str(
        '::'.join(
            sorted(identifier)
        )
    )

    for call in coll.find({'_id': identifier}):
        if call['session_id'] == session_id:
            return call

    if len(binds) > 0:
        binds[-1] = ['__out__']

    entry = {
        '_id': identifier,
        'session_id': session_id,
        'calls': calls,
        'bindings': binds,
        'ingoing': [],
        'outgoing': [],
        'destinations': []
    }

    if is_fork:
        entry['fork'] = is_fork
    if is_merge:
        entry['merge'] = is_merge
    if is_flatten:
        entry['flatten'] = True
    if optional:
        entry['optional'] = True

    return entry


def _merge_graph(graph, nodes):

    updates = set([])
    for n, entry in nodes.items():
        if entry is None:
            continue
        ingoing = [(entry['ingoing'][i], entry['destinations'][i])
                   for i in range(len(entry['ingoing']))]
        ingoing = {str(o[0]): (i, o[1]) for i, o in enumerate(ingoing)}

        for v, _, dest in graph.in_edges(n, data="dest"):
            if nodes[v] is None:
                continue
            v_id = nodes[v]['_id']
            if str(v_id) not in ingoing:
                entry['ingoing'].append(v_id)
                entry['destinations'].append(dest)
                updates.add(n)
            else:
                ix, destinations = ingoing[str(v_id)]
                destinations = set(destinations)
                for d in dest:
                    if d not in destinations:
                        entry['destinations'][ix].append(d)
                        updates.add(n)

        out = set([str(e) for e in entry['outgoing']])
        for _, u in graph.out_edges(n):
            if nodes[u] is None:
                continue
            u_id = nodes[u]['_id']
            if str(u_id) not in out:
                entry['outgoing'].append(u_id)
                updates.add(n)

        if len(ingoing) == 0 and len(out) == 0:
            updates.add(n)
    return updates


def _serialize_graph(session_id, req_id, sequence_graph):
    db = get_db()

    if db.sessions.find_one({'_id': session_id}) is None:
        raise SessionNotInitializedException()

    if db.requests.find_one({'_id': req_id}) is not None:
        return

    updates = []

    functions = {}

    for k, func in sequence_graph.graph['functions'].items():
        id, update = _serialize_func(
            db, session_id, k, func
        )
        functions[k] = id
        if update is not None:
            updates.append(update)

    if len(updates) > 0:
        db.functions.bulk_write(updates)
        logger.info("Registered %i functions." % len(updates))
    updates = []

    nodes = {}

    for n in sequence_graph:
        node = sequence_graph.nodes[n]
        nodes[n] = _serialize_node(
            db, session_id, n, node, functions
        )

    saves = _merge_graph(sequence_graph, nodes)

    for n in saves:
        entry = nodes[n]
        if entry is None:
            continue
        updates.append(
            ReplaceOne(
                {'_id': entry['_id']},
                entry,
                upsert=True
            )
        )

    if len(updates) > 0:
        db.function_graph.bulk_write(updates)
        logger.info("Updated %i nodes in session graph." % len(updates))

    start = sequence_graph.graph['start']
    stop = sequence_graph.graph['stop']

    start_ids = []
    stop_ids = []

    for _, v in sequence_graph.out_edges(start):
        start_ids.append(
            nodes[v]['_id']
        )

    for u, _ in sequence_graph.in_edges(stop):
        stop_ids.append(
            nodes[u]['_id']
        )

    entry = {
        '_id': req_id,
        'session_id': session_id,
        'start_time': str(datetime.datetime.now()),
        'initials': start_ids,
        'endpoints': stop_ids
    }
    db.requests.insert_one(entry)

    session = db.sessions.find_one({'_id': session_id})
    start_points = set(session['start_points'])
    start_points = start_points.union(set(start_ids))
    session['start_points'] = list(start_points)
    db.sessions.replace_one({'_id': session_id}, session)

    logger.info("Created execution request [session: %s, request_id: %s]" % (session_id, req_id))


def _retrieve_and_destroy(session_id, req_id):
    db = get_db()
    requests = db.requests
    graph = db.function_graph
    runs = db.function_runs

    req = requests.find_one({'_id': req_id})

    if req is None:
        raise RemoteError("Invalid request id %s" % req_id)

    results = []

    try:
        for end in req['endpoints']:
            end_node = graph.find_one({'_id': end})

            if 'error' in end_node:
                errors = []
                for err in runs.find({'fork_id': end_node['run_id'],
                                      'error': {'$exists': True}},
                                     ['error']):
                    errors.append(err['error'])
                errors = '------ ERROR ---------- \n'.join(errors)
                raise RemoteError(errors)

            if 'result' not in end_node:
                raise RemoteError("Request %s is not finished." % req_id)

            result = dio.load(db, end_node['result'])
            if isinstance(result, ForkResource):
                result = result.obj_

            results.append(result)
    finally:
        requests.delete_one({'_id': req_id})

    return results


class RemoteBackend:

    def __init__(self):
        self._requests = set([])

    def init(self, session_id):
        db = get_db()
        if db.sessions.find_one({'_id': session_id}) is None:
            db.sessions.insert_one(
                {
                    '_id': session_id,
                    'time': str(datetime.datetime.now()),
                    'start_points': []
                }
            )

    def attach(self, session_id, req_id, sequence_graph):
        _serialize_graph(
            session_id, req_id, sequence_graph
        )
        self._requests.add(req_id)

    def execute(self, session_id):
        rabbitmq_handling.start_session_request(
            session_id
        )
        return True

    def retrieve_result(self, session, req_id):

        # Block
        result = rabbitmq_handling.wait_for_request(session, req_id)

        self._requests.remove(req_id)
        if result != "SUCCESS":
            get_db().requests.delete_one({'_id': req_id})
            raise RemoteError(result)

        return _retrieve_and_destroy(session, req_id)

    def cancel_session(self, session):
        for req_id in self._requests:
            try:
                get_db().requests.delete_one({'_id': req_id})
            except Exception:
                pass

        rabbitmq_handling.close_connections()


def openRemoteSession(session_id=None, auto_join=False):
    return Session(session=session_id, auto_join=auto_join,
                   backend=RemoteBackend())


if __name__ == '__main__':
    with openRemoteSession(auto_join=True,
                           session_id="317e3bb0-caf4-4f57-9975-0e782371a866")\
                           as sess:
        print(sess.run(dummy_composite()))
