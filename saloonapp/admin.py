from django.contrib import admin

from .models import Saloon, Service, Master 


@admin.register(Saloon)
class SalonAdmin(admin.ModelAdmin):
    pass

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    pass

@admin.register(Master)
class MasterAdmin(admin.ModelAdmin):
    pass
