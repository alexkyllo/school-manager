from django.conf.urls import patterns, include, url
from schools.views import SchoolList, SchoolDetail, SchoolCreate, PersonDetail, register
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout_then_login


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'schools.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^schools/$', SchoolList.as_view()),
    url(r'^schools/(?P<pk>\d+)/$', SchoolDetail.as_view()),
    url(r'^schools/create/$', SchoolCreate.as_view()),
    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/register/$', register),
)
