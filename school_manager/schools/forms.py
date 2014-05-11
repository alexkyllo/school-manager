from django import forms
from schools.models import School

class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        exclude = ('manager',)