from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from .models import *
from nec_todo.models import Todo

def dashboard(request):
    if request.user.is_authenticated:
        bucketlists = BucketList.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        todolists = Todo.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        return render(request, 'nec/dashboard.html', {'bucketlists':bucketlists, 'todolists':todolists})
    else:
        return redirect(settings.LOGIN_URL)

def bank(request):
    if request.user.is_authenticated:
        money_unit_lists = MoneyUnit.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        return render(request, 'nec/bank.html', {'money_unit_lists':money_unit_lists})
    else:
        return redirect(settings.LOGIN_URL)
