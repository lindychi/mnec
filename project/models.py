from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model

# Create your models here.
class Project(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created_date = models.DateTimeField(default=timezone.now)
    update_date = models.DateTimeField(blank=True, null=True)
    todo = models.ForeignKey('ProjectTodo', null=True, default=None, on_delete=models.CASCADE, related_name='todo_list')

    def __str__(self):
        return self.title

class ProjectTodo(models.Model):
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255)
    detail = models.TextField(null=True, blank=True, default="")
    depth = models.IntegerField(default=0, null=False, blank=False)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='child', on_delete=models.SET_NULL)
    is_clear = models.BooleanField(default=False)
    clear_date = models.DateTimeField(default=None, null=True)
    priority = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + " " + self.title + " (" + str(self.depth) + ")"
