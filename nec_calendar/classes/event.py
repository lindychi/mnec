
class Event:
    """Unit class for storing events inside data."""

    title = ""
    url = ""
    start_rate = 0.0
    end_rate = 0.0

    def __init__(self, start_rate, end_rate, title, url):
        self.start_rate = start_rate
        self.end_rate = end_rate
        self.title = title
        self.url = url

    def get_title(self):
        return self.title

    def print_event(self):
        """Print event for test. """
        print(" - " + self.title)

    def html_event(self):
        html = "<span>"
        html += self.title
        html += "</span></br>"
        return html
