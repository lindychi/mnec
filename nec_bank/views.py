from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import MoneyForm
from .models import Money


# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def index(request):
    return render(request, 'nec_bank/index.html')


@login_required(login_url=settings.LOGIN_URL)
def create_money(request):
    """Create money object."""
    if request.method == 'POST':
        form = MoneyForm(request.POST, request.FILES)
        if form.is_valid():
            money = form.save(commit=False)
            money.owner = request.user
            money.save()
            return redirect(money)
        else:
            return render(request, 'nec_bank/create_money.html', {'money_form': form})
    else:
        form = MoneyForm(request.GET)
        return render(request, 'nec_bank/create_money.html', {'money_form': form})

def view_money(request, money_id):
    money = Money.objects.get(id=money_id)
    return render(request, 'nec_bank/view_money.html', {'money':money});