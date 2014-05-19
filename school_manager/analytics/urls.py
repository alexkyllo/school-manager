from django.conf.urls import patterns, url

from analytics import views

urlpatterns = patterns('',
    url(r'^$', views.analytics_home, name='index'),
    url(r'^chart/$', views.simple_chart, name='chart')
)