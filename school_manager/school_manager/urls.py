from django.conf.urls import patterns, include, url
from schools.views import (
    SchoolList, SchoolDetail, SchoolCreate, SchoolUpdate, SchoolDelete, 
    LocationList, LocationDetail, LocationCreate, LocationUpdate, LocationDelete,
    CourseList, CourseCreate, CourseUpdate, CourseDelete, CourseDetail,
    register, 
)
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from schools.models import School

urlpatterns = patterns('',
    url(r'^$', 'schools.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/register/$', register),

    url(r'^schools/$', SchoolList.as_view(), name='school_list'),
    url(r'^schools/(?P<pk>\d+)/$', SchoolDetail.as_view(), name='school_detail'),
    url(r'^schools/create/$', SchoolCreate.as_view(success_url='/schools/'), name='school_create'),
    url(r'^schools/(?P<pk>\d+)/update/$', SchoolUpdate.as_view(success_url='/schools/'), name='school_update'),
    url(r'^schools/(?P<pk>\d+)/delete/$', SchoolDelete.as_view(success_url='/schools/'), name='school_delete'),

)

#URL patterns for Location resources nested under schools
#TODO - Limit access to school's manager and return 404 to other school managers
urlpatterns += (
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/$',
        view = LocationList.as_view(),
        name = 'school_location_list',
    ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<pk>\d+)/$',
        view =  LocationDetail.as_view(),
        name = 'school_location_detail',
    ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/create/$',
        view =  LocationCreate.as_view(),
        name = 'school_location_create',
    ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<pk>\d+)/delete/$',
        view =  LocationDelete.as_view(),
        name = 'school_location_delete',
        ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<pk>\d+)/update/$',
        view =  LocationUpdate.as_view(),
        name = 'school_location_update',
        )
    )

#URL patterns for Course resources nested under locations
urlpatterns += (
    url(
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<location_id>\d+)/courses/create/$',
        view = CourseCreate.as_view(),
        name = 'school_location_course_create',
        ),
    url(
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<location_id>\d+)/courses/$',
        view = CourseList.as_view(),
        name = 'school_location_course_list',
        ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<location_id>\d+)/courses/(?P<pk>\d+)/delete/$',
        view =  CourseDelete.as_view(),
        name = 'school_location_course_delete',
        ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<location_id>\d+)/courses/(?P<pk>\d+)/update/$',
        view =  CourseUpdate.as_view(),
        name = 'school_location_course_update',
        ),
    url (
        regex = r'^schools/(?P<school_id>\d+)/locations/(?P<location_id>\d+)/courses/(?P<pk>\d+)/$',
        view =  CourseDetail.as_view(),
        name = 'school_location_course_detail',
        ),
    )

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
