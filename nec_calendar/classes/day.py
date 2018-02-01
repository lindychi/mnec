import calendar
import re
from .event import Event
from django.urls import reverse
import datetime


class Day:
    """Unit of calendar.

    control each day data and print result
    """
    class_str = "noday"
    year = 0
    month = 0
    day = 0
    event = []
    start_time = ""
    end_time = ""

    def __init__(self, class_str, year, month, day):
        self.class_str = class_str
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        self.event = []

        if self.class_str == "noday":
            self.set_noday()
        if self.month > 12 or self.month < 1:
            self.set_noday()
        try:
            if self.day > calendar.monthrange(year, month)[1] or self.day < 1:
                self.set_noday()
        except calendar.IllegalMonthError:
            self.set_noday()

    def set_noday(self):
        self.class_str = "noday"
        self.year = 0
        self.month = 0
        self.day = 0
        self.event = []

    def get_day(self):
        return self.day

    def get_day_str(self):
        if self.day is 0:
            return ""
        else:
            return str(self.day)

    def get_month(self):
        return self.month

    def is_able(self, index):
        """Check whether the event exists in the corresponding index."""
        if len(self.event) >= index + 1 and self.event[index] is not None:
            return False
        else:
            return True

    def calc_time_rate(self, time_token_list):
        calc_time = time_token_list[0] * 3600 + time_token_list[1] * 60 + time_token_list[2]
        return calc_time

    def add_event(self, index, start_time, end_time, title, url, complete):
        self.start_time = start_time
        self.end_time = end_time
        start_token = re.findall(r'(\d+):(\d+):(\d+)',
                                 start_time)[0]
        end_token = re.findall(r'(\d+):(\d+):(\d+)',
                               end_time)[0]

        event = Event(self.calc_time_rate(start_token),
                      self.calc_time_rate(end_token),
                      title,
                      url,
                      complete)

        for i in range(index + 1):
            if i is index:
                try:
                    self.event[index] = event
                except IndexError:
                    self.event.append(event)
            elif len(self.event) > i:
                continue
            else:
                self.event.append(None)

    def print_day(self):
        """Print day for test."""
        for e in self.event:
            if e is not None:
                e.print_event()
            else:
                print(" - None")

    def is_today(self):
        today = datetime.datetime.today()
        if today.year == self.year and today.month == self.month and today.day == self.day:
            return True
        else:
            return False

    def html_day(self):
        html = "<div class=\"calendar_day"
        if self.is_today():
            html += " calendar_today"
        html += " " + self.class_str
        html += "\">"
        html += "<div class=\"calendar_day_button\">"
        if self.get_day_str() != "":
            html += "<a href=\"%s?start_date=%s&end_date=%s\">%s</a>" % (reverse('todo_create', args=()),
                                                                         self.get_start_datetime(),
                                                                         self.get_end_datetime(),
                                                                         self.get_day_str())
        html += "</div>"

        for i in range(len(self.event)):
            if self.event[i] is not None:
                html += self.event[i].html_event()
            else:
                html += "<div class=\"calendar_event none_event btn white\">　</div>"
        html += "</div>"
        return html

    def get_event(self, index):
        if index < len(self.event):
            return self.event[index]
        else:
            return None

    def get_start_datetime(self):
        return "%4d-%02d-%02d 00:00:00" % (self.year, self.month, self.day)

    def get_end_datetime(self):
        return "%4d-%02d-%02d 23:59:59" % (self.year, self.month, self.day)
