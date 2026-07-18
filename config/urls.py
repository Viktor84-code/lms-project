from django.contrib import admin
from django.shortcuts import redirect
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("lms.urls")),
    path("", lambda request: redirect("api/", permanent=False)),
    path("users/", include("users.urls")),
]
