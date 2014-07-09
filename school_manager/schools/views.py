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
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from schools.forms import (
    SchoolForm, CourseForm, LocationForm, SessionForm,
    ManagerCreationForm, StudentCreationForm, InstructorCreationForm, UserUpdateForm,
)
from schools.models import School, Course, Location, Session


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

@login_required
@require_GET
def list_schools(request):
    schools = School.objects.filter(members=request.user)
    return render_to_response('schools/school_list.html', {'object_list': schools}, context_instance=RequestContext(request))

@login_required
@require_GET
def view_school(request, pk):
    school_id = pk
    school = get_object_or_404(School, members=request.user, id=school_id)
    return render_to_response('schools/school_detail.html', {'object':school}, context_instance=RequestContext(request))

@login_required
@permission_required('schools.can_create')
@require_http_methods(['GET','POST'])
def create_school(request):
    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid:
            school = form.save(commit=False)
            school.save()
            school.members = [request.user,]
            return HttpResponseRedirect(reverse('school_list'))
    else:
        form = SchoolForm()
    return render(request, 'schools/school_form.html', {'form':form}, context_instance=RequestContext(request))

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

class SessionMixin(object):
    model = Session
    form_class = SessionForm
    def get_queryset(self):
        #Filter the query set so that it only returns sessions for schools that the currently logged-in user is a member of
        return Session.objects.filter(school__members=self.request.user)

    def form_valid(self, form):
        form.instance.course_id = self.kwargs['course_id']
        course = get_object_or_404(Course, id=form.instance.course_id, school__members=self.request.user)
        form.instance.school_id = course.school_id
        
        return super(SessionMixin, self).form_valid(form)

class SessionCreate(SessionMixin, CreateView):
    pass

class SessionUpdate(SessionMixin, UpdateView):
    pass

class SessionDelete(SessionMixin, DeleteView):
    pass

class SessionDetail(SessionMixin, DetailView):
    pass

#Student CBVs
class StudentList(ListView):
    model = User
    template_name = 'schools/student_list.html'

    def get_queryset(self, *args, **kwargs):
        return User.objects.filter(groups__name='Students', school__id=self.kwargs.get('school_id'), school__members=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(StudentList, self).get_context_data(**kwargs)
        school = get_object_or_404(School,id=self.kwargs['school_id'], members=self.request.user)

        context['school_id'] = school.id
        context['school_name'] = school.name
        return context

class StudentCreate(CreateView):
    template_name = 'schools/user_form.html'
    form_class = StudentCreationForm

    @method_decorator(permission_required('users.can_create', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(StudentCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        school = get_object_or_404(School,id=self.kwargs['school_id'], members=self.request.user)
        school.members.add(self.object)
        students = Group.objects.get(name="Students")
        self.object.groups.add(students)
        return super(StudentCreate, self).form_valid(form)

    def get_success_url(self):
        username = self.request.POST['username'],
        return reverse(
            'user_view', 
            kwargs={
                'username' : username[0], 
            })

#Instructor CBVs
class InstructorList(ListView):
    model = User
    template_name = 'schools/instructor_list.html'

    def get_queryset(self):
        return User.objects.filter(groups__name='Instructors', school__members=self.request.user)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context

        context = super(InstructorList, self).get_context_data(**kwargs)
        school = get_object_or_404(School,id=self.kwargs['school_id'], members=self.request.user)

        context['school_id'] = school.id
        context['school_name'] = school.name
        return context

class InstructorCreate(CreateView):
    template_name = 'schools/user_form.html'
    form_class = InstructorCreationForm

    @method_decorator(permission_required('users.can_create', raise_exception=True))
    def dispatch(self, *args, **kwargs):
        return super(InstructorCreate, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        school = get_object_or_404(School,id=self.kwargs['school_id'], members=self.request.user)
        school.members.add(self.object)
        students = Group.objects.get(name="Instructors")
        self.object.groups.add(students)
        return super(InstructorCreate, self).form_valid(form)

    def get_success_url(self):
        username = self.request.POST['username'],
        return reverse(
            'user_view', 
            kwargs={
                'username' : username[0], 
            })

#User CBVs

class UserDetail(DetailView):
    template_name = 'schools/user_detail.html'

    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])    

class UserUpdate(UpdateView):
    template_name = 'schools/user_form.html'
    form_class = UserUpdateForm
    def get_object(self):
        return get_object_or_404(User, username=self.kwargs['username'])

#Function Based Views for homepage and register page

def angular_home(request):
    template = loader.get_template('angular/index.html')
    context = RequestContext(request, {
    })

    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

    return HttpResponse(template.render(context))

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
