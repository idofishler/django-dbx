from django.conf.urls import patterns, url

from myapp import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^dropbox_auth_finish/$', views.dropbox_auth_finish, name='dropbox_auth_finish'),
    url(r'^dropbox_auth_start/$', views.dropbox_auth_start, name='dropbox_auth_start'),
    url(r'^dropbox_unlink/$', views.dropbox_unlink, name='dropbox_unlink'),
    url(r'^login/$', views.do_login, name='login'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^logout/$', views.do_logout, name='logout'),

)