from django.test import TestCase
from nec_calendar.classes.calendar import Calendar
import calendar


# Create your tests here.
class CalendarTest(TestCase):
    """Todo model testcase."""

    def test_generate(self):
        """Test initialize calendar and build calendar."""
        calendar_with_6 = calendar.HTMLCalendar(firstweekday=6)
        calendar_set_day = calendar_with_6.formatmonth(theyear=2018,
                                                       themonth=1)
        c = Calendar(calendar_set_day)
        self.assertEqual(c.get_size(), 35)
