from django.forms import ModelForm, widgets
from .models import Page, Tag
from django import forms


class PageForm(forms.Form):
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    tags = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(PageForm, self).__init__(*args, **kwargs)
        if self.instance:
            self.initial['title'] = self.instance.title
            self.initial['content'] = self.instance.content
            self.initial['tags'] = self.instance.getTags()

class TagForm(ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
