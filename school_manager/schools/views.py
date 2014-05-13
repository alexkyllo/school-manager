#!/school-manager/school_manager/schools/views.py
"""
This Base view for for the schools app will facilitate the
creation and management of schools
"""

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
from schools.models import School
#from django import forms
from schools.forms import SchoolForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

# This is the base school app view and should provide access
# to school information

# First we have Class Based Views


class SchoolList(ListView):
    """This view returns a list of all school based upon the current user"""
    model = School
    def get_queryset(self):
        return School.objects.filter(manager=self.request.user)


class SchoolDetail(DetailView):
    """ The base class for viewing a school's detail"""
    model = School


class SchoolCreate(CreateView):
    """The base class for creating schools"""
    model = School
    form_class = SchoolForm
    def form_valid(self, form):
        """ Check on the form """
        form.instance.manager = self.request.user
        return super(SchoolCreate, self).form_valid(form)

# And then we have Function Based Views (FBV)

def home(request):
    """This function renders the schools index.html"""
    template = loader.get_template('schools/index.html')
    context = RequestContext(request, {
    })
    return HttpResponse(template.render(context))

def register(request):
    """ Base register function for schools"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html",
                  {'form': form,
                   })

