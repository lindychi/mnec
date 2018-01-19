from django.db import models

# Create your models here.
from django.urls import reverse


class Todo(models.Model):
    owner = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    daily = models.BooleanField()
    daily_page = models.TextField()
    complete = models.BooleanField()

    def __str__(self):
        if self.end_date is self.created_date:
            return "["+str(self.created_date)+" ~ "+str(self.end_date)+"] "+self.title
        else:
            return "["+str(self.created_date)+" ~ ] "+self.title

    def get_absolute_url(self):
        return reverse('todo_view', args=(self.owner.username, self.title, ))
        
