import markdown
import re
from django.db import models
from django.urls import reverse
from datetime import timedelta,date
from django.utils.text import Truncator

# Create your models here.
class Todo(models.Model):
    owner = models.ForeignKey('auth.User')
    title = models.CharField(max_length=1024)
    content = models.TextField(blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    daily = models.BooleanField()
    daily_page = models.TextField(blank=True)
    complete = models.BooleanField()

    def __str__(self):
        if self.end_date is self.created_date:
            return "[%s ~ %s] %s" % (str(self.created_date),
                                     str(self.end_date),
                                     self.title)
        else:
            return "[%s ~ ] %s" % (str(self.created_date),
                                   self.title)

    def get_absolute_url(self):
        return reverse('todo_view', args=(self.title, ))

    def get_event_tuple(self):
        return [self.start_date]

    def get_markdown_content(self):
        return markdown.markdown(re.sub(r"\n", "<br />", self.content))

    def get_date_or_time(self, date):
        if date.strftime("%H:%M:%S") == "00:00:00":
            return date.strftime("%Y-%m-%d")
        else:
            return date.strftime("%Y-%m-%d %H:%M:%S")

    def get_event(self):
        start_date = self.start_date + timedelta(hours=9)
        end_date = self.end_date + timedelta(hours=9)
        attr_list = []
        attr_list.append("title:'"+Truncator(self.title).chars(30)+"'")
        attr_list.append("start:'"+self.get_date_or_time(start_date)+"'")
        if self.end_date is not self.created_date:
            attr_list.append("end:'"+self.get_date_or_time(end_date)+"'")
        attr_list.append("url:'"+reverse('todo_view', args=(self.title, ))+"'")
        if self.complete:
            attr_list.append("color:'#4caf50'")
            attr_list.append("textColor:'black'")
        else:
            attr_list.append("color:'#e57373'")
            attr_list.append("textColor:'black'")
        return "{" + ",".join(attr_list) + "}"

    def is_past_due(self):
        return date.today() > self.end_date.date()
