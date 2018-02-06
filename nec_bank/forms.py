from django.forms import ModelForm, Textarea
from .models import Money


class MoneyForm(ModelForm):\

    class Meta:
        model = Money
        fields = ['created_date', 'bank', 'category', 'title', 'text', 'balance']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20, 'class': 'materialize-textarea'})
        }
