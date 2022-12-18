import datetime

from django.contrib.auth import get_user_model
from rest_framework import serializers

from userapp.serializers import UserGetSerializer, UserPostSerializer
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


class BlockedTımeSerializer(serializers.Serializer):
    date = serializers.DateField()
    saloon = serializers.IntegerField(required=False)
    master = serializers.IntegerField(required=False)
    service = serializers.IntegerField(required=False)

    class Meta:
        fields = ['date', 'saloon', 'master', 'service']


class SaloonGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = ['pk', 'name', 'address']


class SaloonPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saloon
        fields = ['pk']


class ServiceGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['pk', 'name', 'price']


class ServicePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ['pk']


class ServiceGroupSerializer(serializers.ModelSerializer):
    services = ServiceGetSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceGroup
        fields = ['pk', 'name', 'services']


class MasterSpecialitySerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterSpeciality
        fields = ['pk', 'name']


class MasterGetSerializer(serializers.ModelSerializer):
    speciality = MasterSpecialitySerializer(read_only=True)
    services = ServiceGetSerializer(many=True, read_only=True)

    class Meta:
        model = Master
        fields = ['pk', 'full_name', 'avatar', 'speciality', 'services']


class MasterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = ['pk']


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = ['pk', 'name']


class PaymentGetSerializer(serializers.ModelSerializer):
    ptype = PaymentTypeSerializer()
    user = UserGetSerializer()

    class Meta:
        model = Payment
        fields = ['pk', 'user', 'created_at', 'paid_at', 'ptype', 'status']


class PaymentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['pk']


class PromoGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['pk', 'name', 'description', 'code', 'is_active', 'percent', 'absolute']


class PromoPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promo
        fields = ['pk']


class NoteGetSerializer(serializers.ModelSerializer):
    user = UserGetSerializer()
    saloon = SaloonGetSerializer()
    service = ServiceGetSerializer()
    master = MasterGetSerializer()
    payment = PaymentGetSerializer()
    promo = PromoGetSerializer()

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
