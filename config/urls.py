from allauth.account.views import confirm_email
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from two_factor.urls import urlpatterns as tf_urls

from djangodemoprojectcokkiecuter.users import views
from djangodemoprojectcokkiecuter.users.views import *
from djangodemoprojectcokkiecuter.users.views import EmailVerificationRedirectView


def trigger_error(request):
    try:
        division_by_zero = 1 / 0
    except:
        division_by_zero = "Hello World"

    return HttpResponse(division_by_zero)


urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "api/v1/users/",
        include("djangodemoprojectcokkiecuter.users.urls", namespace="users"),
    ),
    path("accounts/", include("allauth.urls"), name="accouts"),
    path("sentry-debug/", trigger_error),
    path("registeration/", register, name="regiser_here"),
    path("loginnew/", views.loginnew, name="login_view"),
    path("otplogin/", views.otplogin, name="otp_login"),
    path("otp/", views.otp, name="otp"),
    path("", include(tf_urls)),
    # Your stuff: custom urls i  ncludes go here
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/v1/", include("config.api_router")),
    # DRF auth token
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    re_path(
        "api/v1/accounts-rest/registration/account-confirm-email/(?P<key>.+)/$",
        confirm_email,
        name="account_confirm_email",
    ),
    path("auth-token/", obtain_auth_token),
    path("api/v1/email-verification-redirect/", EmailVerificationRedirectView),
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/v1/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("api/v1/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/v1/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/v1/o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
