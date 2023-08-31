from functools import wraps
import inspect
from typing import Callable


def serving(_func=None, *, websocket: bool = False, auth: Callable = None):
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        wrapper = async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper
        _args = {
            'name': func.__name__,
            'doc': func.__doc__,
            'params': {
                'include_callback_handlers': websocket,
                # If websocket is True, pass the callback handlers to the client.
                'auth': auth,
            },
        }
        if websocket:
            wrapper.__ws_serving__ = _args
        else:
            wrapper.__serving__ = _args

        return wrapper

    return decorator if _func is None else decorator(_func)
