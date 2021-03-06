
class Event:
    """Unit class for storing events inside data."""

    title = ""
    url = ""
    start_rate = 0.0
    end_rate = 0.0
    complete = False

    def __init__(self, start_rate, end_rate, title, url, complete):
        self.start_rate = start_rate
        self.end_rate = end_rate
        self.title = title
        self.url = url
        self.complete = complete

    def get_title(self):
        return self.title

    def print_event(self):
        """Print event for test. """
        print(" - " + self.title)

    def html_event(self):
        html =  "<a href=\"" + self.url + "\"><div class=\"calendar_event btn truncate left"
        if self.complete:
            html += " completed_event"
        html += "\">"
        html += self.title
        html += "</div></a>"
        return html
