from django.db import models
import markdown

class Tag(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey('auth.User')
    def __str__(self):
        return self.owner.username + " - " + self.name

class Page(models.Model):
    owner = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag)
    def __str__(self):
        return self.owner.username + " - " + self.title

    def setTags(self, tag_string):
        if tag_string.lstrip().rstrip():
            tag_list = [Tag.objects.get_or_create(name=tag.rstrip().lstrip('#'), owner=self.owner)[0] for tag in tag_string.lstrip(' #').split('#')]
            self.tags.clear()
            for tag in tag_list:
                self.tags.add(tag)
