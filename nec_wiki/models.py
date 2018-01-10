from django.db import models
import markdown

# Create your models here.
class Page(models.Model):
    owner = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
