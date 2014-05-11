from django.conf.urls import patterns, include, url
from schools.views import SchoolList, SchoolDetail, SchoolCreate, register
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth.decorators import login_required


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'schools.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$',  login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/register/$', register),

    url(r'^schools/$', login_required(SchoolList.as_view())),
    url(r'^schools/(?P<pk>\d+)/$', login_required(SchoolDetail.as_view())),
    url(r'^schools/create/$', login_required(SchoolCreate.as_view(success_url='/schools/'))),
)
