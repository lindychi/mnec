from django.test import TestCase
from nec_calendar.classes.calendar import Calendar
import calendar


# Create your tests here.
class CalendarTest(TestCase):
    """Todo model testcase."""

    def test_generate(self):
        """Test initialize calendar and build calendar."""
        c = Calendar(2018, 1)
        self.assertEqual(c.get_size(), 35)
