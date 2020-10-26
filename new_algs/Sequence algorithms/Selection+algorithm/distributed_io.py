from taskflow.backend import ForkResource
import json
import gridfs
import uuid
from bson.objectid import ObjectId


class Reference(object):

    def __init__(self, db, reference):
        self.db_ = db
        self.reference_ = reference

    def load(self):
        return load(self.db_, self.reference_, partial=False)

    def __repr__(self):
        return "ref [ %s ]" % str(self.reference_)


def _json_to_gridfs(db, obj):
    grid = gridfs.GridFS(db)

    id = str(uuid.uuid4())

    obj_json = json.dumps(obj).encode('utf-8')

    grid.put(
        obj_json, file_type="json", _id=id
    )

    return 'json_'+id


def _gridfs_to_json(db, ref):
    grid = gridfs.GridFS(db)
    file = grid.get(ref).read().decode('utf-8')

    return json.loads(file)


def store_list(db, L):
    ref_list = [store(db, l) for l in L]
    id = str(uuid.uuid4())

    db.datastructures.insert_one(
        {
            '_id': id,
            'type': 'list',
            'content': ref_list
        }
    )

    return "list_"+id


def store_dict(db, D):
    ref_list = {k: store(db, v) for k, v in D.items()}
    id = str(uuid.uuid4())

    db.datastructures.insert_one(
        {
            '_id': id,
            'type': 'dict',
            'content': ref_list
        }
    )
    return 'dict_'+id


def store(db, obj):

    if obj is None:
        return "<null>"

    if isinstance(obj, Reference):
        return obj.reference_

    if isinstance(obj, ObjectId):
        return obj

    if isinstance(obj, ForkResource):
        return "fork_%s_%s" % (obj.src_, store(db, obj.obj_))

    if isinstance(obj, str):
        return "s\'%s\'" % obj

    if isinstance(obj, int):
        return "i\'%i\'" % obj

    if isinstance(obj, float):
        return "f\'%f\'" % obj

    if isinstance(obj, dict):
        return store_dict(db, obj)

    if isinstance(obj, list) or isinstance(obj, tuple):
        return store_list(db, obj)

    return _json_to_gridfs(db, obj)


def _rebuild_fork(db, ref, partial):
    states = ref.split('_')

    src = states[1]
    obj_ref = '_'.join(states[2:])
    obj = load(db, obj_ref, partial)

    return ForkResource(obj, src)


def _rebuild_list(db, ref, partial):

    L = db.datastructures.find_one({'_id': ref})
    if L is None:
        raise ValueError("%s does not exist." % ref)
    if L['type'] != 'list':
        raise ValueError("%s is not a list." % ref)

    return [load(db, r, partial) for r in L['content']]


def _rebuild_dict(db, ref, partial):

    L = db.datastructures.find_one({'_id': ref})
    if L is None:
        raise ValueError("%s does not exist." % ref)
    if L['type'] != 'dict':
        raise ValueError("%s is not a list." % ref)

    return {r: load(db, v, partial) for r, v in L['content'].items()}


def load(db, obj_ref, partial=False):

    if isinstance(obj_ref, ObjectId):
        return obj_ref

    if obj_ref == '<null>':
        return None

    if obj_ref.startswith('fork_'):
        return _rebuild_fork(db, obj_ref, partial)

    if obj_ref.startswith("list_"):
        obj_ref = obj_ref[5:]
        return _rebuild_list(db, obj_ref, partial)

    if obj_ref.startswith("dict_"):
        obj_ref = obj_ref[5:]
        return _rebuild_dict(db, obj_ref, partial)

    if partial:
        return Reference(db, obj_ref)

    if obj_ref.startswith("s\'"):
        return obj_ref[2:-1]

    if obj_ref.startswith("i\'"):
        return int(obj_ref[2:-1])

    if obj_ref.startswith("f\'"):
        return float(obj_ref[2:-1])

    if obj_ref.startswith("json_"):
        obj_ref = obj_ref[5:]
        return _gridfs_to_json(db, obj_ref)

    raise ValueError("Unknown type for ref %s", obj_ref)


def batch_load(db, obj_refs, partial=False):
    return [
        load(db, r, partial) for r in obj_refs
    ]
