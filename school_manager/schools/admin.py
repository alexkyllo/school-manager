from django.contrib import admin

from .models import Person, School, Location, Course, Session

admin.site.register(Person)
admin.site.register(School)
admin.site.register(Location)
admin.site.register(Course)
admin.site.register(Session)
