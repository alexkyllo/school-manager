#!/school-manager/school_manager/schools/views.py
"""
This Base view for for the schools app will facilitate the
creation and management of schools
"""

from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User, Group
from schools.models import School, Course, Location
from django import forms
from schools.forms import SchoolForm, CourseForm, LocationForm, ManagerCreationForm
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.http import Http404

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
    pass

class SchoolUpdate(SchoolMixin, UpdateView):
    form_class = SchoolForm

#Views for Location Model
class LocationMixin(LoginRequiredMixin, object):
    model = Location

    #def get_success_url(self):
    #    school_id = self.kwargs.get('school_id'),
    #    return reverse('school_location_list', kwargs={'school_id': school_id[0]})

    def get_queryset(self):
        #Filter the query set so that it only returns locations for schools that are managed by the currently logged-in user
        return Location.objects.filter(school__members=self.request.user)

    def form_valid(self, form):
        form.instance.school_id = self.kwargs.get('school_id')
        return super(LocationMixin, self).form_valid(form)

class LocationList(LocationMixin, ListView):
    #pass
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LocationList, self).get_context_data(**kwargs)
        try:
            school_id = self.request.GET['school']
            school = School.objects.get(id=school_id)
        except:
            raise Http404

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

#Views for Course Model
class CourseMixin(LoginRequiredMixin, object):
    model = Course

    def get_success_url(self):
        school_id = self.kwargs.get('school_id'),
        location_id = self.kwargs.get('location_id'),
        return reverse(
            'school_location_course_list', 
            kwargs={
                'school_id' : school_id[0], 
                'location_id' : location_id[0],
            })

    def get_queryset(self):
        return Course.objects.filter(
            location_id=self.kwargs['location_id'],
        )

    def form_valid(self, form):
        form.instance.location_id = self.kwargs.get('location_id')
        return super(CourseMixin, self).form_valid(form)

class CourseList(CourseMixin, ListView):
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CourseList, self).get_context_data(**kwargs)
        school_id=self.kwargs['school_id']
        location_id=self.kwargs['location_id']
        location = Location.objects.get(id=location_id)
        location_name = location.name
        context['school_id'] = school_id 
        context['location_id'] = location_id
        context['location_name'] = location_name
        return context

class CourseCreate(CourseMixin, CreateView):
    form_class = CourseForm

class CourseDelete(CourseMixin, DeleteView):
    pass

class CourseUpdate(CourseMixin, UpdateView):
    form_class = CourseForm

class CourseDetail(CourseMixin, DetailView):
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

# CBVs for API Viewsets
from rest_framework import viewsets, permissions
from schools.permissions import IsManager, IsMember
from schools.serializers import (
    UserSerializer, GroupSerializer, SchoolSerializer, LocationSerializer, CourseSerializer,
)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsManager,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsManager,)

class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schools to be viewed or edited.
    """
    model = School
    serializer_class = SchoolSerializer
    permission_classes = (IsManager, IsMember,)
    def pre_save(self, obj):
        obj.members += self.request.user

    def get_queryset(self):
        return School.objects.filter(members=self.request.user)

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    model = Location
    permission_classes = (IsMember,)
    serializer_class = LocationSerializer
    def get_queryset(self):
        return Location.objects.filter(school__members=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Courses to be viewed or edited.
    """
    model = Course
    permission_classes = (IsMember,)
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.filter(location__school__members=self.request.user)

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users in the Students group to be viewed or edited.
    """
    model = User
    permission_classes = (IsManager, IsMember,)
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(groups__name='Students', school__members=self.request.user)

class InstructorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users in the Students group to be viewed or edited.
    """
    model = User
    permission_classes = (IsManager,)
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(groups__name='Instructors', school__members=self.request.user)