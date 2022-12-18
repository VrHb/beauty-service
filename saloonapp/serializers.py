import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from userapp.serializers import UserSerializer
from .models import Master
from .models import MasterSpeciality
from .models import Note
from .models import Payment
from .models import PaymentType
from .models import Promo
from .models import Saloon
from .models import Service
from .models import ServiceGroup

User = get_user_model()


class BlockedTimeSerializer(serializers.Serializer):
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


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['pk', 'name']


class PaymentSerializer(serializers.ModelSerializer):
    ptype = PaymentTypeSerializer()
    user = UserSerializer()

    class Meta:
        model = Payment
        fields = ['pk', 'user', 'created_at', 'paid_at', 'ptype', 'status']


class PromoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['pk', 'name', 'description', 'code', 'is_active', 'percent', 'absolute']


class NoteGetSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    saloon = SaloonSerializer()
    service = ServiceSerializer()
    master = MasterSerializer()
    payment = PaymentSerializer()
    promo = PromoSerializer()

    class Meta:
        model = Note
        fields = [
            'pk', 'user', 'saloon', 'service', 'master', 'payment',
            'price', 'promo', 'created_at', 'date', 'stime', 'etime'
        ]


class NotePostSerializer(serializers.ModelSerializer):
    # TODO: проверка записи на это время у этого мастера
    class Meta:
        model = Note
        fields = [
            'pk', 'user', 'saloon', 'service', 'master', 'payment',
            'price', 'promo', 'created_at', 'date', 'stime', 'etime'
        ]

    def create(self, validated_data):
        if 'etime' not in validated_data:
            minutes_in_hour = 60
            hour = validated_data['stime'].hour
            minute = validated_data['stime'].minute
            duration = validated_data['service'].duration_in_minutes
            minute += duration
            hour += minute // minutes_in_hour
            minute = minute % minutes_in_hour
            validated_data['etime'] = datetime.time(hour=hour, minute=minute)

        return super().create(validated_data)
