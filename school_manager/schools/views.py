from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from schools.models import School

class SchoolList(ListView):
    model = School

