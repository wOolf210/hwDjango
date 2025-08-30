from django.urls import *
from .views import *
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('posts/',PostListView.as_view(),name='post_list'),
    path('posts/new/',PostCreateView.as_view(),name='post_create'),
    path('bbcode/',bbcode,name='bbcode'),
    path('index/', index, name='index'),
    path('sleep/', sleep_view, name='sleep_view'),
    path('api/ping/', api_ping, name='api_ping'),
    path('erorr/', error_view, name='error_view'),
    path('template/', template_view, name='template_view'),

]


