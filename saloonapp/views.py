from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import render, redirect


from .models import Saloon, ServiceGroup
from .models import Service
from .models import Master
from .models import Note
from .serializers import GetFreeTimeslotsSerializer
from .serializers import SaloonSerializer
from .serializers import ServiceSerializer
from .serializers import ServiceGroupSerializer
from .serializers import MasterSerializer
from .serializers import MasterSpecialitySerializer
from .utils import construct_calendar_by_filters


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('notes-view')
        else:
            messages.success(request, 'Непральвильный логин или пароль, попробуйте еще!')
    context = {
        'saloons': Saloon.objects.all(),
        'services': Service.objects.all(),
        'masters': Master.objects.select_related('speciality').all(),
    }
    return render(request, template_name='index.html', context=context)


@login_required
def notes(request):
    user = request.user
    notes = Note.objects.with_dt().select_related(
        'saloon', 'service', 'master', 'payment', 'promo').filter(user=user).order_by('-dt')
    active_notes = notes.filter(dt__gt=timezone.now())
    past_notes = notes.filter(dt__lte=timezone.now())
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
def get_free_timeslots(request: Request):
    serializer = ServicesSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)

    calendar = construct_calendar_by_filters(
        serializer.validated_data['date'],
        serializer.validated_data.get('saloon', None),
        serializer.validated_data.get('master', None),
        serializer.validated_data.get('service', None),
    )
    return Response(calendar)


def services(request):
    return render(request, 'service.html', {})


def logout_user(request):
    logout(request)
    return redirect('main-view')
class SaloonViewSet(viewsets.ModelViewSet):
    queryset = Saloon.objects.all()
    serializer_class = SaloonSerializer


class ServiceGroupViewSet(viewsets.ModelViewSet):
    queryset = ServiceGroup.objects.prefetch_related('services').order_by('order').distinct()
    serializer_class = ServiceGroupSerializer


class MasterViewSet(viewsets.ModelViewSet):
    queryset = Master.objects.select_related('speciality').prefetch_related('services').all()
    serializer_class = MasterSerializer


def service(request):
    return render(request, 'service.html', {})


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы зарегистрировались!")
            return reidrect('main-view')
    else:
        form = UserCreationForm()
    return render(request, 'registration.html', {'form': form})
