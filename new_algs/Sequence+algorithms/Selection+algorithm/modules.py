import torch as th
from torch import nn as thnn
from torch_geometric import nn as pygnn

from tasks.torch import models as tm
from tasks.torch import modelx as mx

from inspect import signature, Parameter, isfunction
import copy

__method_name__ = ['__init__', 'forward']


class AliasManager:

    def __init__(self, aliases=[]):
        self._aliases = {}
        for a in aliases:
            self.add_aliases(a)

    def add_aliases(self, aliases):
        aliases = set(aliases)

        for alias in aliases:
            old_alias = set([])
            if alias in self._aliases:
                old_alias = self._aliases[alias]
            self._aliases[alias] = set.union(old_alias, aliases)

    def add_alias(self, name, alias):
        self.add_aliases([name, alias])

    def get_alias(self, key, of=None):
        alias = set([key])
        if key in self._aliases:
            alias = self._aliases[key]

        if of is None:
            return alias

        of = set(of)
        return of.intersection(alias)

    def get_item(self, dictionary, key, ret='raise'):
        for alias in self.get_alias(key, of=dictionary.keys()):
            return dictionary[alias]
        if ret == 'raise':
            raise KeyError("Unknown key %s." % key)
        return ret


alias = AliasManager([['x', 'input'],
                     ['out_features', 'node_dim', 'dim', 'out_channels',
                      'out_channel'],
                     ['global_inp', 'condition'],
                     ['global_channels', 'cond_channels'],
                     ['in_features', 'in_channel', 'in_channels']])


def warn_unused(name, config, options):

    for k in config.keys():
        if k not in options:
            print("WARNING: Config \"%s\" will not be used for module %s." % (k, name))


def _get_func_param(func):
    out = {}
    sig = signature(func)

    for name, parameter in sig.parameters.items():
        if name != 'self':
            optional = parameter.default != Parameter.empty
            out[name] = optional

    return out


def _get_param(module, method):
    out = {}

    if method in dir(module):
        method_func = getattr(module, method)
        out = _get_func_param(method_func)

    return out


def get_parameter(module, methods):
    out = {}

    for m in methods:
        out[m] = _get_param(module, m)

    return out


class ModuleDescription:

    def __init__(self, module):
        self._module = module
        param = get_parameter(module, __method_name__)
        self._config_options = param['__init__']
        del param['__init__']
        self._input = param
        self._name = module.__name__

    def get_name(self):
        return self._name

    def get_config_options(self):
        return self._config_options

    def get_input_options(self):
        return self._input

    def get_module(self):
        return self._module

    def __call__(self, config):

        name = self.get_name()
        kwargs = {}
        options = self.get_config_options()

        for k, optional in options.items():
            if k in config:
                val = config[k]
                if val is not None or not optional:
                    kwargs[k] = val
            else:
                if not optional:
                    raise ValueError("Module %s require module option \"%s\"."
                                     % (name, k))

        warn_unused(name, config, options)

        if 'kwargs' in kwargs:
            del kwargs['kwargs']

        return self.get_module()(**kwargs)

    def __str__(self):
        return '%s(%s)' % (self.get_name(),
                           ', '.join(self.get_config_options().keys()))


class ModuleHandler:

    def __init__(self, name, base):
        self._name = name
        self._base = base

    def get_inputs(self):
        pass

    def get_outputs(self):
        pass

    def bind_input(self, key, size):
        pass

    def get_output_size(self, key):
        pass

    def get_name(self):
        return self._name

    def build(self):
        pass

    def is_function(self):
        return False

    def __getstate__(self):
        out = {}
        out.update(self._base)
        out['type'] = self.get_name()
        return out


def bind_out(src_config, target_config, key='out_features'):
    target = alias.get_alias(key, of=target_config.keys())
    if len(target) == 0:
        return None
    size = alias.get_item(src_config, key, ret=None)
    if size is None:
        raise ValueError("Expect an output size for Torch Modules")
    for k in target:
        target_config[k] = size
    return size


