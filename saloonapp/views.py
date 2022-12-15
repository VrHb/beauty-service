from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Saloon
from .models import Service
from .models import Master
from .models import Note
from .serializers import ServicesSerializer
from .utils import construct_calendar_by_filters


def index(request):
    context = {
        'saloons': Saloon.objects.all(),
        'services': Service.objects.all(),
        'masters': Master.objects.select_related('speciality').all(),
    }
    return render(request, template_name='index.html', context=context)


@login_required
def notes(request):
    user = request.user
    notes = Note.objects.select_related('saloon', 'service', 'master', 'payment', 'promo').filter(user=user)
    active_notes = notes.filter(date__gt=datetime.now())
    past_notes = notes.filter(date__lt=datetime.now())
    total_price = Decimal(0)
    payment_ids = []
    for note in notes:
        total_price += note.payment.get_total_price()
        payment_ids.append(str(note.payment.pk))
    context = {
        'active_notes': active_notes,
        'past_notes': past_notes,
        'total': {
            'price': total_price,
            'payments': ','.join(payment_ids)
        }
    }
    return render(request, template_name='notes.html', context=context)


@api_view(['GET'])
def services(request: Request):
    serializer = ServicesSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    calendar = construct_calendar_by_filters(
        serializer.validated_data['date'],
        serializer.validated_data.get('saloon', None),
        serializer.validated_data.get('master', None),
        serializer.validated_data.get('service', None),
    )
    return Response(calendar)
