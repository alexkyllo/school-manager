from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from schools.models import School, Course, Location
from django import forms
from schools.forms import SchoolForm, CourseForm, LocationForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.core.urlresolvers import reverse

class SchoolMixin(object):
	model = School

	def get_queryset(self):
		return School.objects.filter(manager=self.request.user)

class SchoolList(SchoolMixin, ListView):
	pass

class SchoolDetail(SchoolMixin, DetailView):
	pass

class SchoolCreate(SchoolMixin, CreateView):
	form_class = SchoolForm

	def form_valid(self, form):
		form.instance.manager = self.request.user
		return super(SchoolCreate, self).form_valid(form)

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
	template = loader.get_template('schools/index.html')
	context = RequestContext(request, {
	})
	return HttpResponse(template.render(context))

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/")
	else:
		form = UserCreationForm()
	return render(request, "registration/register.html", {
		'form': form,
	})
