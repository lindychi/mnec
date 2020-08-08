from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone

from .models import Project, ProjectTodo
from .forms import ProjectTodoForm

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    model = Project
    paginate_by = 50

class CreateProjectView(LoginRequiredMixin, generic.CreateView):
    model = Project
    fields = ['title']
    success_url = reverse_lazy('project:index')

    def form_valid(self, form):
        project = form.save(commit=False)
        project.author = self.request.user
        result = super(CreateProjectView, self).form_valid(form)

        project_todo = ProjectTodo.objects.create(author=self.request.user, project=project, title=project.title, depth=0)
        project_todo.save()

        project.todo = project_todo
        project.save()

        return result


class DetailProjectView(LoginRequiredMixin, generic.DetailView):
    model = Project

    def get_context_data(self, **kwargs):
        context = super(DetailProjectView, self).get_context_data(**kwargs)
        context['child'] = ProjectTodo.objects.filter(project=self.get_object())
        context['child_clear_log'] = ProjectTodo.objects.filter(project=self.get_object(), is_clear=True).order_by('-clear_date')
        context['total_child_count'] = ProjectTodo.objects.filter(project=self.get_object()).count()
        context['total_clear_count'] = ProjectTodo.objects.filter(project=self.get_object(), is_clear=True).count()
        return context

def create_project_todo(request, project_id, todo_id=None):
    if request.method == 'POST':
        form = ProjectTodoForm(request.POST, request.FILES)

        if form.is_valid():
            project_todo = form.save(commit=False)
            project_todo.author = request.user
            project = Project.objects.get(pk=project_id)
            project_todo.project = project
            if todo_id:
                todo = ProjectTodo.objects.get(pk=todo_id)
                project_todo.parent = todo
                project_todo.depth = todo.depth + 1
            project_todo.save()
            return HttpResponseRedirect(reverse('project:detail_project', args=[project_id]))
    else:
        form = ProjectTodoForm()
        return render(request, 'project/create_todo.html', {
            'form': form,
        })

def delete_reverse_cascade(todo):
    todo = ProjectTodo.objects.filter(parent=todo)
    for t in todo:
        delete_reverse_cascade(t)
        t.delete()

def delete_project_todo(request, todo_id):
    todo = ProjectTodo.objects.get(id=todo_id)
    project_id = todo.project.id
    delete_reverse_cascade(todo)
    todo.delete()
    return HttpResponseRedirect(reverse('project:detail_project', args=[project_id]))

class EditProjectTodoView(LoginRequiredMixin, generic.edit.UpdateView):
    model = ProjectTodo
    fields = ['title', 'detail']

    def get_success_url(self):
        return reverse('project:detail_project', args=[self.object.project.id])

def clear_project_todo(request, todo_id):
    todo = ProjectTodo.objects.get(id=todo_id)
    if todo.is_clear:
        todo.is_clear = False
        todo.clear_date = None
    else:
        todo.is_clear = True
        todo.clear_date = timezone.now()
    todo.save()
    return HttpResponseRedirect(reverse('project:detail_project', args=[todo.project.id]))