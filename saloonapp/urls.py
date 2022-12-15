from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    path('admin/', admin.site.urls, name='admin-view'),
    path('', views.index, name='main-view'),
    path('notes/', views.notes, name='notes-view'),
    path('__debug__/', include('debug_toolbar.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
