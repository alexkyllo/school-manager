#!/school-manager/school_manager/students/views.py
"""
This Base view for for the Students app will facilitate the
CRUD of students
"""
from django.shortcuts import render
#from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from schools.models import School  #, Course, Location
from students.models import Student

def students_home(request):
    student_list = Student.objects.all()
    context = {'student_list': student_list}
    return render(request, 'students/index.html', context)


class LoginRequiredMixin(object):
    """Simple Mixin to require login for all classes in this view"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AnalyticsMixin(LoginRequiredMixin, object):
    """Mixin that attaches the Analysis model to classes"""
    model = Student

    #def get_queryset(self):
    #    return Student.objects.filter(user=self.request.user)
