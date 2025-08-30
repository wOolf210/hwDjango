import time
import json
import uuid
from typing import Callable,Optional
from django.http import HttpRequest, HttpResponse,JsonResponse
from django.template.response import TemplateResponse
from django.utils.deprecation import MiddlewareMixin

def simple_middleware(get_response: Callable[[HttpRequest],HttpResponse]):

    #initialization code
    def middleware(request: HttpRequest) -> HttpResponse:
        #До вызова view (изменяем request)
        response= get_response(request)
        # После вызова view (изменяем response)
        response.headers['X-Project'] = "Middleware Example"
        return response


    return middleware

class RequestIdMiddleware:

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        # Initialization code

        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # Generate a unique request ID
        request_id = str(uuid.uuid4())
        request.request_id = request_id

        # Process the request
        response = self.get_response(request)

        # Add the request ID to the response headers
        response.headers['X-Request-ID'] = request_id
        return response



class TimingMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start_time = time.perf_counter()
        response = self.get_response(request)
        dur_ms = int((time.perf_counter() - start_time) * 1000)
        response.headers['X-Processing-Time'] = str(dur_ms)
        return response

    def process_template_response(self, request: HttpRequest, response: TemplateResponse):
        ctx= response.context_data or {}
        ctx['x-processing-time']=response.headers.get('X-Processing-Time')
        response.context_data = ctx
        return response


class BlockIpMiddleware:
    BLOCKED_IPS = {"127.0.0.2"}
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return response

    def process_view(self, request: HttpRequest, view_func, view_args, view_kwargs):
        client_ip = request.META.get('REMOTE_ADDR') or ""
        if client_ip in self.BLOCKED_IPS:
            return HttpResponse("Access denied", status=403)
        return None



class ExceptionMiddleware:
    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        if request.path.startswith("/core/api/"):
            data={
                "error": str(exception),
                "type": type(exception).__name__,
                "request_id": getattr(request, 'request_id', None),

            }
            return JsonResponse(data, status=500)
        return None


from django.http import HttpResponse

class BlockForbiddenWordsMiddleware:
    FORBIDDEN_WORDS = {"hack", "forbidden", "badword"}

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path.lower()

        for word in self.FORBIDDEN_WORDS:
            if word in path:
                return HttpResponse(
                    f"Запрещённое слово в URL: '{word}'",
                    status=403
                )

        return self.get_response(request)
