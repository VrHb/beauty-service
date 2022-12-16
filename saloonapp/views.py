from datetime import datetime
from decimal import Decimal

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import render, redirect

from .models import Saloon
from .models import Service
from .models import Master
from .models import Note


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
