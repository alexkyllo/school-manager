from django import forms
from django.forms.extras.widgets import SelectDateWidget
from schools.models import School, Location, Course, Session
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin.widgets import AdminDateWidget, AdminTimeWidget
import datetime

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('members',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('school',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('location','school',)

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        startdatetime = forms.DateTimeField(widget=AdminDateWidget, initial=datetime.date.today())
        enddatetime = forms.SplitDateTimeField()
        exclude = ('school','course','students')

class ManagerCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        managers = Group.objects.get(name='Managers')
        if commit:
            user.save()
            user.groups.add(managers)
        return user

class StudentCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")


class InstructorCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username")

class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "groups")