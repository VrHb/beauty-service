from django_filters import rest_framework as filters

from .models import Master
from .models import Saloon
from .models import Service
from .models import ServiceGroup


class MasterFilter(filters.FilterSet):
    saloon = filters.NumberFilter(field_name='saloonlinks__saloon__pk', label='saloon')
    service = filters.NumberFilter(field_name='services__pk', label='service')

    class Meta:
        model = Master
        fields = ['saloon', 'service']


class SaloonFilter(filters.FilterSet):
    master = filters.NumberFilter(field_name='masters__pk', label='master')
    service = filters.NumberFilter(field_name='masters__services__pk', label='service')

    class Meta:
        model = Saloon
        fields = ['master', 'service']


class ServiceFilter(filters.FilterSet):
    master = filters.NumberFilter(field_name='masters__pk', label='master')
    saloon = filters.NumberFilter(field_name='masters__saloonlinks__saloon__pk', label='saloon')

    class Meta:
        model = Service
        fields = ['master', 'saloon']


class ServiceGroupFilter(filters.FilterSet):
    master = filters.NumberFilter(field_name='services__masters__pk', label='master')
    saloon = filters.NumberFilter(field_name='services__masters__saloonlinks__saloon__pk', label='saloon')

    class Meta:
        model = ServiceGroup
        fields = ['master', 'saloon']
