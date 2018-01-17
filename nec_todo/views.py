from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Todo
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import TodoForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def index(request):
    todo_list = Todo.objects.filter(owner=request.user, created_date__lte=timezone.now()).order_by('-created_date')
    return render(request, 'nec_todo/index.html', {'todo_list': todo_list, 'user_name':request.user.username})


@login_required(login_url=settings.LOGIN_URL)
def create(request, user_name):
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            return redirect(todo)
        else:
            return render(request, 'nec_todo/create.html', {'todo_form': form})
    else:
        form = TodoForm()
        return render(request, 'nec_todo/create.html', {'todo_form': form})


@login_required(login_url=settings.LOGIN_URL)
def view(request, user_name, todo_name):
    todo_list = Todo.objects.filter(owner=request.user, title=todo_name)
    return render(request, 'nec_todo/view.html', {'user_name': user_name, 'todo_list': todo_list})


@login_required(login_url=settings.LOGIN_URL)
def edit(request, user_name, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect(todo)
        else:
            return render(request, 'nec_todo/edit.html', {'todo': todo, 'todo_form':form})

    else:
        form = TodoForm(instance=todo)
        return render(request, 'nec_todo/edit.html', {'todo': todo, 'todo_form':form})


@login_required(login_url=settings.LOGIN_URL)
def delete(request, user_name, todo_id):
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    title = todo.title
    todo.delete()
    return redirect(reverse('todo_view', args=(request.user.username, title, )))

@login_required(login_url=settings.LOGIN_URL)
def do(request, user_name, todo_id):
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    if todo.daily:
        new_todo = copy.copy(todo)
        new_todo.start_date = datetime.datetime.now().strftime('%Y-%m-%d')
        new_todo.end_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_todo.complete = True
        new_todo.save()
    else:
        todo.complete = True
        todo.save()
    return redirect(reverse('todo_index'))
