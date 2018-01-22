"""For parse calendar html."""
import re
import calendar


class Day:
    """Unit of calendar.

    control each day data and print result
    """
    class_str = ""
    month = 1
    day = 1
    event = []

    def __init__(self, class_str, month, day):
        self.class_str = class_str
        self.month = int(month)
        self.day = int(day)
        self.event = []

        if self.class_str == "noday":
            self.day = 0

    def get_day(self):
        return self.day

    def get_month(self):
        return self.month

class Calendar:
    """Print calendar html with other classes."""

    first_day = 0
    token_list = ()
    calendar_array = []

    def __init__(self, year, month):
        """Parse html and Build Array.

        html: The calendar for that month is entered in the form of a table.

        After parsing the html, it arranges the data and stores the size.
        """
        self.year = year
        self.month = month
        calendar_with_6 = calendar.HTMLCalendar(firstweekday=6)
        calendar_set_day = calendar_with_6.formatmonth(theyear=year,
                                                       themonth=month)

        raw_html_table = re.compile(r"""<td\sclass="
                                    ([^\"]+)         #class name
                                    ">
                                    ([^\<]+)         #day value
                                    </td>""", re.VERBOSE)
        self.token_list = raw_html_table.findall(calendar_set_day)
        self.list_to_array()

    def get_size(self):
        """Return Array size."""
        return len(self.token_list)

    def set_event(self, start_date, end_date, title, url):
        return True

    def list_to_array(self):
        """Make array from token list."""
        calendar_array = []
        for token_class, token_value in self.token_list:
            if token_class is "noday":
                token_value = ""
            if token_value is "1":
                self.first_day = len(calendar_array)
            calendar_array.append([token_class, token_value, []])

    def get_first_day(self):
        return self.first_day
