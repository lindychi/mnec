from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^edit/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.edit_page, name='edit_wiki_page'),
    url(r'^save/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.save_page, name='save_wiki_page'),
    url(r'^save/(?P<user_name>[^/]+)/$', views.save_new_page, name='save_new_wiki_page'),
    url(r'^create/(?P<user_name>[^/]+)/$', views.create_page, name='create_wiki_page'),
    url(r'^delete/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.delete_page, name='delete_wiki_page'),
    url(r'^(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.view_page, name='view_wiki_page'),
    url(r'^(?P<user_name>[^/]+)/$', views.dashboard_page, name='dashboard_wiki_page'),
    url(r'^$', views.index_page, name='index_wiki_page')
]
