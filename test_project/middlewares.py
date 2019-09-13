from django.http import HttpResponse
from django_middleware_filter.wrappers import *

from .utils import append

@start_with("test_start_with")
def func_test_start_with_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)
        return append(response, "<p>This is handled by a functional middleware with start_with.[10001]</p>")

    return middleware

@exempt_start_with("test_start_with")
def func_test_exempt_start_with_middleware(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        response = get_response(request)
        return append(response, "<p>This is handled by a functional middleware with exempt_start_with.[10002]</p>")

    return middleware
