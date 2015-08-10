from django.conf.urls import patterns, include, url
from schools.views import *
from school_calendar.views import *
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout_then_login
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', login_required(home)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', login),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^accounts/register/$', register),
    url(r'^analytics/', include('analytics.urls')),
    url(r'^students/', include('students.urls')),

    #School resources
    url(r'^schools/$', list_schools, name='school_list'),
    url(r'^schools/(?P<pk>\d+)/$', view_school, name='school_detail'),
    #url(r'^schools/(?P<slug>[-\w]+)/$', SchoolDetail.as_view(), name='school_detail_by_slug'),
    url(r'^schools/create/$', create_school, name='school_create'),
    url(r'^schools/(?P<pk>\d+)/update/$', SchoolUpdate.as_view(success_url='/schools/'), name='school_update'),
    url(r'^schools/(?P<pk>\d+)/delete/$', SchoolDelete.as_view(success_url='/schools/'), name='school_delete'),

    #Location resources
    url(r'^schools/(?P<school_id>\d+)/locations/$', LocationList.as_view(), name='location_list'),
    url(r'^locations/(?P<pk>\d+)/$', LocationDetail.as_view(), name='location_detail'),
    url(r'^schools/(?P<school_id>\d+)/locations/create/$', LocationCreate.as_view(), name='location_create'),
    url(r'^locations/(?P<pk>\d+)/update/$', LocationUpdate.as_view(), name='location_update'),
    url(r'^locations/(?P<pk>\d+)/delete/$', LocationDelete.as_view(), name='location_delete'),

    #Course resources
    url(r'^locations/(?P<location_id>\d+)/courses/$', CourseList.as_view(), name='course_list'),
    url(r'^courses/(?P<pk>\d+)/$', CourseDetail.as_view(), name='course_detail'),
    url(r'^locations/(?P<location_id>\d+)/courses/create/$', CourseCreate.as_view(), name='course_create'),
    url(r'^courses/(?P<pk>\d+)/update/$', CourseUpdate.as_view(), name='course_update'),
    url(r'^courses/(?P<pk>\d+)/delete/$', CourseDelete.as_view(), name='course_delete'),

    #Session Resources
    #url(r'^courses/(?P<course_id>\d+)/sessions/(?P<pk>\d+)/$', SessionList.as_view(), name='session_list'),
    #url(r'^sessions/(?P<pk>\d+)/$', SessionDetail.as_view(), name='session_detail'),
    #url(r'^courses/(?P<course_id>\d+)/sessions/create/$', SessionCreate.as_view(), name='session_create'),
    #url(r'^sessions/(?P<pk>\d+)/update/$', SessionUpdate.as_view(), name='session_update'),
    #url(r'^sessions/(?P<pk>\d+)/delete/$', SessionDelete.as_view(), name='session_delete'),

    #User Resources
    url(r'^schools/(?P<school_id>\d+)/students/$', StudentList.as_view(), name='student_list'),
    url(r'^schools/(?P<school_id>\d+)/students/create/$', StudentCreate.as_view(), name='student_create'),
    url(r'^schools/(?P<school_id>\d+)/instructors/$', InstructorList.as_view(), name='instructor_list'),
    url(r'^schools/(?P<school_id>\d+)/instructors/create/$', InstructorCreate.as_view(), name='instructor_create'),
    url(r'^users/(?P<username>\w+)/$', UserDetail.as_view(), name='user_view'),
    url(r'^users/(?P<username>\w+)/update/$', UserUpdate.as_view(), name='user_update'),

    #Calendar
    url(r'^schools/(?P<school_id>\d+)/calendar/$', view_school_calendar, name='view_school_calendar'),
    url(r'^schools/(?P<school_id>\d+)/calendar/events/$', view_all_events_between, name='view_school_calendar_events'),
    url(r'^schools/(?P<school_id>\d+)/events/create/$', create_event, name='create_school_event'),
    url(r'^courses/(?P<course_id>\d+)/sessions/create/$', create_event, name='create_course_session'),
    url(r'^schools/(?P<school_id>\d+)/events/(?P<pk>\d+)/update/$', update_event, name='update_school_event'),
    url(r'^courses/(?P<course_id>\d+)/sessions/(?P<pk>\d+)/update/$', update_event, name='update_course_session'),
)

#URL routes for API
from rest_framework import routers
from api.views import (
    SchoolViewSet, LocationViewSet, UserViewSet, StudentViewSet, InstructorViewSet, GroupViewSet, CourseViewSet,
    )
from django.conf.urls import patterns, url, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'schools', SchoolViewSet, base_name='schools')
router.register(r'users', UserViewSet, base_name='users')
router.register(r'instructors', InstructorViewSet, base_name='instructors')
router.register(r'students', StudentViewSet, base_name='students')
router.register(r'groups', GroupViewSet)
router.register(r'locations', LocationViewSet, base_name='locations')
router.register(r'courses', CourseViewSet, base_name='courses')

# Wire up our API using automatic URL routing
# Additionally, we include login URLs for the browseable API.
urlpatterns += (
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
