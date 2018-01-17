from django.forms import ModelForm, widgets
from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content', 'end_date']