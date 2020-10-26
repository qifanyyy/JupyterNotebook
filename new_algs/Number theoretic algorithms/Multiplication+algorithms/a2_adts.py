# A single element of the list of all M^i matrices
import threading
class mElement:
        def __init__(self, M):
                self.M    = M;
                self.lock = threading.Lock();
                self.done = threading.Event();

# A single element of the list of all Ci matricies
class aElement:
        def __init__(self, A):
                self.A    = A;
                self.lock = threading.Lock();
                self.done = threading.Event();
