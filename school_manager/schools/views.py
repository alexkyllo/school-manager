#!/school-manager/school_manager/schools/views.py
"""
This Base view for for the schools app will facilitate the
creation and management of schools
"""

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
<<<<<<< HEAD
from django.views.generic import ListView, DetailView, CreateView
from schools.models import School
#from django import forms
from schools.forms import SchoolForm
=======
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from schools.models import School, Course, Location
from django import forms
from schools.forms import SchoolForm, CourseForm, LocationForm
>>>>>>> a3cedaecb0002fdd3a8966cf9fded95d640f3eb1
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.core.urlresolvers import reverse

<<<<<<< HEAD
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
=======
class SchoolMixin(object):
	model = School

	def get_queryset(self):
		return School.objects.filter(manager=self.request.user)

class SchoolList(SchoolMixin, ListView):
	pass
>>>>>>> a3cedaecb0002fdd3a8966cf9fded95d640f3eb1

class SchoolDetail(SchoolMixin, DetailView):
	pass

<<<<<<< HEAD
class SchoolCreate(CreateView):
    """The base class for creating schools"""
    model = School
    form_class = SchoolForm
    def form_valid(self, form):
        """ Check on the form """
        form.instance.manager = self.request.user
        return super(SchoolCreate, self).form_valid(form)
=======
class SchoolCreate(SchoolMixin, CreateView):
	form_class = SchoolForm
>>>>>>> a3cedaecb0002fdd3a8966cf9fded95d640f3eb1

# And then we have Function Based Views (FBV)

class SchoolDelete(SchoolMixin, DeleteView):
	pass

class SchoolUpdate(SchoolMixin, UpdateView):
	form_class = SchoolForm

class LocationMixin(object):
	model = Location

	def get_success_url(self):
		school_id = self.kwargs.get('school_id'),
		return reverse('school_location_list', kwargs={'school_id': school_id[0]})

	def get_queryset(self):
		
		return Location.objects.filter(
			school_id=self.kwargs['school_id'],
		)

	def form_valid(self, form):
		form.instance.school_id = self.kwargs.get('school_id')
		return super(LocationMixin, self).form_valid(form)

class LocationList(LocationMixin, ListView):
	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(LocationList, self).get_context_data(**kwargs)
	    school_id=self.kwargs['school_id']
	    school = School.objects.get(id=school_id)
	    school_name = school.name
	    context['school_name'] = school_name
	    context['school_id'] = school_id 
	    return context

class LocationDetail(LocationMixin, DetailView):
	pass

class LocationCreate(LocationMixin, CreateView):
	form_class = LocationForm

class LocationDelete(LocationMixin, DeleteView):
	pass

class LocationUpdate(LocationMixin, UpdateView):
	form_class = LocationForm

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

