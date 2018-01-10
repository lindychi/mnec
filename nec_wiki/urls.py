from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/edit/$', views.edit_page, name='edit_wiki_page'),
    url(r'^(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/save/$', views.save_page, name='save_wiki_page'),
    url(r'^(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.view_page, name='view_wiki_page'),
    url(r'^(?P<user_name>[^/]+)/create/$', views.dashboard_page, name='dashboard_wiki_page'),
    url(r'^(?P<user_name>[^/]+)/$', views.dashboard_page, name='dashboard_wiki_page'),
]
