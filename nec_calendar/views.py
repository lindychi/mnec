from django.shortcuts import render
from django.utils import timezone
from nec_todo.models import Todo


# Create your views here.
def index(request):
    todo_list = get_event_array(request)
    return render(request, 'nec_calendar/index.html', {'todo_list':todo_list})

def get_event_array(request):
    todo_list = Todo.objects.filter(owner=request.user)
    todo_array = []

    for todo in todo_list:
        todo_array.append(todo.get_event())

    return "{" + todo_array.join(',') + "}"
