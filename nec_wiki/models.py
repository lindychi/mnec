from django.db import models
import markdown
from django.urls import reverse
import re


class Tag(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.owner.username + " - " + self.name

    def get_absolute_url(self):
        return reverse('wiki_view_tag', args=(self.owner.username, self.name, ))


class Page(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    todo_log = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    update_date = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.owner.username + " - " + self.title

    def setTags(self, tag_string):
        tag_list = []
        if tag_string.lstrip().rstrip():
            tag_list = [Tag.objects.get_or_create(name=tag.rstrip().lstrip('#'), owner=self.owner)[0] for tag in tag_string.lstrip(' #').split('#')]
        if self.tags and self.tags.count() > 0:
            self.tags.clear()
        for tag in tag_list:
            self.tags.add(tag)

    def save_form(self, form):
        self.title = form.cleaned_data['title']
        self.content = form.cleaned_data['content']
        self.setTags(form.cleaned_data['tags'])
        self.save()

    def getTags(self):
        tag_str = ""
        for tag in self.tags.all():
            tag_str = tag_str + tag.name
        return tag_str

    def get_absolute_url(self):
        return reverse('wiki_view_page', args=(self.title, ))

    def get_markdown_content(self):
        return markdown.markdown(re.sub(r"\n", "<br />", self.content))
