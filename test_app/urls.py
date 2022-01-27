from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("zerozero/api/", include("zerozero.api_urls")),
    path("", include("zerozero.urls")),
]
