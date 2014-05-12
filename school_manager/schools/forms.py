from django import forms
from schools.models import School, Location, Course

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('manager',)

class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        exclude = ('school',)

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        exclude = ('location',)