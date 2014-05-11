from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView
from schools.models import School
from django import forms
from schools.forms import SchoolForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

class SchoolList(ListView):
	model = School
	def get_queryset(self):
		return School.objects.filter(manager=self.request.user)

class SchoolDetail(DetailView):
	model = School


class SchoolCreate(CreateView):
	model = School
	form_class = SchoolForm

	def form_valid(self, form):
		form.instance.manager = self.request.user
		return super(SchoolCreate, self).form_valid(form)

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
