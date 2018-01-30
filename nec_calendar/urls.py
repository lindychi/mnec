from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='calendar_today'),
    url(r'^$monthly/(?P<year>[^/]+)/(?P<month>[^/]+)/$',
        views.index, name='calendar_monthly'),
]
