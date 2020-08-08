from django import forms
from .models import ProjectTodo

class ProjectTodoForm(forms.ModelForm):
    class Meta:
        model = ProjectTodo
        fields = ['title', 'detail']