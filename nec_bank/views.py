from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from .forms import MoneyForm, BankForm
from .models import Money, Bank


# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def index(request, bank_id=""):
    bank_list = Bank.objects.filter(owner=request.user).order_by('name')
    if (bank_id==""):
        money_list = Money.objects.filter(owner=request.user).order_by('-created_date')
    else:
        money_list = Money.objects.filter(owner=request.user,bank_id=int(bank_id)).order_by('-created_date')
    return render(request, 'nec_bank/index.html', {'bank_list':bank_list, 'money_list':money_list})


@login_required(login_url=settings.LOGIN_URL)
def create_money(request):
    """Create money object."""
    if request.method == 'POST':
        form = MoneyForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            money = form.save(commit=False)
            money.owner = request.user
            money.save()
            return redirect(money)
        else:
            return render(request, 'nec_bank/create_money.html', {'money_form': form})
    else:
        request.GET._mutable = True
        request.GET['created_date'] = timezone.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')
        request.GET._mutable = False
        form = MoneyForm(request.user, request.GET)
        return render(request, 'nec_bank/create_money.html', {'money_form': form})


def view_money(request, money_id):
    money = Money.objects.get(id=money_id)
    return render(request, 'nec_bank/view_money.html', {'money': money});


@login_required(login_url=settings.LOGIN_URL)
def edit_money(request, money_id):
    """Edit money content.

    when edit money, search with money_id.
    money_name is not unique.
    """
    money = get_object_or_404(Money, id=money_id)
    if request.method == 'POST':
        form = MoneyForm(request.POST, request.FILES, instance=money)
        if form.is_valid():
            money = form.save()
            return redirect(money)
        else:
            return render(request, 'nec_bank/edit_money.html',
                          {'money': money, 'money_form': form})

    else:
        form = MoneyForm(instance=money)
        return render(request, 'nec_bank/edit_money.html',
                      {'money': money, 'money_form': form})


@login_required(login_url=settings.LOGIN_URL)
def delete_money(request, money_id):
    """Delete money object."""
    money = Money.objects.get(id=int(money_id), owner=request.user)
    title = money.title
    money.delete()
    return redirect(reverse('money_view',
                            args=(request.user.username, title, )))



@login_required(login_url=settings.LOGIN_URL)
def create_bank(request):
    """Create bank object."""
    if request.method == 'POST':
        form = BankForm(request.POST, request.FILES)
        if form.is_valid():
            bank = form.save(commit=False)
            bank.owner = request.user
            bank.save()
            return redirect(bank)
        else:
            return render(request, 'nec_bank/create_bank.html', {'bank_form': form})
    else:
        request.GET._mutable = True
        request.GET['created_date'] = timezone.now().astimezone().strftime('%Y-%m-%d %H:%M:%S')
        request.GET._mutable = False
        form = BankForm(request.GET)
        return render(request, 'nec_bank/create_bank.html', {'bank_form': form})


@login_required(login_url=settings.LOGIN_URL)
def view_bank(request, bank_id):
    bank = Bank.objects.get(id=bank_id, owner=request.user)
    return render(request, 'nec_bank/view_bank.html', {'bank': bank});


@login_required(login_url=settings.LOGIN_URL)
def edit_bank(request, bank_id):
    """Edit bank content.

    when edit bank, search with bank_id.
    bank_name is not unique.
    """
    bank = get_object_or_404(Bank, id=bank_id)
    if request.method == 'POST':
        form = BankForm(request.POST, request.FILES, instance=bank)
        if form.is_valid():
            bank = form.save()
            return redirect(bank)
        else:
            return render(request, 'nec_bank/edit_bank.html',
                          {'bank': bank, 'bank_form': form})

    else:
        form = BankForm(instance=bank)
        return render(request, 'nec_bank/edit_bank.html',
                      {'bank': bank, 'bank_form': form})


@login_required(login_url=settings.LOGIN_URL)
def delete_bank(request, bank_id):
    """Delete bank object."""
    bank = Bank.objects.get(id=int(bank_id), owner=request.user)
    title = Bank.name
    bank.delete()
    return redirect(reverse('bank_view',
                            args=(request.user.username, title, )))
