"""For parse calendar html."""
import re
import calendar


class Calendar:
    """Print calendar html with other classes."""

    token_list = None

    def __init__(self, year, month):
        """Parse html and Build Array.

        html: The calendar for that month is entered in the form of a table.

        After parsing the html, it arranges the data and stores the size.
        """
        calendar_with_6 = calendar.HTMLCalendar(firstweekday=6)
        calendar_set_day = calendar_with_6.formatmonth(theyear=year,
                                                       themonth=month)

        raw_html_table = re.compile(r"""<td\sclass="
                                    ([^\"]+)         #class name
                                    ">
                                    ([^\<]+)         #day value
                                    </td>""", re.VERBOSE)
        self.token_list = raw_html_table.findall(calendar_set_day)

    def get_size(self):
        """Return Array size."""
        return len(self.token_list)

    def set_event(self, start_date, end_date, title, url):
        return True
