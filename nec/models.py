from django.db import models
from django.utils import timezone

# Create your models here.
class BucketList(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    deadline_date = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return self.title
