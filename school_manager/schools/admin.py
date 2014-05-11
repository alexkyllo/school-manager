from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from schools.models import Person, School, Location, Course, Session

# Define an inline admin descriptor for Person model
# which acts a bit like a singleton
class PersonInline(admin.StackedInline):
    model = Person
    can_delete = False
    verbose_name_plural = 'profile'

# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (PersonInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
#admin.site.register(Person)
admin.site.register(School)
admin.site.register(Location)
admin.site.register(Course)
admin.site.register(Session)
