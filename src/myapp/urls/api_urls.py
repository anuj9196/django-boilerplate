from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

auth_urlpatterns = [
    # Endpoints providing custom views provided by `authentication` application
    path('', include('authentication.urls')),

    # Endpoints provided by `rest_auth` package
    path('', include('dj_rest_auth.urls')),

    # path('social-account-connection-temp/', TemplateView.as_view(), name='socialaccount_connections'),

    # path('confirm/', VerifyEmailView.as_view(), name='account_email_verification_sent'),

    # Endpoints used for user registration provided by `rest_auth` package
    path('register/', include('dj_rest_auth.registration.urls')),

    # This URL will be sent in the verification email to verify email
    path('register/verify-email/<key>', TemplateView.as_view(), name='account_confirm_email'),

    # This endpoint is used to generate password reset link in email content
    # The website URL is taken from Sites module which can be customized from the admin panel
    path('password/reset/confirm/<uidb64>/<token>', TemplateView.as_view(), name='password_reset_confirm'),
]


"""
Api endpoints for the other applications
"""
api_endpoints = [
    # path('plans/', include('plans.urls')),
    # # path('campaigns/', include('campaigns.urls')),
    # path('qr/', include('qr_manager.urls')),
    # path('lead/', include('lead_generation.urls')),
    # path('custom-domain/', include('custom_domain.urls')),
    # path('multi-users/', include('multi_users.urls')),
    # path('payment/', include('payments.urls')),
    # path('media/', include('user_media.urls')),
    # path('webhook/', include('webhook_integration.urls')),
    # path('tracking/', include('tracking.urls')),
    # path('event-tracking/', include('event_tracking.urls')),
    # path('scan-data/', include('scan_data_collect.urls')),
    # path('qr-assets/', include('qr_assets.urls')),
    # path('analytics/', include('analytics.urls')),
    # path('notification/', include('notification.urls')),
    # path('security/', include('security.urls')),
    # path('utils/', include('utils.urls')),
]

"""
Include all endpoints to `urlpatterns`. Only the path defined in the `urlpatterns` will be served.
Those which are not included in the `urlpatterns` list will be discarded and will not be served.
"""
urlpatterns = [
    path('auth/', include(auth_urlpatterns)),
    path('', include(api_endpoints))
]


# Add media url
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Add static url
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
