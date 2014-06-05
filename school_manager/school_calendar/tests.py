from django.test import TestCase
from django.test.client import Client
from school_calendar.models import *
from django.contrib.auth.models import User
from dateutil.rrule import *
from datetime import datetime
from django.utils.timezone import utc
# Create your tests here.

class TestCalendarModels(TestCase):
    fixtures = ['users.json','groups.json', 'school_calendar/fixtures.json']
    def setUp(self):
        pass

    def test_event_get_occurrences(self):
        creator = User.objects.create_user(username='alex', first_name="Alex", last_name="Kyllo", password='42')
        mondays_at_noon = RecurrenceRule.objects.create(name='Mondays', frequency='WEEKLY', params={'byweekday':MO})
        event = Event.objects.create(creator=creator, rule=mondays_at_noon, startdatetime=datetime(2014,6,2,12,0,0, tzinfo=utc), enddatetime=datetime(2014,6,2,13,0,0, tzinfo=utc))
        self.assertEqual(event.get_occurrences(datetime(2014,6,4,0,0,0, tzinfo=utc),datetime(2014,6,11,0,0,0, tzinfo=utc))[0],datetime(2014,6,9,12,0,0, tzinfo=utc))

    def test_event_get_month_occurrences(self):
        event = Event.objects.get(name='Test Event')
        month_occurrences = event.get_month_event_occurrences(year=2014, month=6)
        print(month_occurrences)
        self.assertTrue(datetime(2014,6,9,12,0, tzinfo=utc) in month_occurrences)

