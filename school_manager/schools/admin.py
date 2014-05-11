from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from schools.models import School, Location, Course, Session

admin.site.register(School)
admin.site.register(Location)
admin.site.register(Course)
admin.site.register(Session)
