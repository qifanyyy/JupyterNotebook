import uuid
import hashlib
from inspect import signature


def hash_str(string):
    bytes = string.encode('utf-8')
    h = hashlib.blake2b(digest_size=32)
    h.update(bytes)
    return str(h.hexdigest())


def __create_sym(function, args, kwargs):
    sig = signature(function)
    bound_args = sig.bind(*args, **kwargs)

    env_args_ = {}
    task_args_ = {}

    for k in bound_args.arguments:
        x = bound_args.arguments[k]

        if isinstance(x, Symbolic):
            task_args_[k] = x
        else:
            env_args_[k] = x

    return SymbolicFunction(function, "1.0",
                            sig, env_args_, task_args_)


def get_item_inner(obj, key):
    return obj[key]


def get_item(obj, key):
    return __create_sym(
        get_item_inner, [obj, key], {}
    )


def scatter_func_inner(iterable, n):

    sc = [[] for _ in range(n)]

    for i, value in enumerate(iterable):
        sc[i % n].append(value)

    return sc


def scatter(iterable, n):
    sym = __create_sym(
        scatter_func_inner, [iterable, n], {}
    )
    return SymbolicForkElement(sym)


class ForkResource(object):

    def __init__(self, obj, src=None):
        self.src_ = src
        if self.src_ is None:
            self.src_ = str(uuid.uuid1())
        self.obj_ = obj

    def __str__(self):
        return "fork[ %s ]" % (str(self.obj_))


class Symbolic(object):

    def __getitem__(self, key):
        return get_item(self, key)


class optional(Symbolic):

    def __init__(self, obj):
        self._obj = obj

    def get_content(self):
        return self._obj

    def __str__(self):
        return "optional(%s)" % str(self._obj)

    def __identifier__(self):
        return "optional(%s)" % self._obj.__identifier__()

    def __hash__(self):
        return hash_str(optional+"_"+self._obj.hash())


class SymbolicFunction(Symbolic):

    def __init__(self, func, version, signature, env_args,
                 task_args, attr={}):
        self.function_ = func
        self.version_ = version
        self._signature = signature
        self.env_args_ = env_args
        self.task_args_ = task_args
        self.attr_ = attr

    def __exec__(self, **kwargs):
        return self.function_(**kwargs)

    def __identifier__(self):
        param = []

        for k in self._signature.parameters:
            if k in self.env_args_:
                param.append(str(self.env_args_[k]))
            elif k in self.task_args_:
                param.append("symbolic_"+hash_str(str(self.task_args_[k])))

        param = ', '.join(param)

        return self.function_.__name__+"("+param+")"

    def __hash__(self):

        param = []

        for k in self._signature.parameters:
            if k in self.env_args_:
                param.append(str(self.env_args_[k]))
            elif k in self.task_args_:
                param.append(hash_str(str(self.task_args_[k])))

        param = ', '.join(param)

        return hash_str(self.function_.__name__+"_"+param+"::"+self.version_)

    def __str__(self):
        kwargs = {}
        kwargs.update(self.env_args_)
        kwargs.update(self.task_args_)

        param = []

        for k in self._signature.parameters:
            if k in kwargs:
                param.append(str(kwargs[k]))

        param = ', '.join(param)

        return "symbolic ver. %s [ %s (%s) ]" % (self.version_,
                                                 self.function_.__name__,
                                                 param)


class SymbolicForkElement(Symbolic):

    def __init__(self, list):
        self.list_ = list

    def __identifier__(self):
        return "fork_"+self.list_.__identifier__()

    def __str__(self):
        return "element of %s" % str(self.list_)


class SymbolicMergeElement(Symbolic):

    def __init__(self, args, flatten=False):
        if not isinstance(args, list):
            args = [args]
        self.args_ = {
            '__merge__%i' % i: v for i, v in enumerate(args)
        }
        self.flatten_ = flatten

    def __identifier__(self):
        return "merge_"+str([v.__identifier__() for v in self.args_.values()])

    def __str__(self):
        return "merge of %s" % str([str(v) for v in self.args_.values()])
