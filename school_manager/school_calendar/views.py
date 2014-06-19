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
        event_form = CourseSessionRecurrenceForm(request.POST)
        if event_form.is_valid():
            cleaned_data = event_form.cleaned_data
            course = get_object_or_404(Course, id=kwargs['course_id'])
            school = get_object_or_404(School, id=course.school_id, members=request.user)
            event = Event(
                startdatetime=cleaned_data['startdatetime'],
                enddatetime=cleaned_data['enddatetime'],
                allday=cleaned_data['allday'],
                recurring=cleaned_data['recurring'],
                creator=request.user,
                course=course,
                school=school,
                name=course.name,
            )
            if cleaned_data['recurring']:
                rule = RecurrenceRule(
                    frequency=cleaned_data['frequency'],
                    params={'byweekday':[eval(day) for day in cleaned_data['byweekday']]},
                )
                rule.save()
                event.rule = rule
            event.save()
            return HttpResponseRedirect(reverse('view_school_calendar', kwargs={'school_id':school.id}))
    else:
        event_form = CourseSessionRecurrenceForm()
    return render(request, 'school_calendar/event_form.html', {'event_form':event_form}, context_instance=RequestContext(request))

@require_http_methods(['GET','POST'])
def create_school_event(request, **kwargs):
if request.method == 'POST':
        event_form = CourseSessionRecurrenceForm(request.POST)
        if event_form.is_valid():
            cleaned_data = event_form.cleaned_data
            school = get_object_or_404(School, id=kwargs['school_id'], members=request.user)
            event = Event(
                startdatetime=cleaned_data['startdatetime'],
                enddatetime=cleaned_data['enddatetime'],
                allday=cleaned_data['allday'],
                recurring=cleaned_data['recurring'],
                creator=request.user,
                school=school,
                name=course.name,
            )
            if cleaned_data['recurring']:
                rule = RecurrenceRule(
                    frequency=cleaned_data['frequency'],
                    params={'byweekday':[eval(day) for day in cleaned_data['byweekday']]},
                )
                rule.save()
                event.rule = rule
            event.save()
            return HttpResponseRedirect(reverse('view_school_calendar', kwargs={'school_id':school.id}))
    else:
        event_form = CourseSessionRecurrenceForm()
    return render(request, 'school_calendar/event_form.html', {'event_form':event_form}, context_instance=RequestContext(request))
