from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('lms.urls')),
    path('', lambda request: redirect('api/', permanent=False)),  # редирект с корня на API
]
