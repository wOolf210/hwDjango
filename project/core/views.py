from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from .models import Post

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "registration/home.html"

class PostListView(PermissionRequiredMixin, ListView):
    permission_required = "core.view_secret_post"
    model = Post
    template_name = "registration/post_list.html"

class PostCreateView(LoginRequiredMixin,CreateView):
    model = Post
    fields = ['title', 'body']
    template_name = "registration/post_create.html"
    success_url = "/core/posts/"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



def bbcode(request):
    example=(
        "[b]Жирный текст[/b]\n"
        "[i] Курсив[/i]\n"
        "[url=https://pypi.org]Ссылка [/url]\n"
        "[quote]Цитата[/quote]\n"
        "[list]\n"
        "[*] Первый пункт\n" 
        "[*] Второй пункт]\n"
        "[/list]\n"
        ":) \n"
        "[spoiler]SPOILER[/spoiler] \n"
        "[under]UNDERLINE[/under]"
    )
    post=Post.objects.first()
    context = {"example":example,"post":post}
    return render(request, "core/bbcode.html", context)



def index(request):
    text=[
        "Example Middleware",
        f"Request Id:{getattr(request, 'request_id', '-')}",
    ]
    time.sleep(1)
    return HttpResponse("<br>".join(text))

import time

def sleep_view(request):
    time.sleep(0.2)
    return HttpResponse("Sleep 200 ms")

def api_ping(request):
    return JsonResponse(
        {
            "ok": True,
            "request_id": getattr(request, 'request_id', None),
        }
    )

def error_view(request):
    raise RuntimeError("Boom!")


def template_view(request):
    context = {
        "title":"Template View",
    }
    return render(request, "core/template_view.html", context)