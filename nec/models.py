"""Get db models."""
from django.db import models
from django.utils import timezone


# Create your models here.
class BucketList(models.Model):
    """Start with BucketList. but now we do not use it."""

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=1024)
    text = models.TextField(null=True)
    created_date = models.DateTimeField()
    deadline_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        """Bucketlist to string.

        [ <author> ] title.
        """
        return "[" + str(self.author) + "]" + self.title


class MoneyUnit(models.Model):
    """For my account book."""

    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    category = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    text = models.TextField(null=True)
    balance = models.IntegerField()
    created_date = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        """Moneyunit to string.

        [ <author> ][ <category> ] title.
        """
        return "[" + str(self.author) + "][" + self.category + "]" + self.title
