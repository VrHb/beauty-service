import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.core.handlers.wsgi import WSGIRequest
from django.db import transaction
from django.db.models import Count
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from .filters import MasterFilter
from .filters import SaloonFilter
from .filters import ServiceFilter
from .filters import ServiceGroupFilter
from .forms import SignUpUser
from .models import Note
from .models import Payment
from .models import Promo
from .models import Master
from .models import Saloon
from .models import SaloonMasterWeekday
from .models import ServiceGroup
from .models import Service
from .serializers import BlockedTimeSerializer
from .serializers import NoteGetSerializer
from .serializers import NotePostSerializer
from .serializers import PaymentSerializer
from .serializers import PromoSerializer
from .serializers import SaloonSerializer
from .serializers import ServiceSerializer
from .serializers import ServiceGroupSerializer
from .serializers import ServiceSpecialPriceSerializer
from .serializers import MasterSerializer


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


@login_required(login_url='login')
def notes(request):
    user = request.user
    notes = Note.objects.with_dt().select_related(
        'saloon', 'service', 'master', 'payment', 'promo'
    ).filter(user=user, payment__isnull=False).order_by('-dt')
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
def get_blocked_timeslots(request: Request):
    serializer = BlockedTimeSerializer(data=request.query_params)
    serializer.is_valid(raise_exception=True)
    timeslots = [f'{t}:00' for t in range(10, 21)]

    # На прошлое записей нет
    if serializer.validated_data['date'] < timezone.now().date():
        return Response(timeslots)

    # составим фильтры для записей и для рабочих дней мастеров в салонах
    # если у записи нет платежа, то она еще не подтверждена и это время свободно
    note_filters = {'date': serializer.validated_data['date'], 'payment__isnull': False}
    saloon_master_filters = {'isoweekday': note_filters['date'].isoweekday()}
    for key in ['saloon', 'service', 'master']:
        if key in serializer.validated_data:
            note_filters[f'{key}__pk'] = serializer.validated_data[key]
            if key == 'service':
                saloon_master_filters['saloonmaster__master__services__pk__in'] = [serializer.validated_data[key]]
            else:
                saloon_master_filters[f'saloonmaster__{key}__pk'] = serializer.validated_data[key]

    # если нет рабочих дней у мастеров в салонах по фильтрам, то все занято
    saloon_master_day_items = SaloonMasterWeekday.objects.filter(**saloon_master_filters)
    if not saloon_master_day_items:
        return Response(timeslots)

    # если среди фильтров только дата, то пользователь все равно
    # еще будет делать выбор, поэтому отдадим, что все свободно
    if len(note_filters.keys()) == 1:
        return Response([])

    # если нет записей по фильтрам, то все свободно
    note_stimes = Note.objects.filter(**note_filters)
    if not note_stimes:
        return Response([])

    # составляем комбинации [салон, мастер(в котором работает мастер)]
    # услуга в комбинациях не нужна, т.к. мастер не может делать 2 услуги одновременно,
    # но по услуге проверятся, что он вообще делает выбранную или любую, если не выбрана
    combs = set()
    for saloon_master_day_item in saloon_master_day_items:
        saloon_pk = saloon_master_day_item.saloonmaster.saloon.pk
        master_pk = saloon_master_day_item.saloonmaster.master.pk
        services = saloon_master_day_item.saloonmaster.master.services.all()
        if 'service__pk' in note_filters:
            services = services.filter(pk=note_filters['service__pk'])
        if services:
            combs.add((saloon_pk, master_pk))

    # и дальше проверяем по каждому часу, если записей на этот час больше
    # или равно числу возможных комбинаций, то это время занято
    blocked_times = []
    note_stimes = note_stimes.values('stime').annotate(cnt=Count('stime'))
    for note_stime in note_stimes:
        if note_stime['cnt'] >= len(combs):
            time_in_hour_minute_format = str(note_stime['stime'])[:-3]
            blocked_times.append(time_in_hour_minute_format)

    # добавим прошедшие на сегодня времена
    is_today = serializer.validated_data['date'] == timezone.now().date()
    if is_today:
        for timeslot in timeslots:
            not_added_yet = timeslot not in blocked_times
            time_past = datetime.time.fromisoformat(timeslot) <= timezone.now().time()
            if not_added_yet and time_past:
                blocked_times.append(timeslot)

    return Response(blocked_times)


def logout_user(request):
    logout(request)
    return redirect('main-view')


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('service')
        else:
            messages.success(request, 'Неправильный логин или пароль, попробуйте еще!')
    return render(request, 'login.html', {})


@login_required(login_url='login')
def service(request):
    return render(request, 'service.html', {})


@login_required(login_url='login')
def service_finally(request: WSGIRequest):
    note_pk = request.COOKIES.get('note_pk', '')
    if not note_pk:
        return redirect('service')
    note = Note.objects.get(pk=note_pk)
    # ищем, нет ли такой же записи, но уже подтвержденной
    same_booked_note = Note.objects.filter(
        date=note.date, stime=note.stime, master=note.master, payment__isnull=False)
    if same_booked_note:
        # TODO: редирект на отдельную страницу тип "извините, уже кто-то другой записался"
        return redirect('service')
    if request.method == 'GET':
        return render(request, 'serviceFinally.html', {'note': note})
    with transaction.atomic():
        payment = Payment.objects.create(
            user=note.user,
            status=Payment.Status.created
        )
        note.payment = payment
        note.save()
        request.COOKIES['note_pk'] = ''
    return redirect('notes-view')


def register_user(request):
    if request.method == 'POST':
        form = SignUpUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "Вы зарегистрировались!")
            return redirect('notes-view')
    else:
        form = SignUpUser()
    return render(request, 'registration.html', {'form': form})


class SaloonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Saloon.objects.all()
    serializer_class = SaloonSerializer
    filterset_class = SaloonFilter


class ServiceGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ServiceGroup.objects.prefetch_related('services').order_by('order').distinct()
    serializer_class = ServiceGroupSerializer
    filterset_class = ServiceGroupFilter


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSpecialPriceSerializer
    filterset_class = ServiceFilter

    def get_serializer_context(self):
        """Adds request to the context of serializer"""
        if self.request.user.is_anonymous:
            has_notes = False
        else:
            has_notes = self.request.user.notes.filter(payment__isnull=True).count() > 0
        return {'has_notes': has_notes}


class MasterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Master.objects.select_related('speciality').prefetch_related('services').all()
    serializer_class = MasterSerializer
    filterset_class = MasterFilter


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('user', 'ptype').all()
    serializer_class = PaymentSerializer


class PromoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.select_related().all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return NotePostSerializer
        return NoteGetSerializer
