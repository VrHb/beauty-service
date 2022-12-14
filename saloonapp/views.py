from django.shortcuts import render

from .models import Saloon
from .models import Service
from .models import Master


def index(request):
    context = {
        'saloons': Saloon.objects.all(),
        'services': Service.objects.all(),
        'masters': Master.objects.all(),
    }
    return render(request, template_name='index.html', context=context)
