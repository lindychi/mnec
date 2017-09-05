from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^accounts/login/', auth_views.login, name='login', kwargs={'template_name':'login.html'}),
    utl(r'^accounts/logout/', auth_views.logout, name='logout', kwargs={'next_page':settings.LOGIN_URL})
]
