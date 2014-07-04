from django import forms
from django.forms.extras.widgets import SelectDateWidget
from schools.models import School, Location, Course, Session
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
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

class DateTimeWidget(forms.MultiWidget):

    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

class SessionForm(forms.ModelForm):
    startdatetime = forms.SplitDateTimeField(label="Start Date/Time", widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    enddatetime = forms.SplitDateTimeField(label="End Date/Time", widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    class Meta:
        model = Session
        
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