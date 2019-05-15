"""Django shortcuts."""
from django.shortcuts import render, redirect
import datetime
from django.conf import settings
from .models import MoneyUnit, BucketList
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.urls import reverse
from nec_todo.models import Todo


def dashboard(request):
    if request.user.is_authenticated:
        return redirect(reverse('todo_index'))
    # if request.user.is_authenticated:
    #     bucketlists = BucketList.objects.filter(
    #         author=request.user,
    #         created_date__lte=datetime.datetime.now()).order_by('-created_date')
    #     todolists = Todo.objects.filter(
    #         owner=request.user,
    #         created_date__lte=datetime.datetime.now()).order_by('-created_date')
    #     return render(request, 'nec/dashboard.html',
    #                   {'bucketlists': bucketlists, 'todolists': todolists})
    else:
        return redirect(settings.LOGIN_URL)


def bank(request):
    if request.user.is_authenticated:
        money_unit_lists = MoneyUnit.objects.filter(
            created_date__lte=datetime.datetime.now()).order_by('-created_date')
        return render(request, 'nec/bank.html',
                      {'money_unit_lists': money_unit_lists})
    else:
        return redirect(settings.LOGIN_URL)


def signup(request):
    return redirect(settings.LOGIN_URL)
    # if request.method == 'POST':
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         username = form.cleaned_data.get('username')
    #         raw_password = form.cleaned_data.get('password1')
    #         user = authenticate(username=username, password=raw_password)
    #         login(request, user)
    #         return redirect(reverse("dashboard"))
    # else:
    #     form = UserCreationForm()
    # return render(request, 'nec/signup.html', {'form': form})
