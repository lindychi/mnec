from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='todo_index'),
    url(r'^list$', views.list_all, name='todo_list'),
    url(r'^calendar/(?P<year>[^/]+)/(?P<month>[^/]+)/$', views.calendar, name='todo_calendar'),
    url(r'^create/$', views.create, name='todo_create'),
    url(r'^create_simple/$', views.create_simple, name='todo_create_simple'),
    url(r'^view/(?P<todo_name>.+)/$', views.view, name='todo_view'),
    url(r'^edit/(?P<todo_id>[^/]+)/$', views.edit, name='todo_edit'),
    url(r'^delete/(?P<todo_id>[^/]+)/$', views.delete, name='todo_delete'),
    url(r'^do/(?P<todo_id>[^/]+)/$', views.do, name='todo_do'),
    url(r'^undo/(?P<todo_id>[^/]+)/$', views.undo, name='todo_undo'),
    url(r'^delay_enddate/(?P<todo_id>[^/]+)/(?P<day>[^/]+)$', views.delay_enddate, name='todo_delay_enddate'),
]
