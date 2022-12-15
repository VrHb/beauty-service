from django.contrib import admin

from .models import Saloon
from .models import Service
from .models import ServiceGroup
from .models import Master
from .models import MasterSpeciality
from .models import Payment
from .models import PaymentType
from .models import Promo
from .models import SaloonMaster
from .models import SaloonMasterWeekday
from .models import Note


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


@admin.register(PaymentType)
class PaymentTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    pass


class SaloonMasterWeekdayInline(admin.TabularInline):
    model = SaloonMasterWeekday


@admin.register(SaloonMaster)
class SaloonMasterAdmin(admin.ModelAdmin):
    inlines = [SaloonMasterWeekdayInline]


@admin.register(SaloonMasterWeekday)
class SaloonMasterWeekdayAdmin(admin.ModelAdmin):
    pass


@admin.register(Note)
class MasterSpecialityAdmin(admin.ModelAdmin):
    pass
