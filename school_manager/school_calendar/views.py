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
    events = Event.objects.filter(school_id=kwargs['school_id'])
    startdatetime = parser.parse(request.GET['start']+'T00:00:00.0+00:00')
    enddatetime = parser.parse(request.GET['end']+'T00:00:00.0+00:00')
    event_occurrences = [event.get_event_occurrences(startdatetime, enddatetime) for event in events]
    event_occurrences_flat = [item for sublist in event_occurrences for item in sublist] #flatten the list of lists of events
    fullcalendar_events = [event_to_fullcalendar(event) for event in event_occurrences_flat]
    return HttpResponse(json.dumps(fullcalendar_events))

@require_http_methods(['GET','POST'])
def create_course_session(request, **kwargs):
    if request.method == 'POST':
        event_form = CourseSessionForm(request.POST, instance=Event())
        rule_form = RecurrenceRuleForm(request.POST, instance=RecurrenceRule())
        if event_form.is_valid():
            event = event_form.save(commit=False)
            event.creator = request.user
            course = get_object_or_404(Course, id=kwargs['course_id'])
            school = get_object_or_404(School, id=course.school_id, members=request.user)
            event.course = course
            event.school = school
            if event.recurring and rule_form.is_valid():
                rule = rule_form.save()
                event.rule = rule
            event.save()
            return HttpResponseRedirect(reverse('view_school_calendar', kwargs={'school_id':school.id}))
    else:
        event_form = CourseSessionForm(instance=Event())
        rule_form = RecurrenceRuleForm(instance=RecurrenceRule())
        return render_to_response('school_calendar/event_form.html', {'event_form':event_form,'rule_form':rule_form}, context_instance=RequestContext(request))
