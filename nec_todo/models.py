from django.db import models

# Create your models here.
class Todo(models.Model):
    owner = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True, auto_now=True)
    def __str__(self):
        if self.end_date is self.created_date:
            return "["+str(self.created_date)+" ~ "+str(self.end_date)+"] "+self.title
        else:
            return "["+str(self.created_date)+" ~ ] "+self.title
