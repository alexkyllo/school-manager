from django.conf.urls import patterns, include, url
from schools.views import SchoolList
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'school_manager.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^schools/$', SchoolList.as_view())
)
