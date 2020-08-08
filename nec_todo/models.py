import markdown
import re
from django.db import models
from django.urls import reverse


# Create your models here.
class Todo(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE)
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
