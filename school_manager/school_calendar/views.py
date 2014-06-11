from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from school_calendar.models import RecurrenceRule, Event, Occurrence
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
    #now = datetime.now()
    school = School.objects.get(pk=kwargs['school_id'])
    return render_to_response('school_calendar/calendar_view.html', {'school' : school}, context_instance=RequestContext(request))

@require_GET
def view_all_events_between(request, **kwargs):
    '''
    This view is for the jquery-ui fullcalendar widget. Takes a GET request with a date range and returns all events inside the range
    in the JSON format that fullcalendar is expecting.
    '''
    events = Event.objects.all()
    startdatetime = parser.parse(request.GET['start']+'T00:00:00.0+00:00')
    enddatetime = parser.parse(request.GET['end']+'T00:00:00.0+00:00')
    event_occurrences = [event.get_event_occurrences(startdatetime, enddatetime) for event in events]
    event_occurrences_flat = [item for sublist in event_occurrences for item in sublist] #flatten the list of lists of events
    fullcalendar_events = [event_to_fullcalendar(event) for event in event_occurrences_flat]
    return HttpResponse(json.dumps(fullcalendar_events))
