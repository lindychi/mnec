from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='todo_index'),
    url(r'^create/(?P<user_name>[^/]+)/$', views.create, name='todo_create'),
    url(r'^save/(?P<user_name>[^/]+)/$', views.save_new, name='todo_save_new'),
    url(r'^save/(?P<user_name>[^/]+)/(?P<todo_id>[^/]+)/$', views.save, name='todo_save'),
    url(r'^view/(?P<user_name>[^/]+)/(?P<todo_name>.+)/$', views.view, name='todo_view'),
    url(r'^edit/(?P<user_name>[^/]+)/(?P<todo_id>[^/]+)/$', views.edit, name='todo_edit'),
    url(r'^delete/(?P<user_name>[^/]+)/(?P<todo_id>[^/]+)/$', views.delete, name='todo_delete'),
]