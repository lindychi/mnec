"""use admin site."""
from django.contrib import admin
from .models import BucketList, MoneyUnit

# Register your models here.
admin.site.register(BucketList)
admin.site.register(MoneyUnit)
