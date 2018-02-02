from django.forms import ModelForm, widgets
from .models import Money


class MoneyForm(ModelForm):
    class Meta:
        model = Money
        fields = ['bank', 'category', 'title', 'text', 'balance']