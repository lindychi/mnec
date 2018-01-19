from django.test import TestCase
from .views import Calendar
import calendar


# Create your tests here.
class CalendarTest(TestCase):
    """Todo model testcase."""

    @classmethod
    def test_generate(self):
        html = calendar.HTMLCalendar(firstweekday=6).formatmonth(theyear=2018, themonth=1)
        c = Calendar(html)
        self.assertEquals(c.get_size(), 32)
