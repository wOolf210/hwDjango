from django.contrib import admin
from django.contrib.sessions.backends import file
from django.urls import path,include

from .views import *

app_name = 'app'

urlpatterns = [
    path('all/',index,name='all'),
    path('python/',index2,name='index2'),
    path('html/', index_html, name='index_html'),
    path('html/python/', index2, name='index_htm'),
    path('rubric/<int:pk>/', detail, name='detail'),
    path('bb/<int:pk>/', detail_bb, name='detail_bb'),
    path('add-bb/',cache_page(300)(add_bb), name='add_bb'),
    path('stream/',stream,name='stream'),
    path('file/',file_response,name='file'),
    path('json/',json_response,name='json'),
    path('update/<int:pk>/bb/',update_bb,name='update_bb'),
    path('delete/<int:pk>/bb/',delete_bb,name='delete_bb'),
    #Class Views
    path('create/class/',BbCreateView.as_view(),name='create'),
    path('by_rubric/class/<int:rubric_id>/',BbByRubricTemplateView.as_view(),name='by_rubric'),
    path('rubric_detail/class/<int:rubric_id>/',RubricDetailView.as_view(),name='rubric_detail'),
    path('bb_detail/class/<int:pk>/',BbDetailView.as_view(),name='bb_detail'),
    path('all/class/',BbListView.as_view(),name='all_class'),
    path('update/bb/class/<int:pk>/',BbUpdateView.as_view(),name='update_bb_class'),
    path('delete/bb/class/<int:pk>/',BbDeleteView.as_view(),name='delete_bb_class'),

    #date
    path('archive/',BbIndexArchiveView.as_view(),name='archive'),
    path('archive/<int:year>/',BbYearArchiveView.as_view(),name='archive-year'),
    path('archive/<int:year>/<int:month>/', BbMonthArchiveView.as_view(),name='archive-month'),
    path('archive/<int:year>/week/<int:week>/', BbWeekArchiveView.as_view(),name='archive-week'),
    path('archive/<int:year>/<int:month>/<int:day>/', BbDayArchiveView.as_view(),name='archive-day'),
    path('archive/today/',BbTodayArchiveView.as_view(),name='archive-today'),
    path('redirect/',BbRedirectView.as_view(),name='redirect'),
    path('merge/<int:rubric_id>/',MergeBbRubricView.as_view(),name='merge'),
    path('contact/',ContactFormView.as_view(),name='contact'),
    path('all-bboards/',TemplateAllBboard.as_view(),name='all_bboards'),
    path('test/',TestView.as_view(),name='test'),
    path('bootstrap/',BootstrapFormView.as_view(),name='bootstrap'),
    path('paginator/',bb_paginator,name='paginator'),
    path('paginator-class/',BbListViewPaginator.as_view(),name='paginator-class'),
    path('rubric-formset/',RubricSetView.as_view(),name='rubric_formset'),
    path('quiz/<int:pk>/',QuizFormsetView.as_view(),name='quiz_formset'),
    path('atomic/',manual_transaction_example,name='atomic'),
    path('atomic-auto/', atomic_transaction_example, name='atomic-auto'),
    path('json-response/', BbJsonView.as_view(), name='json-response'),
    path('cache/',cache_backend,name='cache'),
    path('filter/',filter,name='filter'),

    path("doclist/", docs_list, name="docs_list"),
    path("photos/", photos_list, name="photos_list"),

    path("upload/doc/", UploadDocumentView.as_view(), name="upload_doc"),
    path("upload/doc/many/", UploadManyDocsView.as_view(), name="upload_many"),
    path("upload/photo/", UploadPhotoView.as_view(), name="upload_photo"),

    path("delete/doc/<int:pk>/", delete_document, name="delete_document"),
    path("delete/photo/<int:pk>/", delete_photo, name="delete_photo"),

    path("gallery/", gallery_list, name="gallery_list"),

    path("upload/resized/", UploadResizedPhotoView.as_view(), name="upload_resized"),
]

















