from django.conf.urls import url

from taskmaster import views

urlpatterns = [
    url(r'^$', views.jobgroups, name='jobgroups'),
    url(r'^kickstart$', views.kickstart, name='kickstart')
]