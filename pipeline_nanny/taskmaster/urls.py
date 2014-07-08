from django.conf.urls import url

from taskmaster import views

urlpatterns = [
    url(r'^$', views.jobgroups, name='jobgroups'),
    url(r'^jobgroups/(?P<group_id>\d+)/$', views.jobgroup, name='jobgroup'),

    url(r'^kickstart$', views.kickstart, name='kickstart')
]