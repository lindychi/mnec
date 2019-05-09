"""using url in function."""
from django.db.models import F, Q
from django.urls import reverse
from .models import Todo
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import TodoForm
from django.contrib.auth.decorators import login_required
from nec_calendar.classes.calendar import Calendar
from django.utils import timezone
from nec_wiki.models import Page
from django.db.models import Q
from datetime import timedelta,date


# Create your views here.
# def index(request):
#     """Todo index page.
#
#     list up all todo with current user
#     """
#     return calendar(request, timezone.datetime.now().year, timezone.datetime.now().month)

# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def index(request):
    todo_list = get_event_array(request)
    return render(request, 'nec_todo/calendar.html', {'todo_list':todo_list})


@login_required(login_url=settings.LOGIN_URL)
def list_all(request):
    tommorow = date.today() + timedelta(1)
    daily_list = Todo.objects.filter(owner=request.user, complete=False, daily=True, end_date__lt=tommorow).order_by('end_date')
    todo_list = Todo.objects.filter(owner=request.user, complete=False, daily=False).order_by('end_date')
    return render(request, 'nec_todo/todo_list.html', {'todo_list':todo_list, 'daily_list':daily_list})

@login_required(login_url=settings.LOGIN_URL)
def get_event_array(request):
    todo_list = Todo.objects.filter(owner=request.user)
    todo_array = []

    for todo in todo_list:
        todo_array.append(todo.get_event())

    return ",".join(todo_array)

@login_required(login_url=settings.LOGIN_URL)
def calendar(request, year, month):
    c = Calendar(year, month)
    c.set_url('todo_calendar')

    todo_list = Todo.objects.filter(owner=request.user,
                                    start_date__lte=c.get_end_datetime())
    todo_list = todo_list.filter(Q(end_date=F('start_date')) | Q(end_date__gte=c.get_start_datetime()))
    for todo in todo_list:
        c.add_event(todo.start_date.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                    todo.end_date.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                    todo.title,
                    reverse('todo_view', args=(todo.title, )),
                    todo.complete)

    return render(request, 'nec_todo/calendar.html', {'calendar': c, 'todo_list': todo_list})


def recent_list(request):
    """Todo recent list page.

    list up all todo with current user
    """
    todo_filter = Todo.objects.filter(owner=request.user,
                                      created_date__lte=timezone.datetime.now())
    todo_list = todo_filter.order_by('-created_date')
    return render(request, 'nec_todo/recent_list.html',
                  {'todo_list': todo_list, 'user_name': request.user.username})


@login_required(login_url=settings.LOGIN_URL)
def create(request):
    """Create todo object."""
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.complete = False
            todo.save()
            return redirect(todo)
        else:
            return render(request, 'nec_todo/create.html', {'todo_form': form})
    else:
        form = TodoForm(request.GET)
        return render(request, 'nec_todo/create.html', {'todo_form': form})

@login_required(login_url=settings.LOGIN_URL)
def create_simple(request):
    """Create todo object."""
    if request.method == 'POST':
        form = TodoForm(request.POST, request.FILES)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.complete = False
            todo.save()
            return redirect(todo)
        else:
            return render(request, 'nec_todo/create_simple.html', {'todo_form': form, 'error_msg': error_msg})
    else:
        return render(request, 'nec_todo/create_simple.html')

@login_required(login_url=settings.LOGIN_URL)
def view(request, todo_name):
    """View todo objects.

    Search todo objects with request.user, todo_name
    todo can generate same title
    """
    todo_list = Todo.objects.filter(owner=request.user, title=todo_name)
    return render(request, 'nec_todo/view.html',
                  {'todo_list': todo_list})


@login_required(login_url=settings.LOGIN_URL)
def edit(request, todo_id):
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
def delete(request, todo_id):
    """Delete todo object."""
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    title = todo.title
    todo.delete()
    if "view/" in request.META['HTTP_REFERER']:
        return redirect(reverse('todo_index'))
    else:
        return redirect(request.META['HTTP_REFERER'])


@login_required(login_url=settings.LOGIN_URL)
def do(request, todo_id):
    """Do todo object.

    if todo.daily is True. todo obect is copy & save with current time
    and then write 'do todo object' in wiki_page.
    else just complete todo object.
    """
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    now = timezone.now()
    if todo.daily:
        now = timezone.now()
        new_todo = Todo(owner=todo.owner, title=todo.title, content=todo.content,
                        start_date=now.astimezone().strftime('%Y-%m-%d'),
                        end_date=now.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                        daily=False, daily_page=todo.daily_page, complete=True)
        new_todo.save()
        next_day = now + timezone.timedelta(days=1)
        todo.start_date = next_day.astimezone().strftime('%Y-%m-%d')
        todo.end_date = next_day.astimezone().strftime('%Y-%m-%d')
        todo.save()
    else:
        todo.complete = True
        todo.end_date = timezone.datetime.now()
        todo.save()

    if todo.daily_page:
        try:
            page = Page.objects.get(owner=request.user, title=todo.daily_page)
        except Page.DoesNotExist:
            page = Page(owner=request.user, title=todo.daily_page)
        log_msg = "%s <a href=\"%s\">%s</a>을 완료함.</br>" % (now.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                                                              reverse('todo_view', args=(todo.title,)),
                                                              todo.title)
        page.todo_log = log_msg + page.todo_log
        page.save()
    return redirect(request.META['HTTP_REFERER'])

@login_required(login_url=settings.LOGIN_URL)
def undo(request, todo_id):
    """Undo todo object.

    if todo.daily is True. todo obect is copy & save with current time
    and then write 'do todo object' in wiki_page.
    else just complete todo object.
    """
    todo = Todo.objects.get(id=int(todo_id), owner=request.user)
    now = timezone.now()
    todo.complete = False
    todo.end_date = todo.start_date
    todo.save()

    if todo.daily_page:
        try:
            page = Page.objects.get(owner=request.user, title=todo.daily_page)
        except Page.DoesNotExist:
            page = Page(owner=request.user, title=todo.daily_page)
        log_msg = "%s <a href=\"%s\">%s</a>을 재수행함.</br>" % (now.astimezone().strftime('%Y-%m-%d %H:%M:%S'),
                                                                reverse('todo_view', args=(todo.title,)),
                                                                todo.title)
        page.todo_log = log_msg + page.todo_log
        page.save()
    return redirect(reverse('todo_index'))
