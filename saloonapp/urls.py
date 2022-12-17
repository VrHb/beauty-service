from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('saloons', views.SaloonViewSet)
router.register('service_groups', views.ServiceGroupViewSet)
router.register('masters', views.MasterViewSet)

urlpatterns = [
    path('', views.index, name='main-view'),
    path('', include(router.urls)),
    path('logout/', views.logout_user, name='logout'),
    path('registration/', views.register_user, name='registration'),
    path('notes/', views.notes, name='notes-view'),
    path('get_free_timeslots/', views.get_free_timeslots, name='get_free_timeslots-api'),
    path('service/', views.service, name='service'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
