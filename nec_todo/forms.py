from django.forms import ModelForm, widgets, Textarea, TextInput
from .models import Todo


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'content', 'start_date', 'end_date', 'daily', 'daily_page']
