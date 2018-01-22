"""import Testcase."""
from django.test import TestCase
from nec_calendar.classes.calendar import Calendar, Day


# Create your tests here.
class DayTest(TestCase):
    """Todo model testcase."""

    def test_day_init(self):
        """Test initialize day class."""
        day = Day("noday", 1, 2)
        self.assertEqual(day.get_day(), 0)
        self.assertEqual(day.get_month(), 1)
