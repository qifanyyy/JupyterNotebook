import signal
import PrintUtils

class TimeoutError(Exception):
    pass

def handler(signum, frame):
    raise TimeoutError()

def tryExecuteWithTimeout(func, timeout, failMessage):
    signal.signal(signal.SIGALRM, handler)
    signal.alarm(timeout)
    try:
        func()
    except TimeoutError:
        PrintUtils.printErr(failMessage)