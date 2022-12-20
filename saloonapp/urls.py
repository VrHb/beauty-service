from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('saloons', views.SaloonViewSet)
router.register('services', views.ServiceViewSet, basename='Service')
router.register('service_groups', views.ServiceGroupViewSet)
router.register('masters', views.MasterViewSet)
router.register('payments', views.PaymentViewSet)
router.register('promos', views.PromoViewSet)
router.register('notes-api', views.NoteViewSet)

urlpatterns = [
    path('', views.index, name='main-view'),
    path('', include(router.urls)),
    path('logout/', views.logout_user, name='logout'),
    path('login/', views.login_user, name='login-view'),
    path('registration/', views.register_user, name='registration'),
    path('notes/', views.notes, name='notes-view'),
    path('get_blocked_timeslots/', views.get_blocked_timeslots, name='get_blocked_timeslots-api'),
    path('service/', views.service, name='service'),
    path('service-finally/', views.service_finally, name='service_finally'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
