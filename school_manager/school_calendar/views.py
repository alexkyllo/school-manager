from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import RequestContext, loader
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from school_calendar.models import RecurrenceRule, Event, Occurrence
from schools.models import School
from datetime import datetime
from django.utils.timezone import utc

# Create your views here.

@require_GET
def view_school_calendar(request, **kwargs):
    #now = datetime.now(tz=utc)
    school = School.objects.get(pk=kwargs['school_id'])
    return render_to_response('school_calendar/calendar_view.html', {'school' : school}, context_instance=RequestContext(request))
