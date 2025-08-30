from django.contrib import admin
from django.urls import *
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('cookie-demo/', cookie_demo, name='cookie_demo'),
    path('cookie-set/', cookie_set, name='cookie_set'),
    path('cookie-delete/', cookie_delete, name='cookie_delete'),

    path('session-demo/', session_demo, name='session_demo'),
    path('session-counter/', session_counter, name='session_counter'),
    path('session-set-expiry/', session_set_expiry, name='session_set_expiry'),
    path('session-flush/', session_flush, name='session_flush'),
    path('session-cycle/', session_cycle, name='session_cycle'),
    path('session-test-cookie/', session_test_cookie, name='session_test_cookie'),

    path('message-demo/', message_demo, name='message_demo'),
    path('message-success/', message_success, name='message_success'),
    path('message-error/', message_error, name='message_error'),
    path('message-notice/', message_notice, name='message_notice'),
    path('message-custom/', message_custom, name='message_custom'),

    path('signing/', signing_demo, name='signing_demo'),
    path('signing-set/', signing_make_token, name='signing_set'),
    #signing_set_type
    path('signing-set-type/', signing_pack_payload, name='signing_set_type'),
    path('cookie-signing/', cookie_set_signed, name='cookie_set_signed'),

    path('mail/send/',test_email),
    path('mail/send/low/',send_low_code_email_v1),
    path('mail/send/file/', send_low_code_email_v2),
    path('mail/send/html/', send_low_code_email_v3),
    path('mail/send/many/', send_many_emails),
    path('mail/send/admins/', notify_admins),
    path('mail/send/contact/', contact_form),
    path('verify/<str:token>/', verify_token),


    path('signing/list/', signing_list_demo, name='signing_list_demo'),

    path('api/rubrics/',api_rubrics, name='api_rubrics'),
    path('api/rubrics/<int:pk>/',api_rubric_detail, name='api_rubric_detail'),
    path('api/ads/',api_ads, name='api_ads'),
    path('api/ads/<int:pk>/', api_ad_detail, name='api_ad_detail'),
    path("api/csrf/", csrf_probe)
]


