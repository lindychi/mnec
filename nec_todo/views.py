"""using url in function."""
from django.urls import reverse
from .models import Todo
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import TodoForm
from django.contrib.auth.decorators import login_required
from nec_calendar.classes.calendar import Calendar


# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def index(request):
    """Todo index page.

    list up all todo with current user
    """
    c = Calendar(timezone.now().year,
                 timezone.now().month)

    todo_list = Todo.objects.filter(owner=request.user, end_date__gte=c.get_start_datetime(), start_date__lte=c.get_end_datetime())
    todo_tuple = []
    for todo in todo_list:
        todo_tuple.append( (todo.start_date.strftime('%Y-%m-%d %H:%M:%S'), todo.end_date.strftime('%Y-%m-%d %H:%M:%S'), todo.title, reverse('todo_view', args=(request.user.username, todo.title, ))) )
        c.add_event(todo.start_date.strftime('%Y-%m-%d %H:%M:%S'),
                    todo.end_date.strftime('%Y-%m-%d %H:%M:%S'),
                    todo.title,
                    reverse('todo_view', args=(request.user.username, todo.title, )))

    return render(request, 'nec_todo/index.html',
                  {'calendar': c, 'todo_list': todo_list, 'todo_tuple': todo_tuple})


def recent_list(request):
    """Todo recent list page.

    list up all todo with current user
    """
    todo_filter = Todo.objects.filter(owner=request.user,
                                      created_date__lte=timezone.now())
    todo_list = todo_filter.order_by('-created_date')
    return render(request, 'nec_todo/recent_list.html',
                  {'todo_list': todo_list, 'user_name': request.user.username})


@login_required(login_url=settings.LOGIN_URL)
def create(request, user_name):
    """Create todo object."""
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid() and form.cleaned_data['end_date'] < form.cleaned_data['start_date']:
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.complete = False
            todo.save()
            return redirect(todo)
        else:
            return render(request, 'nec_todo/create.html', {'todo_form': form})
    else:
        form = TodoForm()
        return render(request, 'nec_todo/create.html', {'todo_form': form})


@login_required(login_url=settings.LOGIN_URL)
def view(request, user_name, todo_name):
    """View todo objects.

    Search todo objects with request.user, todo_name
    todo can generate same title
    """
    todo_list = Todo.objects.filter(owner=request.user, title=todo_name)
    return render(request, 'nec_todo/view.html',
                  {'todo_list': todo_list})


@login_required(login_url=settings.LOGIN_URL)
def edit(request, user_name, todo_id):
    """Edit todo content.

    when edit todo, search with todo_id.
    todo_name is not unique.
    """
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES, instance=todo)
        if form.is_valid():
            todo = form.save()
            return redirect(todo)
        else:
            return render(request, 'nec_todo/edit.html',
                          {'todo': todo, 'todo_form': form})

    else:
        form = TodoForm(instance=todo)
        return render(request, 'nec_todo/edit.html',
                      {'todo': todo, 'todo_form': form})


@login_required(login_url=settings.LOGIN_URL)
def delete(request, user_name, todo_id):
    """Delete todo object."""
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    title = todo.title
    todo.delete()
    do
    return redirect(reverse('todo_view',
                            args=(request.user.username, title, )))


@login_required(login_url=settings.LOGIN_URL)
def do(request, user_name, todo_id):
    """Do todo object.

    if todo.daily is True. todo obect is copy & save with current time
    and then write 'do todo object' in wiki_page.
    else just complete todo object.
    """
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    if todo.daily:
        now = timezone.now()
        new_todo = Todo(owner=todo.owner, title=todo.title, content=todo.content, start_date=now.strftime('%Y-%m-%d'), end_date=now.strftime('%Y-%m-%d %H:%M:%S'), daily=False, daily_page=todo.daily_page, complete=True)
        new_todo.save()
    else:
        todo.complete = True
        todo.save()
    return redirect(reverse('todo_index'))