def bind_general(src_config, target_config, definition):
    for k in list(definition):
        for a in alias.get_alias(k, of=src_config.keys()):
            for b in alias.get_alias(k, of=target_config.keys()):
                target_config[b] = src_config[a]


class NotInitializedException(Exception):
    pass


class TorchHandler(ModuleHandler):

    def __init__(self, name, module, config):
        super().__init__(name, config)
        self._base_config = config
        self._module = ModuleDescription(module)
        self._config = {k: None
                        for k in self._module.get_config_options().keys()}
        self._output_size = bind_out(config, self._config)
        bind_general(config, self._config,
                     self._module.get_config_options().keys())
        input_ = self._module.get_input_options()
        method = alias.get_alias('forward', of=input_.keys())
        self._method = next(iter(method))
        input_ = input_[self._method]
        self._input = alias.get_alias('input', of=input_.keys())

    def get_inputs(self):
        return self._input

    def get_outputs(self):
        return [self._method]

    def bind_input(self, key, size):
        if key in self._input:
            for a in alias.get_alias('in_features', of=self._config.keys()):
                self._config[a] = size
            if self._output_size is None:
                self._output_size = size

    def get_output_size(self, key):
        if key == self._method:
            return self._output_size
        raise NotInitializedException()

    def build(self):
        return self._module(self._config)

    def __str__(self):
        name = self._module.get_name()
        assign = [
            '%s=%s' % (k, str(v) if v is not None else '?')
            for k, v in self._config.items()
        ]
        return "%s(%s) -> %d" % (name, ', '.join(assign), self._output_size)


class SimpleGraphHandler(ModuleHandler):

    def __init__(self, name, module, config):
        super().__init__(name, config)
        self._module = ModuleDescription(module)
        self._config = {k: None
                        for k in self._module.get_config_options().keys()}
        self._output_size = bind_out(config, self._config, 'out_channels')
        bind_general(config, self._config,
                     self._module.get_config_options().keys())

        input_ = self._module.get_input_options()
        method = alias.get_alias('forward', of=input_.keys())
        self._method = next(iter(method))
        input_ = input_[self._method]
        self._node = alias.get_alias('x', of=input_.keys())
        self._edge = alias.get_alias('edge_index', of=input_.keys())

    def get_inputs(self):
        return set.union(self._node, self._edge)

    def get_outputs(self):
        return [self._method]

    def bind_input(self, key, size):
        if key in self._node:
            for a in alias.get_alias('in_channels', of=self._config.keys()):
                self._config[a] = size

    def get_output_size(self, key):
        if key == self._method:
            return self._output_size
        raise NotInitializedException()

    def build(self):
        return self._module(self._config)

    def __str__(self):
        name = self._module.get_name()
        assign = [
            '%s=%s' % (k, str(v) if v is not None else '?')
            for k, v in self._config.items()
        ]
        return "%s(%s) -> %d" % (name, ', '.join(assign), self._output_size)


class GraphFunctionHandler(ModuleHandler):

    def __init__(self, name, func, config):
        super().__init__(name, config)
        params = _get_func_param(func)
        self._func = func
        self._params = set([k for k, v in params.items() if not v])
        self._size = None

    def get_inputs(self):
        return self._params

    def get_outputs(self):
        return ['forward']

    def bind_input(self, key, size):
        if key == 'x':
            self._size = size

    def get_output_size(self, key):
        if key == 'forward':
            return self._size
        raise NotInitializedException()

    def is_function(self):
        return True

    def build(self):
        return self._func

    def __str__(self):
        name = self._func.__name__
        assign = [
            '%s=%s' % (k, self._size if self._size is not None else '?')
            for k in self._params
        ]
        return "%s(%s) -> %d" % (name, ', '.join(assign), self._output_size)


