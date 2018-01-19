from django.forms import ModelForm, widgets
from .models import Page, Tag


class PageForm(ModelForm):
    class Meta:
        model = Page
        fields = ['title', 'content', 'tags']


class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
