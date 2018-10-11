"""Autogen for url."""
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf import settings
from . import views


urlpatterns = [
    url(r'^(?P<bank_id>[^/]*)$', views.index, name='bank_index'),
    url(r'^money/create/$', views.create_money, name='bank_create_money'),
    url(r'^money/(?P<money_id>[^/]+)/$', views.view_money, name='bank_view_money'),
    url(r'^money/edit/(?P<money_id>[^/]+)/$', views.edit_money, name='bank_edit_money'),
    url(r'^money/delete/(?P<money_id>[^/]+)/$', views.delete_money, name='bank_delete_money'),
    url(r'^bank/create/$', views.create_bank, name='bank_create_bank'),
    url(r'^bank/(?P<bank_id>[^/]+)/$', views.view_bank, name='bank_view_bank'),
    url(r'^bank/edit/(?P<bank_id>[^/]+)/$', views.edit_bank, name='bank_edit_bank'),
    url(r'^bank/delete/(?P<bank_id>[^/]+)/$', views.delete_bank, name='bank_delete_bank'),
]
