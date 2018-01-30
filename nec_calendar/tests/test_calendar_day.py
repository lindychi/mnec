"""import Testcase."""
from django.test import TestCase
from nec_calendar.classes.day import Day


# Create your tests here.
class DayTest(TestCase):
    """Todo model testcase."""

    def test_day_init(self):
        """Test initialize day class."""
        day = Day("noday", 2018, 1, 2)
        self.assertEqual(day.get_day(), 0)
        self.assertEqual(day.get_month(), 0)

        day = Day("mon", 2018, 1, 1)
        self.assertEqual(day.get_day(), 1)
        self.assertEqual(day.get_month(), 1)

        day = Day("mon", 2018, 1, 32)
        self.assertEqual(day.get_day(), 0)
        self.assertEqual(day.get_month(), 0)

        day = Day("mon", 2018, 13, 1)
        self.assertEqual(day.get_day(), 0)
        self.assertEqual(day.get_month(), 0)
