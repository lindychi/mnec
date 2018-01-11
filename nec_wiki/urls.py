from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^page/edit/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.edit_page, name='edit_wiki_page'),
    url(r'^page/save/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.save_page, name='save_wiki_page'),
    url(r'^page/save/(?P<user_name>[^/]+)/$', views.save_new_page, name='save_new_wiki_page'),
    url(r'^page/create/(?P<user_name>[^/]+)/$', views.create_page, name='create_wiki_page'),
    url(r'^page/delete/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.delete_page, name='delete_wiki_page'),
    url(r'^page/(?P<user_name>[^/]+)/(?P<page_name>[^/]+)/$', views.view_page, name='view_wiki_page'),
    # url(r'^tag/edit/(?P<user_name>[^/]+)/(?P<tag_name>[^/]+)/$', views.edit_tag, name='edit_wiki_tag'),
    # url(r'^tag/save/(?P<user_name>[^/]+)/(?P<tag_name>[^/]+)/$', views.save_tag, name='save_wiki_tag'),
    # url(r'^tag/save/(?P<user_name>[^/]+)/$', views.save_new_tag, name='save_new_wiki_tag'),
    # url(r'^tag/create/(?P<user_name>[^/]+)/$', views.create_tag, name='create_wiki_tag'),
    # url(r'^tag/delete/(?P<user_name>[^/]+)/(?P<tag_name>[^/]+)/$', views.delete_tag, name='delete_wiki_tag'),
    url(r'^tag/(?P<user_name>[^/]+)/(?P<tag_name>[^/]+)/$', views.view_tag, name='view_wiki_tag'),
    url(r'^(?P<user_name>[^/]+)/$', views.dashboard_page, name='dashboard_wiki_page'),
    url(r'^$', views.index_page, name='index_wiki_page')
]
