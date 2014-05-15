#!/school-manager/school_manager/analytics/views.py
"""
This Base view for for the Analytics app will facilitate the
analysis and metrics of this application
"""

#from django.template import RequestContext, loader
#from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
#from schools.models import School, Course, Location
from analytics.models import Analysis
#from django import forms
#from django.shortcuts import render
#from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    """Simple Mixin to require login for all classes in this view"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AnalyticsMixin(LoginRequiredMixin, object):
    """Mixin that attaches the Analysis model to classes"""
    model = Analysis

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user)


class AnalyticsList(AnalyticsMixin, ListView):
    """CBV for listing all previous analytics"""
    pass


class AnalyticsDetail(AnalyticsMixin, DetailView):
    """CBV to show the details of a particular analysis"""
    pass


class AnalyticsCreate(AnalyticsMixin, CreateView):
    """Start an Analysis"""
    pass


class AnalyticsDelete(AnalyticsMixin, DeleteView):
    """Delete and Analysis"""
    pass


class AnalyticsUpdate(AnalyticsMixin, UpdateView):
    """Update and Analysis"""
    pass
