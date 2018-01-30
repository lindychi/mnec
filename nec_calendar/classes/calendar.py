"""For parse calendar html."""
import re
import calendar

from django.utils import timezone

from .day import Day


class Calendar:
    """Print calendar html with other classes."""

    year = 0
    month = 0
    first_day_index = 0
    last_day = 0
    token_list = ()
    calendar_array = []

    def __init__(self, year, month):
        """Parse html and Build Array.

        html: The calendar for that month is entered in the form of a table.

        After parsing the html, it arranges the data and stores the size.
        """
        self.year = year
        self.month = month
        self.last_day = calendar.monthrange(self.year, self.month)[1]
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
                self.first_day_index = len(self.calendar_array) - 1
            self.calendar_array.append(Day(token_class,
                                       self.year,
                                       self.month,
                                       token_value))

    def add_event(self, start_date, end_date, title, url, complete):
        start_token = list(re.findall(r'(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)',
                                      start_date)[0])
        end_token = list(re.findall(r'(\d+)-(\d+)-(\d+)\s(\d+):(\d+):(\d+)',
                                    end_date)[0])

        if int(start_token[1]) < self.month:
            start_token[2] = "1"
        elif int(start_token[1]) > self.month:
            return

        if int(end_token[1]) > self.month or start_date == end_date:
            end_token[2] = str(self.last_day)
        elif int(end_token[1]) < self.month:
            return

        available = False
        index = 0
        count = 0
        while not available:
            for i in range(int(start_token[2]), int(end_token[2]) + 1):
                if not self.calendar_array[self.first_day_index + i].is_able(index):
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

            self.calendar_array[self.first_day_index + i].add_event(index,
                                                                    start_time,
                                                                    end_time,
                                                                    title,
                                                                    url,
                                                                    complete)

    def get_first_day_index(self):
        return self.first_day_index

    def get_start_datetime(self):
        return timezone.datetime(year=self.year, month=self.month, day=1, hour=0, minute=0, second=0)

    def get_end_datetime(self):
        return timezone.datetime(year=self.year, month=self.month, day=self.last_day, hour=23, minute=59, second=59)

    def get_day(self, index):
        return self.calendar_array[index + self.first_day_index]

    def print_calendar(self):
        """Print calendar for test."""
        for day in self.calendar_array:
            day.print_day()

    def html_calendar(self):
        """Return html format calendar."""
        html =  "<div class=\"calendar_wrapper\">"
        html += "  <div class=\"current-month\">" + str(self.year) + "년 " + str(self.month) + "월</div>"
        html += "  <div class=\"calendar\">"
        html += "    <div class=\"calendar_header\">"
        html += "      <div>일</div>"
        html += "      <div>월</div>"
        html += "      <div>화</div>"
        html += "      <div>수</div>"
        html += "      <div>목</div>"
        html += "      <div>금</div>"
        html += "      <div>토</div>"
        html += "    </div>"
        for i in range(len(self.calendar_array)):
            if i % 7 is 0:
                html += "<div class=\"calendar_week\">"

            html += self.calendar_array[i].html_day()

            if i % 7 is 6:
                html += "</div>"
        html += "  </div>"
        html += "</div>"
        return html
