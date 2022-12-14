from django.contrib import admin

from .models import Saloon, Service, ServiceGroup, Master, MasterSpeciality


@admin.register(Saloon)
class SalonAdmin(admin.ModelAdmin):
    pass


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceGroup)
class ServiceGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass


@admin.register(MasterSpeciality)
class MasterSpecialityAdmin(admin.ModelAdmin):
    pass
