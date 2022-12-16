from rest_framework import serializers

from .models import Master
from .models import MasterSpeciality
from .models import Saloon
from .models import Service
from .models import ServiceGroup


class GetFreeTimeslotsSerializer(serializers.Serializer):
    date = serializers.DateField()
    saloon = serializers.IntegerField(required=False)
    master = serializers.IntegerField(required=False)
    service = serializers.IntegerField(required=False)

    class Meta:
        fields = ['date', 'saloon', 'master', 'service']


class SaloonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = ['pk', 'name', 'address']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['pk', 'name', 'price']


class ServiceGroupSerializer(serializers.ModelSerializer):
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceGroup
        fields = ['pk', 'name', 'services']


class MasterSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSpeciality
        fields = ['pk', 'name']


class MasterSerializer(serializers.ModelSerializer):
    speciality = MasterSpecialitySerializer(read_only=True)
    services = ServiceSerializer(many=True, read_only=True)

    class Meta:
        model = Master
        fields = ['pk', 'full_name', 'avatar', 'speciality', 'services']
