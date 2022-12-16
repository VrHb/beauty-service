from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.index, name='main-view'),
    path('logout/', views.logout_user, name='logout'),
    path('notes/', views.notes, name='notes-view'),
    path('service/', views.services, name='service'),
    path('get_free_timeslots/', views.get_free_timeslots, name='get_free_timeslots-api'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
