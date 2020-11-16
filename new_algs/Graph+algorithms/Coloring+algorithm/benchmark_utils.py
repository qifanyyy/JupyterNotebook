from __future__ import print_function
import functools
from inspect import getcallargs
try:
    from time import perf_counter as process_time
except ImportError:
    from time import clock as process_time
from os import path
import shortuuid as sid


def trace(func):
    if search_step_trace.enabled:
        return search_step_trace(func)
    else:
        return func


def print_trace(prob, sol):
    if search_step_trace.enabled:
        search_step_trace.print_trace(prob, sol)
    else:
        pass


class search_step_trace(object):

    enabled = False
    __instances = {}
    env_name = "default"
    dir_path = ""
    __id = sid.ShortUUID().random(length=10)

    def __init__(self, f):
        self.__f = f
        self.__name__ = f.__name__
        self.__numcalls = 0
        self.__elapsed_time = {'mean': 0.0, 'std': 0.0}
        self.__cumulative_time = 0.0
        search_step_trace.__instances[f] = self
        self.procceding = False

    def __call__(self, *args, **kwargs):
        self.__numcalls += 1

        self.procceding = True
        self.start_time = process_time()
        result = self.__f(*args, **kwargs)
        elapsed = process_time() - self.start_time
        self.procceding = False

        self.__cumulative_time += elapsed
        old_mean = self.__elapsed_time['mean']
        old_std = self.__elapsed_time['std'] * (self.__numcalls - 1)
        delta = (elapsed - old_mean)

        new_mean = (old_mean + (delta/self.__numcalls))
        new_std = old_std + ((elapsed - old_mean) * (elapsed - new_mean))
        new_std = (new_std / self.__numcalls)
        self.__elapsed_time['mean'] = new_mean
        self.__elapsed_time['std'] = new_std

        return result

    def count(self):
        return self.__numcalls

    def elapsed_time(self):
        return self.__elapsed_time

    def cumulative_time(self):
        return self.__cumulative_time

    def dump_vars(self):
        trace = (self.count(),
                 self.elapsed_time(),
                 self.cumulative_time())
        return trace

    def clear_vars(self):
        self.__numcalls = 0
        self.__elapsed_time = {'mean': 0.0, 'std': 0.0}
        self.__cumulative_time = 0.0

    @staticmethod
    def set_trace(data):
        for func in search_step_trace.__instances.values():
            name = func.__name__
            trace = data.get(name)
            if trace is not None:
                try:
                    func.__numcalls = trace[0]
                    func.__elapsed_time['mean'] = trace[1]['mean']
                    func.__elapsed_time['std'] = trace[1]['std']
                    func.__cumulative_time = trace[2]
                except:
                    print(name, trace)

    @staticmethod
    def dump_all():
        """Return a dict of {function: # of calls}
           for all registered functions."""
        dump = {}
        for func, trace in search_step_trace.__instances.items():
            if trace.__numcalls > 0:
                stat = trace.dump_vars()
                dump[func.__name__] = stat
        return dump

    @staticmethod
    def clear_func(func):
        trace = search_step_trace.__instances.get(func)
        if trace is not None:
            trace.clear_vars()

    @staticmethod
    def clear_all():
        for func, trace in search_step_trace.__instances.items():
            trace.clear_vars()
        search_step_trace.__id = sid.ShortUUID().random(length=10)

    @staticmethod
    def print_format():
        return '{0:<30} {1[0]:<10} {1[1][mean]:<10f} {1[1][std]:<10f} {1[2]:<10f}'

    @staticmethod
    def csv_format():
        return '{0}, {1[0]:d}, {1[1][mean]:f}, {1[1][std]:f}, {1[2]:f}'

    @staticmethod
    def print_trace(prob, sol):
        env_name = search_step_trace.env_name
        dir_name = path.abspath(search_step_trace.dir_path)
        tracefname = "{0}/{1}.qst".format(dir_name, env_name)
        with open(tracefname, 'a') as f:
            trace = search_step_trace.dump_all()
            for name, data in trace.items():
                if data is not None:
                    print(prob.name, ", ", sol.get_max_col(), ", ",
                          search_step_trace.__id, ", ",
                          search_step_trace.csv_format().format(name, data),
                          file=f, sep="")
            print("", file=f)


def set_env(func):
    @functools.wraps(func)
    def echo_func(*args, **kwargs):
        callargs = getcallargs(func, *args, **kwargs)
        for kw, arg in callargs.items():
            if type(arg).__name__ is "PackColSolution" and arg.record is not None:
                search_step_trace.set_trace(arg.record)

        return func(*args, **kwargs)
    return echo_func


# class conditional_decorator(object):
#     def __init__(self, dec, condition):
#         self.decorator = dec
#         self.condition = condition

#     def __call__(self, func):
#         if not self.condition:
#             # Return the function unchanged, not decorated.
#             return func
#         return self.decorator(func)