class GraphHandler(ModuleHandler):

    def __init__(self, name, module, config, idempotent=False):
        super().__init__(name, config)
        self._module = ModuleDescription(module)
        self._config = {k: None
                        for k in self._module.get_config_options().keys()}
        self._output_size = bind_out(config, self._config)
        bind_general(config, self._config,
                     self._module.get_config_options().keys())
        input_ = self._module.get_input_options()
        method = alias.get_alias('forward', of=input_.keys())
        self._method = next(iter(method))
        input_ = input_[self._method]
        self._node = alias.get_alias('x', of=input_.keys())
        self._batch = alias.get_alias('batch', of=input_.keys())
        self._global = alias.get_alias('global_inp', of=input_.keys())
        self._edge_index = alias.get_alias('edge_index', of=input_.keys())
        self._edge_attr = alias.get_alias('edge_attr', of=input_.keys())
        self.idempotent = idempotent

    def get_inputs(self):
        return set.union(self._node, self._batch, self._global,
                         self._edge_attr, self._edge_index)

    def get_outputs(self):
        return [self._method]

    def bind_input(self, key, size):
        if key in self._node:
            for a in alias.get_alias('in_channels', of=self._config.keys()):
                self._config[a] = size
            if self.idempotent:
                self._output_size = size
        if key in self._global:
            for a in alias.get_alias('global_channels', of=self._config.keys()):
                self._config[a] = size
        if key in self._edge_attr:
            for a in alias.get_alias('edge_channels', of=self._config.keys()):
                self._config[a] = size

    def get_output_size(self, key):
        if key == self._method:
            return self._output_size
        raise NotInitializedException()

    def build(self):
        return self._module(self._config)

    def __str__(self):
        name = self._module.get_name()
        assign = [
            '%s=%s' % (k, str(v) if v is not None else '?')
            for k, v in self._config.items()
        ]
        return "%s(%s) -> %d" % (name, ', '.join(assign), self._output_size)


class GraphDenseHandler(GraphHandler):

    def __init__(self, name, module, config):
        super().__init__(name, module, config, False)
        self._tmp_output = self._output_size

    def bind_input(self, key, size):
        if key in self._node:
            for a in alias.get_alias('in_channels', of=self._config.keys()):
                self._config[a] = size
            self._output_size = self._tmp_output + size
        else:
            super().bind_input(key, size)


def create_handler(type, config):

    if type == 'tasks::cga':
        return GraphHandler(type, tm.ConditionalGlobalAttention, config,
                            idempotent=True)

    if type == 'mx::cga':
        return GraphHandler(type, mx.ConditionalGlobalAttention, config)

    if type.startswith('tasks::'):
        type_ = type[7:]
        if type_ in dir(tm):
            module = getattr(tm, type_)

            if isfunction(module):
                return GraphFunctionHandler(type, module, config)

            return GraphHandler(type, module, config)

    if type.startswith('dense::'):
        type_ = type[7:]
        if type_ in dir(mx):
            module = getattr(mx, type_)

            if isfunction(module):
                raise ValueError("No dense function: %s" % type_)

            return GraphDenseHandler(type, module, config)

    if type.startswith('mx::'):
        type_ = type[4:]
        if type_ in dir(mx):
            module = getattr(mx, type_)

            if isfunction(module):
                return GraphFunctionHandler(type, module, config)

            return GraphHandler(type, module, config)

    if type.startswith('geo::'):
        type_ = type[5:]
        if type_ in dir(pygnn):
            module = getattr(pygnn, type_)

            if isfunction(module):
                return GraphFunctionHandler(type, module, config)

            return SimpleGraphHandler(type, module, config)

    if type.startswith('torch::'):
        type_ = type[7:]
        if type_ in dir(thnn):
            module = getattr(thnn, type_)
            return TorchHandler(type, module, config)

    raise ValueError("Unknown type %s as torch module" % type)
