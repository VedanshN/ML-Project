from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/upload/', include('uploads.urls')),
    path('api/services/', include('services.urls')),
    ]