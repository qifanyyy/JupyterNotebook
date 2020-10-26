"""
Debugger of Master module. Out-sourced to debugger.py for clarity.
Defines a wrapper for methods of Master, to allow breakpoints and step-by-step
with interactive shell when debugging is turned on.
"""

from utils import log
from functools import wraps
from config import Config
import code

def check_debugging(func):
    """Breakpoint logic for master"""
    def debugger(self, func_name):
        if self._debugging_on:
            log.info("BP: STEP_BY_STEP_ON")
        else:
            if self._debug_countdown is not None:
                self._debug_countdown -= 1
                if self._debug_countdown == 0:
                    log.info("BP: DEBUG_COUNTDOWN")
                    self._debugging_on = True
                    self._debug_countdown = None

        m = self._io.get_breakpoint_msg()
        while m is not None:
            self._debugging_on = True
            self._debug_countdown = None
            log.info("BP: in %s : %r", func_name, m.get_msg())
            m = self._io.get_breakpoint_msg()
        
        # Read DebugData messages or messages sniffed / duplicated to master
        m = self._io.get_breakpoint_msg()
        while m is not None:
            typ = m.get_type()
            if typ == Message.TYPE.DebugData:
                print "NODE DEBUG DATA"
                print m.get_msg()
            else:
                print "SNIFFED MESSAGE:", m
        
        # Debug console
        if self._debugging_on:
            code.interact(local=dict(globals(), **locals()))
    
    @wraps(func)
    def func_wrapper(self, *args, **kwargs):
        debugger(self, func.__name__)
        func(self, *args, **kwargs)
        debugger(self, func.__name__)
    
    # Enable debugging only if enabled in Config
    if not Config.DEBUGGING:
        return func
    else:
        return func_wrapper
