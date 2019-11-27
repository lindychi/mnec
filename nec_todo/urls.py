from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='todo_index'),
    url(r'^calendar/(?P<year>[^/]+)/(?P<month>[^/]+)/$', views.calendar, name='todo_calendar'),
    url(r'^create/$', views.create, name='todo_create'),
    url(r'^view/(?P<todo_name>.+)/$', views.view, name='todo_view'),
    url(r'^edit/(?P<todo_id>[^/]+)/$', views.edit, name='todo_edit'),
    url(r'^delete/(?P<todo_id>[^/]+)/$', views.delete, name='todo_delete'),
    url(r'^do/(?P<todo_id>[^/]+)/(?P<update>[^/]+)/$', views.do, name='todo_do'),
    url(r'^undo/(?P<todo_id>[^/]+)/$', views.undo, name='todo_undo'),
]
