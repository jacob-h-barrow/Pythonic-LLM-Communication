import signal
import time
from functools import wraps

def raise_timeout(*args, **kwargs):
    raise TimeoutError()

signal.signal(signalnum=signal.SIGALRM, handler=raise_timeout)

def timeout(secs):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.alarm(secs)
            try:
                return func(*args, **kwargs)
            finally:
                signal.alarm(0)
        return wrapper

    return decorator
