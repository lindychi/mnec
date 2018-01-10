from django.db import models
from django.utils import timezone

# Create your models here.
class BucketList(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    text = models.TextField(null=True)
    created_date = models.DateTimeField(default=timezone.now)
    deadline_date = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return "[" + str(self.author) + "]" + self.title

class MoneyUnit(models.Model):
    author = models.ForeignKey('auth.User')
    category = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    text = models.TextField(null=True)
    balance = models.IntegerField()
    created_date = models.DateTimeField(blank=False, null=False)
    def __str__(self):
        return "[" + str(self.author) + "][" + self.category + "]" + self.title

class TodoUnit(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        if self.end_date is self.created_date:
            return "["+str(self.created_date)+" ~ "+str(self.end_date)+"] "+self.title
        else:
            return "["+str(self.created_date)+" ~ ] "+self.title
