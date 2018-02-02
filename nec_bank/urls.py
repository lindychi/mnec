"""Autogen for url."""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^$', views.index, name='bank_index'),
    url(r'^money/create/$', views.create_money, name='bank_create_money'),
    url(r'^money/(?P<money_id>[^/]+)/$', views.view_money, name='bank_view_money'),
    url(r'^money/edit/(?P<money_id>[^/]+)/$', views.edit_money, name='bank_edit_money'),
    url(r'^money/delete/(?P<money_id>[^/]+)/$', views.delete_money, name='bank_delete_money'),
]
