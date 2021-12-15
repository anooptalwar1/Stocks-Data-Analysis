from django.http import HttpResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularJSONAPIView

urlpatterns = [
    path("api/health", lambda r: HttpResponse(status=200, content="I'm alive!")),
    path("api/reporting/", include("reporting.urls")),
    path("api/docs/openapi", SpectacularAPIView.as_view(), name="openapi-schema"),
    path(
        "api/docs",
        SpectacularRedocView.as_view(url_name="openapi-schema", template_name="redoc.html"),
        name="redoc",
    ),
]
