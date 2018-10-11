from django.forms import ModelForm, Textarea
from .models import Money, Bank


class MoneyForm(ModelForm):
    #bank = forms.ChoiceField(choices=[(bank.uid, bank.name) for bank in Bank.objects.filter()])
    class Meta:
        model = Money
        fields = ['created_date', 'bank', 'category', 'title', 'text', 'balance',]
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20, 'class': 'materialize-textarea'}),
        }

    def __init__(self, owner, *args, **kwargs):
        super(MoneyForm, self).__init__(*args, **kwargs)
        self.fields['bank'].queryset = Bank.objects.filter(owner=owner)

class BankForm(ModelForm):
    class Meta:
        model = Bank
        fields = ['name']
        widgets = {
            'text': Textarea(attrs={'cols': 80, 'rows': 20, 'class': 'materialize-textarea'})
        }
