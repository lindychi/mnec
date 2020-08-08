from django.urls import path

from . import views

app_name = 'project'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create_project/', views.CreateProjectView.as_view(), name='create_project'),
    path('detail_project/<int:pk>/', views.DetailProjectView.as_view(), name='detail_project'),
    path('create_projecttodo/<int:project_id>/<int:todo_id>/', views.create_project_todo, name='create_projecttodo'),
    path('delete_projecttodo/<int:todo_id>/', views.delete_project_todo, name='delete_projecttodo'),
    path('edit_projecttodo/<int:pk>/', views.EditProjectTodoView.as_view(), name='edit_projecttodo'),
    path('clear_projecttodo/<int:todo_id>/', views.clear_project_todo, name='clear_projecttodo'),
]
