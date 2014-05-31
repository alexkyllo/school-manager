from django.conf.urls import patterns, url

from students import views

urlpatterns = patterns('',
    url(r'^$', views.students_home, name='index'),
)
