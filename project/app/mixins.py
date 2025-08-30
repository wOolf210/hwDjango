
from django.views.generic.base import ContextMixin
from pyexpat.errors import messages

from .models import Rubric


class RubricMixin(ContextMixin):
    menu=[
        {"title":"Главная", "url_name":"app:all_class"},
        {"title":"Создать пост", "url_name":"app:create"},
        {"title": "Контакты", "url_name": "app:contact"},
    ]
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['menu'] = self.menu
        context['rubrics']=Rubric.objects.all()
        return context


from django.http import JsonResponse

class JsonResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(context, **response_kwargs)

from django.contrib import messages
class SuccessMessageMixin:
    success_message =""

    def form_valid(self,form):
        response=super().form_valid(form)
        if self.success_message:
            messages.success(self.request, self.success_message)
            print(f"Success message: {self.success_message}")
        return response

from django.views.generic.base import ContextMixin
class CurrentTimeMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from django.utils import timezone
        current_time = timezone.now()
        context['current_time'] = current_time
        return context

import random

class RandomQuoteMixin(ContextMixin):
    quotes=[
        "Ученье свет, а неученье тьма.",
        "Век живи, век учись.",
        "Кто ищет, тот всегда найдет.",
    ]
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['quote']=random.choice(self.quotes)
        return context

import time
class ResponseTimeHeaderMixin:
    def dispatch(self, request, *args, **kwargs):
        start=time.monotonic()
        response=super().dispatch(request, *args, **kwargs)
        duration_time=(time.perf_counter()-start) * 1000
        response["X-Response-Time"] = f"{duration_time:.2f} ms"
        return response