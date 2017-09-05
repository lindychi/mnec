from django.shortcuts import render
from django.utils import timezone
from .models import *

def dashboard(request):
    bucketlists = BucketList.objects.filter(created_date__lte=timezone.now()).order_by('created_date')
    return render(request, 'nec/dashboard.html', {'bucketlists':bucketlists})
