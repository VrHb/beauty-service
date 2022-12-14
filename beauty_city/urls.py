from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls, name='admin-view'),
    path("", include("saloonapp.urls")),
    path('__debug__/', include('debug_toolbar.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path("", include('django.contrib.auth.urls')),
]


