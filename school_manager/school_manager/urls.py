from django.conf.urls import patterns, include, url
from schools.views import SchoolList, SchoolDetail
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'schools.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^schools/$', SchoolList.as_view()),
    url(r'^schools/(?P<pk>\d+)/$', SchoolDetail.as_view())
)
