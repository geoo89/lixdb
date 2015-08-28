from django.conf.urls import patterns, include, url

from lixdb import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'testprj.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^(?P<root_name_url>levels(/[0-9A-z]+)*)[/]*$', views.level_list, name='level_list'), #TODO: add - and _
    url(r'^(?P<root_name_url>levels(/[0-9A-z]+)*/.*\.txt)$', views.replay_list, name='replay_list'), #TODO: add - and _
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^upload_replays/$', views.upload_replays, name='upload_replays'),
    url(r'^my_replays/$', views.my_replays, name='my_replays'),
)
