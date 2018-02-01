
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
        html =  "<div class=\"calendar_event btn truncate left"
        if self.complete:
            html += " completed_event red darken-4"
        html += "\">"
        html += "<a href=\"" + self.url + "\">" + self.title + "</a>"
        html += "</div>"
        return html
