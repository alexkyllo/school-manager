from school_calendar.models import Event
from datetime import datetime
#import json

def event_to_fullcalendar(event):
	if (isinstance(event, Event) == False):
		raise Exception("Positional argument 'event' must be an Event model object")

	event_dict = {}
	event_dict['id'] = event.id
	event_dict['title'] = event.name
	event_dict['allDay'] = event.allday
	event_dict['start'] = event.startdatetime.isoformat()
	event_dict['end'] = event.enddatetime.isoformat()

	return event_dict