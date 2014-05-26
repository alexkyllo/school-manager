#!/school-manager/school_manager/schools/views.py
"""
This Base view for for the schools app will facilitate the
creation and management of schools
"""

from django import forms
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from schools.forms import SchoolForm, CourseForm, LocationForm, ManagerCreationForm, StudentCreationForm, InstructorCreationForm
from schools.models import School, Course, Location


# This is the base school app view and should provide access
# to school information

# First we have Class Based Views
# Views for School Model

class LoginRequiredMixin(object):
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class SchoolMixin(LoginRequiredMixin, object):
    model = School

    def get_queryset(self):
        return School.objects.filter(members=self.request.user)

class SchoolList(SchoolMixin, ListView):
    pass

class SchoolDetail(SchoolMixin, DetailView):
    pass

class SchoolCreate(SchoolMixin, CreateView):
    form_class = SchoolForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        self.object.members = [self.request.user,]
        return super(SchoolCreate, self).form_valid(form)

class SchoolDelete(SchoolMixin, DeleteView):
    @method_decorator(permission_required('schools.can_delete', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(SchoolDelete, self).dispatch(*args, **kwargs)

class SchoolUpdate(SchoolMixin, UpdateView):
    form_class = SchoolForm

#Views for Location Model
class LocationMixin(LoginRequiredMixin, object):
    model = Location

    def get_queryset(self):
        #Filter the query set so that it only returns locations for schools that are managed by the currently logged-in user
        return Location.objects.filter(school__members=self.request.user)

    def form_valid(self, form):
        form.instance.school_id = self.kwargs['school_id']
        membership = get_object_or_404(School, id=form.instance.school_id, members=self.request.user)

        return super(LocationMixin, self).form_valid(form)

class LocationList(LocationMixin, ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationList, self).get_context_data(**kwargs)
        school = get_object_or_404(School, id=self.kwargs['school_id'], members=self.request.user)
        context['school_name'] = school.name
        context['school_id'] = school.id 
        return context

    def get_queryset(self):
        return Location.objects.filter(school__members=self.request.user, school_id=self.kwargs['school_id'])

class LocationDetail(LocationMixin, DetailView):
    pass

class LocationCreate(LocationMixin, CreateView):
    form_class = LocationForm

class LocationDelete(LocationMixin, DeleteView):
    pass

class LocationUpdate(LocationMixin, UpdateView):
    form_class = LocationForm

#Views for Course Model
class CourseMixin(LoginRequiredMixin, object):
    model = Course

    #def get_success_url(self):
    #    school_id = self.request.get('school_id'),
    #    location_id = self.kwargs.get('location_id'),
    #    return reverse(
    #        'school_location_course_list', 
    #        kwargs={
    #            'school_id' : school_id[0], 
    #            'location_id' : location_id[0],
    #        })

    def get_queryset(self):
        return Course.objects.filter(location__school__members=self.request.user)

    def form_valid(self, form):
        form.instance.location_id = self.kwargs['location_id']
        location = get_object_or_404(Location, id=form.instance.location_id, school__members=self.request.user)
        form.instance.school_id = location.school_id
        
        return super(CourseMixin, self).form_valid(form)

class CourseList(CourseMixin, ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(CourseList, self).get_context_data(**kwargs)
        location = get_object_or_404(Location,id=self.kwargs['location_id'], school__members=self.request.user)

        context['location_id'] = location.id
        context['location_name'] = location.name
        return context

    def get_queryset(self):
        return Course.objects.filter(location__school__members=self.request.user, location_id=self.kwargs['location_id'])

class CourseCreate(CourseMixin, CreateView):
    form_class = CourseForm

class CourseDelete(CourseMixin, DeleteView):
    pass

class CourseUpdate(CourseMixin, UpdateView):
    form_class = CourseForm

class CourseDetail(CourseMixin, DetailView):
    pass

#Student CBVs
class StudentMixin(LoginRequiredMixin, object):
    model = User

    def get_queryset(self):
        return User.objects.filter(groups__name='Students', school__members=self.request.user)

    def get_success_url(self):
        username = self.request.POST['username'],
        return reverse(
            'student_view', 
            kwargs={
                'username' : username[0], 
            })

class StudentList(StudentMixin, ListView):
    template_name = 'schools/student_list.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(StudentList, self).get_context_data(**kwargs)
        school = get_object_or_404(School,id=self.kwargs['school_id'], members=self.request.user)

        context['school_id'] = school.id
        context['school_name'] = school.name
        return context

class StudentDetail(StudentMixin, DetailView):
    template_name = 'schools/student_detail.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

class StudentCreate(StudentMixin, CreateView):
    template_name = 'schools/student_form.html'
    form_class = StudentCreationForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        school = get_object_or_404(School,id=self.kwargs['school_id'], members=self.request.user)
        school.members.add(self.object)
        students = Group.objects.get(name="Students")
        self.object.groups.add(students)
        return super(StudentCreate, self).form_valid(form)

class StudentUpdate(StudentMixin, UpdateView):
    pass

class StudentDelete(StudentMixin, DeleteView):
    pass

#Function Based Views for homepage and register page

def home(request):
    """This function renders the schools index.html"""
    template = loader.get_template('schools/index.html')
    context = RequestContext(request, {
    })

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    return HttpResponse(template.render(context))

def register(request):
    """ Base register function for schools"""
    if request.user.is_authenticated():
        logout(request)

    if request.method == 'POST':
        form = ManagerCreationForm(request.POST) #UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/")
    else:
        form = ManagerCreationForm()
    return render(request, "registration/register.html",
                  {'form': form,
                   })
