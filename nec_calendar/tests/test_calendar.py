from django.test import TestCase
from nec_calendar.classes.calendar import Calendar
from nec_calendar.classes.day import Day


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
        self.assertEqual(c.get_first_day(), 0)

    def test_dup_date(self):
        c = Calendar(2018, 1)
        c.add_event('2018-1-10 01:00:00', '2018-1-11 00:00:00',
                    'first', '/wiki/first')
        c.add_event('2018-1-8 00:00:00', '2018-1-13 00:00:00',
                    'second', '/wiki/second')
        c.add_event('2018-1-6 00:00:00', '2018-1-11 00:00:00',
                    'third', '/wiki/third')
        c.add_event('2018-1-11 00:00:00', '2018-1-15 00:00:00',
                    'fourth', '/wiki/fourth')
        c.add_event('2019-1-13 00:00:00', '2018-1-16 00:00:00',
                    'fifth', '/wiki/fifth')

        self.assertEqual(c.get_day(6).get_event(0), None)
        self.assertEqual(c.get_day(6).get_event(1), None)
        self.assertEqual(c.get_day(6).get_event(2).get_title(), 'third')

        self.assertEqual(c.get_day(8).get_event(0), None)
        self.assertEqual(c.get_day(8).get_event(1).get_title(), 'second')
        self.assertEqual(c.get_day(8).get_event(2).get_title(), 'third')

        self.assertEqual(c.get_day(10).get_event(0).get_title(), 'first')
        self.assertEqual(c.get_day(10).get_event(1).get_title(), 'second')
        self.assertEqual(c.get_day(10).get_event(2).get_title(), 'third')

        self.assertEqual(c.get_day(11).get_event(0).get_title(), 'first')
        self.assertEqual(c.get_day(11).get_event(1).get_title(), 'second')
        self.assertEqual(c.get_day(11).get_event(2).get_title(), 'third')
        self.assertEqual(c.get_day(11).get_event(3).get_title(), 'fourth')

        self.assertEqual(c.get_day(12).get_event(0), None)
        self.assertEqual(c.get_day(12).get_event(1).get_title(), 'second')
        self.assertEqual(c.get_day(12).get_event(2), None)
        self.assertEqual(c.get_day(12).get_event(3).get_title(), 'fourth')

        self.assertEqual(c.get_day(13).get_event(0).get_title(), 'fifth')
        self.assertEqual(c.get_day(13).get_event(1).get_title(), 'second')
        self.assertEqual(c.get_day(13).get_event(2), None)
        self.assertEqual(c.get_day(13).get_event(3).get_title(), 'fourth')

        self.assertEqual(c.get_day(14).get_event(0).get_title(), 'fifth')
        self.assertEqual(c.get_day(14).get_event(1), None)
        self.assertEqual(c.get_day(14).get_event(2), None)
        self.assertEqual(c.get_day(14).get_event(3).get_title(), 'fourth')
