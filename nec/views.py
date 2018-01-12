from django.shortcuts import render, redirect
from django.utils import timezone
from django.conf import settings
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse


def dashboard(request):
    if request.user.is_authenticated:
        bucketlists = BucketList.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        todolists = TodoUnit.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        return render(request, 'nec/dashboard.html', {'bucketlists':bucketlists, 'todolists':todolists})
    else:
        return redirect(settings.LOGIN_URL)


def bank(request):
    if request.user.is_authenticated:
        money_unit_lists = MoneyUnit.objects.filter(created_date__lte=timezone.now()).order_by('-created_date')
        return render(request, 'nec/bank.html', {'money_unit_lists':money_unit_lists})
    else:
        return redirect(settings.LOGIN_URL)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse("dashboard"))
    else:
        form = UserCreationForm()
    return render(request, 'nec/signup.html', {'form': form})