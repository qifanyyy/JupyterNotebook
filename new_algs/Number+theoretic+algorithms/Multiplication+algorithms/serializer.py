"""
General serialization module. Exports two functions serialize() and unserialize().
Serialization of objects that implement __serialize__ and a class method __unserialize__ is done using these methods,
other objects are serialized using cPickle. gzip compression may be applied to too long results.
An object that wants to support efficient serialization must implement __serialize__ and a class "constructor"
__unserialize__ receiving a serialized object and returns a class instance.
"""

from cPickle import dumps, loads
from gzip import zlib
from config import Config

__all__ = ['serialize', 'unserialize']

serialize   = lambda *args, **kwargs : _Serializer.serialize(*args, **kwargs)
unserialize = lambda *args, **kwargs : _Serializer.unserialize(*args, **kwargs)

class _Serializer(object):
    """A serialization object should not be created, instead - class methods should be used.
    A serialization of an object that implements __serialize__ is a generic serialization of
    the tuple (object's class, __serialize__ of object). Iterables are recursively
    serialized. Other objects are generally serialized using cPickle and gzip.
    """
    def __init__(self):
        pass

    @classmethod
    def serialize(cls, obj):
        """Serialize the given object or iterable of objects"""
        if hasattr(obj, "__serialize__"):
            return cls._generic_serialize(obj.__class__, obj.__serialize__())
        elif isinstance(obj, dict):
            return cls._generic_serialize(dict, [(serialize(k), serialize(v)) for k,v in obj.items()])
        elif isinstance(obj, (list, tuple)):
            return cls._generic_serialize(obj.__class__, [serialize(v) for v in obj])
        else:
            return cls._generic_serialize(None, obj)

    @classmethod
    def unserialize(cls, s, cls_assert=None):
        """Unserialize the given serialized string"""
        cls, obj_s = cls._generic_unserialize(s)
        if hasattr(cls, "__unserialize__"):
            obj = cls.__unserialize__(obj_s)
        elif cls is dict:
            obj = dict((unserialize(k), unserialize(v)) for k,v in obj_s)
        elif cls in (list, tuple):
            obj = cls(unserialize(v) for v in obj_s)
        else:
            obj = obj_s
            assert cls_assert is None or isinstance(obj, cls_assert), "Invalid %s representation" % cls_assert.__name__
        return obj

    @classmethod
    def _generic_serialize(cls, *obj):
        """Serialization of general objects using cPickle and optional gzip compression"""
        if len(obj) == 1:
            obj = obj[0]
        res = dumps(obj)
        if Config.COMPRESS_SERIALIZATION and  \
           len(res) > Config.COMPRESS_LIM and \
           len(obj) >= 4:                     # Avoid multiple compressing
            return zlib.compress(res)
        else:
            return "P" + res

    @classmethod
    def _generic_unserialize(cls, s, cls_assert=None):
        """Unserialize the given string serialized using _generic_serialize"""
        if s[0] == "P":
            data = s[1:]
        else:
            data = zlib.decompress(s)
        obj = loads(data)
        assert cls_assert is None or isinstance(obj, cls_assert), "Invalid %s representation" % cls_assert.__name__
        return obj
