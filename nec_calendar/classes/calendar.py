"""For parse calendar html."""
import re
import calendar
from .day import Day


class Calendar:
    """Print calendar html with other classes."""

    year = 0
    month = 0
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
        self.calendar_array = []
        for token_class, token_value in self.token_list:
            if token_class == "noday":
                token_value = "0"
            if token_value is "1":
                self.first_day = len(self.calendar_array) - 1
            self.calendar_array.append(Day(token_class,
                                       self.year,
                                       self.month,
                                       token_value))

    def add_event(self, start_date, end_date, title, url):
        start_token = re.findall(r'(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)',
                                 start_date)[0]
        end_token = re.findall(r'(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)',
                               end_date)[0]

        if int(start_token[1]) < self.month:
            start_token[2] = "1"
        elif int(start_token[1]) > self.month:
            return

        if int(end_token[1]) > self.month:
            end_token[2] = str(calendar.monthrange(self.year, self.month)[1])
        elif int(end_token[1]) < self.month:
            return

        available = False
        index = 0
        count = 0
        while not available:
            for i in range(int(start_token[2]), int(end_token[2]) + 1):
                if not self.calendar_array[self.first_day + i].is_able(index):
                    break
                else:
                    count = count + 1
            if count is int(end_token[2]) + 1 - int(start_token[2]):
                available = True
            else:
                count = 0
                index = index + 1

        for i in range(int(start_token[2]), int(end_token[2]) + 1):
            if int(start_token[2]) is i:
                start_time = ":".join(start_token[3:])
            else:
                start_time = "00:00:00"

            if int(end_date[2]) + 1 == i:
                end_time = ":".join(end_token[3:])
            else:
                end_time = "23:59:59"

            self.calendar_array[self.first_day + i].add_event(index,
                                                              start_time,
                                                              end_time,
                                                              title,
                                                              url)

    def get_first_day(self):
        return self.first_day

    def get_day(self, index):
        return self.calendar_array[index + self.first_day]

    def print_calendar(self):
        """Print calendar for test."""
        for day in self.calendar_array:
            day.print_day()
