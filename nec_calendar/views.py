from django.shortcuts import render
from nec_calendar.classes.calendar import Calendar
from django.utils import timezone


# Create your views here.
def index(request):
    now = timezone.now()
    calendar = Calendar(now.year, now.month)
    return render(request, 'nec_calendar/index.html', {'calendar': calendar})
