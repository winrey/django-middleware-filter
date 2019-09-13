from inspect import isfunction, isclass
from functools import wraps


def _noop(*args, **kwargs):
    return None

def _middleware_function_filter(filter_func):
    """
    @param filter_func: Receives a Request argument. The code will use this middleware if returns true or bypass the middleware if it returns false.
    """
    def decorator(middleware_func):
        @wraps(middleware_func)
        def wrapper(get_response):
            origin_middleware = middleware_func(get_response)
            def middleware(request):
                if filter_func(request):
                    return origin_middleware(request)
                # bypass the middleware
                return get_response(request)
            return middleware
        return wrapper
    return decorator

def _middleware_class_filter(filter_func):
    """
    @param filter_func: Receives a Request argument. The code will use this middleware if returns true or bypass the middleware if it returns false.
    """

    def class_func_filter(cls, name, bypass_func=_noop):
        "WARNING: This is NOT a pure function!"
        if hasattr(cls, name):
            origin = getattr(cls, name)
            def class_func_wrapper(self, request, *args, **kwargs):
                if filter_func(request):
                    return origin(self, request, *args, **kwargs)
                return bypass_func(request)
            setattr(cls, name, class_func_wrapper)

    def decorator(Middleware):
        class_func_filter(Middleware, "__call__")
        class_func_filter(Middleware, "process_view")
        class_func_filter(Middleware, "process_exception")
        class_func_filter(Middleware, "process_template_response", lambda self, req, res: res)
        return Middleware

    return decorator
    

def middleware_filter(filter_func):
    """
    @param filter_func: Receives a Request argument. The code will use this middleware if returns true or bypass the middleware if it returns false.
    """
    def decorator(middleware):
        if isclass(middleware):
            return _middleware_class_filter(filter_func)(middleware)
        elif isfunction(middleware):
            return _middleware_function_filter(filter_func)(middleware)
        else:
            raise "Unsupported Middleware Type"
    return decorator

def _add_slash_prefix_if_not_exists(path):
    return path if path.startswith("/") else ("/" + path)

def start_with(path):
    path = _add_slash_prefix_if_not_exists(path)
    # Using path_info instead of path by the following reason.
    # https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.path_info
    return middleware_filter(lambda req: req.path_info.startswith(path))

def exempt_start_with(path):
    path = _add_slash_prefix_if_not_exists(path)
    # Using path_info instead of path by the following reason.
    # https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.path_info
    return middleware_filter(lambda req: not req.path_info.startswith(path))
