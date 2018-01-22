"""For parse calendar html."""
import re


class Calendar:
    """Print calendar html with other classes."""

    token_list = None

    def __init__(self, html):
        """Parse html and Build Array.

        html: The calendar for that month is entered in the form of a table.

        After parsing the html, it arranges the data and stores the size.
        """
        raw_html_table = re.compile(r"""<td\sclass="
                                    ([^\"]+)         #class name
                                    ">
                                    ([^\<]+)         #day value
                                    </td>""", re.VERBOSE)
        self.token_list = raw_html_table.findall(html)

    def get_size(self):
        """Return Array size."""
        return len(self.token_list)
