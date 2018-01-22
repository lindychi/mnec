from django.test import TestCase
from nec_calendar.classes.calendar import Calendar


# Create your tests here.
class CalendarTest(TestCase):
    """Todo model testcase."""

    c = None

    def test_generate(self):
        """Test initialize calendar and build calendar."""
        c = Calendar(2018, 1)
        self.assertEqual(c.get_size(), 35)

    def test_get_first_day(self):
        c = Calendar(2018, 1)
        self.assertEqual(c.get_first_day(), 1)

    def test_dup_date(self):
        c = Calendar(2018, 1)
