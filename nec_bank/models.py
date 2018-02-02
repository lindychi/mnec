from django.db import models


# Create your models here.
from django.urls import reverse


class Money(models.Model):
    """For my account book."""

    owner = models.ForeignKey('auth.User')
    bank = models.TextField()
    category = models.CharField(max_length=1024)
    title = models.CharField(max_length=1024)
    text = models.TextField(null=True)
    balance = models.IntegerField()
    created_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Moneyunit to string.

        [ <author> ][ <category> ] title.
        """
        return "[" + str(self.owner) + "][" + self.category + "]" + self.title

    def get_absolute_url(self):
        return reverse('bank_view_money', args=(self.id, ))