from django import forms
from schools.models import School, Location, Course 
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('manager',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('school','managers')

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('location','school','managers')

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
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        students = Group.objects.get(name='Students')
        if commit:
            user.save()
            user.groups.add(students)
        return user

class InstructorCreationForm(UserCreationForm):
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        instructors = Group.objects.get(name='Instructors')
        if commit:
            user.save()
            user.groups.add(instructors)
        return user