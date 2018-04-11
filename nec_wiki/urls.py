from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^page/edit/(?P<user_name>[^/]+)/(?P<page_name>.+)/$', views.edit_page, name='wiki_edit_page'),
    url(r'^page/create/(?P<user_name>[^/]+)/$', views.create_page, name='wiki_create_page'),
    url(r'^page/delete/(?P<user_name>[^/]+)/(?P<page_name>.+)/$', views.delete_page, name='wiki_delete_page'),
    url(r'^page/(?P<user_name>[^/]+)/(?P<page_name>[\s\S]+)/$', views.view_other_page, name='wiki_view_other_page'),
    url(r'^page/(?P<page_name>[\s\S]+)$', views.view_page, name='wiki_view_page'),
    # url(r'^tag/edit/(?P<user_name>[^/]+)/(?P<tag_name>.+)/$', views.edit_tag, name='wiki_edit_tag'),
    # url(r'^tag/save/(?P<user_name>[^/]+)/(?P<tag_name>.+)/$', views.save_tag, name='wiki_save_tag'),
    # url(r'^tag/save/(?P<user_name>[^/]+)/$', views.save_new_tag, name='wiki_save_new_tag'),
    # url(r'^tag/create/(?P<user_name>[^/]+)/$', views.create_tag, name='wiki_create_tag'),
    # url(r'^tag/delete/(?P<user_name>[^/]+)/(?P<tag_name>.+)/$', views.delete_tag, name='wiki_delete_tag'),
    url(r'^tag/create/(?P<user_name>[^/]+)/$', views.create_tag, name='wiki_create_tag'),
    url(r'^tag/(?P<user_name>[^/]+)/(?P<tag_name>.+)/$', views.view_tag, name='wiki_view_tag'),
    url(r'^$', views.index, name='wiki_index')
]
