from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from school_calendar.models import *
from school_calendar.forms import *
from schools.models import School
from datetime import datetime
from dateutil import parser
from django.utils.timezone import utc
from school_calendar.event2fullcalendar import event_to_fullcalendar
import json

# Create your views here.

@require_GET
def view_school_calendar(request, **kwargs):
    '''
    Display the calendar template for a given school.
    '''
    school = School.objects.get(pk=kwargs['school_id'])
    return render_to_response('school_calendar/calendar_view.html', {'school' : school}, context_instance=RequestContext(request))

@require_GET
def view_all_events_between(request, **kwargs):
    '''
    This view is for the jquery-ui fullcalendar widget. Takes a GET request with a date range and returns all events inside the range
    in the JSON format that fullcalendar is expecting.
    '''
    if 'school_id' in kwargs:
        school_id = kwargs['school_id']
    elif 'schoolId' in request.GET:
        school_id = request.GET['schoolId']
    else:
        raise Http404
    events = Event.objects.filter(school_id=school_id)
    startdatetime = parser.parse(request.GET['start']+'T00:00:00.0+00:00')
    enddatetime = parser.parse(request.GET['end']+'T00:00:00.0+00:00')
    event_occurrences = [event.get_event_occurrences(startdatetime, enddatetime) for event in events]
    event_occurrences_flat = [item for sublist in event_occurrences for item in sublist] #flatten the list of lists of events
    fullcalendar_events = [event_to_fullcalendar(event) for event in event_occurrences_flat]
    return HttpResponse(json.dumps(fullcalendar_events))

@require_http_methods(['GET','POST'])
def create_event(request, **kwargs):
    if request.method == 'POST':
        if 'course_id' in kwargs:
            event_form = CourseSessionForm(request.POST, instance=Event())
        else:
            event_form = EventForm(request.POST, instance=Event())
        #event_form = CourseSessionForm(request.POST, instance=Event())
        rule_form = RuleForm(request.POST, instance=Rule())
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.creator = request.user
            if 'course_id' in kwargs:
                course = get_object_or_404(Course, id=kwargs['course_id'])
                event.course = course
                event.name = course.name
                school = get_object_or_404(School, id=course.school_id, members=request.user)
            else:
                school = get_object_or_404(School, id=kwargs['school_id'], members=request.user)
            event.school = school
            if event.recurring:
                if rule_form.is_valid():
                    rule = rule_form.save()
                    event.rule = rule
                else:
                    return render_to_response('school_calendar/event_form.html', {'event_form':event_form,'rule_form':rule_form}, context_instance=RequestContext(request))
            event.save()
            return HttpResponseRedirect(reverse('view_school_calendar', kwargs={'school_id':school.id}))
    else:
        if 'course_id' in kwargs:
            event_form = CourseSessionForm(instance=Event())
        else:
            event_form = EventForm(instance=Event())
        rule_form = RuleForm(instance=Rule())
    return render_to_response('school_calendar/event_form.html', {'event_form':event_form,'rule_form':rule_form}, context_instance=RequestContext(request))

@require_http_methods(['GET','POST'])
def update_event(request, **kwargs):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=kwargs['pk'])
        if 'course_id' in kwargs:
            event_form = CourseSessionForm(request.POST, instance=event)
        else:
            event_form = EventForm(request.POST, instance=event)
        if event.rule:
            rule_form = RuleForm(instance=event.rule)
        else:
            rule_form = RuleForm(instance=Rule())
        if event_form.is_valid():
            event = event_form.save(commit=False)
            if event.recurring:
                    if rule_form.is_valid():
                        rule = rule_form.save()
                        event.rule = rule
                    else:
                        return render_to_response('school_calendar/event_form.html', {'event_form':event_form,'rule_form':rule_form}, context_instance=RequestContext(request))
            event.save()
            return HttpResponseRedirect(reverse('view_school_calendar', kwargs={'school_id':event.school_id}))
    else:
        event = get_object_or_404(Event, id=kwargs['pk'])
        if 'course_id' in kwargs:
            event_form = CourseSessionForm(instance=event)
        else:
            event_form = EventForm(instance=event)
        if event.rule:
            rule_form = RuleForm(instance=event.rule)
        else:
            rule_form = RuleForm(instance=Rule())
    return render_to_response('school_calendar/event_form.html', {'event_form':event_form,'rule_form':rule_form}, context_instance=RequestContext(request))
