from django.shortcuts import render

from .models import Saloon
from .models import Service
from .models import Master
from .models import User 


def index(request):
    context = {
        'user': User.objects.get(id=1),
        'saloons': Saloon.objects.all(),
        'services': Service.objects.all(),
        'masters': Master.objects.select_related('speciality').all(),
    }
    return render(request, template_name='index.html', context=context)
