from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Todo
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import TodoForm


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        todo_list = Todo.objects.filter(owner=request.user, created_date__lte=timezone.now()).order_by('-created_date')
        return render(request, 'nec_todo/index.html', {'todo_list': todo_list, 'user_name':request.user.username})
    else:
        return redirect(settings.LOGIN_URL)


def create(request, user_name):
    if request.user.is_authenticated:
        return render(request, 'nec_todo/create.html', {'user_name':user_name})
    else:
        return redirect(settings.LOGIN_URL)


def save_new(request, user_name):
    if request.user.is_authenticated and request.user.username == user_name:
        content = request.POST["content"]
        todo_name = request.POST["title"]
        todo = Todo(owner=request.user, title=todo_name, content=content)
        todo.save()
        return HttpResponseRedirect(reverse('todo_index'))
    else:
        return redirect(settings.LOGIN_URL)


def save(request, user_name, todo_id):
    if request.user.is_authenticated and request.user.username == user_name:
        title = request.POST["title"]
        content = request.POST["content"]
        try:
            todo = Todo.objects.get(id=int(todo_id), owner=request.user)
            todo.content = content
        except Todo.DoesNotExist:
            todo = Page(owner=request.user, title=title, content=content)
        todo.save()
        return HttpResponseRedirect(reverse('todo_view', args=(user_name, title,)))
    else:
        return redirect(settings.LOGIN_URL)


def view(request, user_name, todo_name):
    if request.user.is_authenticated and request.user.username == user_name:
        todo_list = Todo.objects.filter(owner=request.user, title=todo_name)
        return render(request, 'nec_todo/view.html', {'user_name': user_name, 'todo_list': todo_list})
    else:
        return redirect(settings.LOGIN_URL)


def edit(request, user_name, todo_id):
    if request.user.is_authenticated and request.user.username == user_name:
        todo = get_object_or_404(Todo, id=todo_id)
        if request.method == 'POST':
            form = TodoForm(request.POST, request.FILES, instance=todo)
            if form.is_valid():
                todo = form.save()
                return redirect(todo)
        else:
            todo_form = TodoForm(instance=todo)
            return render(request, 'nec_todo/edit.html', {'todo': todo, 'todo_form':todo_form})
    else:
        return redirect(settings.LOGIN_URL)


def delete(request, user_name, todo_id):
    if request.user.is_authenticated and request.user.username == user_name:
        todo = Todo.objects.get(id=int(todo_id), owner=request.user)
        title = todo.title
        todo.delete()
        return redirect(reverse('todo_view', args=(request.user.username, title, )))
    else:
        return redirect(settings.LOGIN_URL)
    return None
