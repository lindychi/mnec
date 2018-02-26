"""import TestCase."""
from django.test import TestCase
from nec_todo.models import Todo
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# Create your tests here.
class TodoModelTest(TestCase):
    """Todo model testcase."""

    @classmethod
    def setUpTestData(cls):
        """Setup default data in db."""
        # Set up non-modified objects used by all test methods
        User.objects.create_user('hanchi')
        Todo.objects.create(title='test', owner=User.objects.get(id=1), end_date=timezone.now(), daily=False, start_date=timezone.now(), complete=False)

    def test_get_absolute_url(self):
        """Absolute url test."""
        todo = Todo.objects.get(id=1)
        self.assertEquals(todo.get_absolute_url(), '/todo/view/test/')