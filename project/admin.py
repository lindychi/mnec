from django.contrib import admin

from .models import Project, ProjectTodo

# Register your models here.
admin.site.register(Project)
admin.site.register(ProjectTodo)
