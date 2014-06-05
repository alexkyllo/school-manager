from django.test import TestCase
from django.test.client import Client
from school_calendar.models import *
from django.contrib.auth.models import User
from dateutil.rrule import *
from datetime import datetime
# Create your tests here.

class TestCalendarModels(TestCase):
    def setUp(self):
        pass

    def testEventCanHaveRecurrenceRule(self):
        creator = User.objects.create_user(username='alex', first_name="Alex", last_name="Kyllo", password='42')
        mondays_at_noon = RecurrenceRule.objects.create(name='Mondays', frequency='WEEKLY', params={'byweekday':MO})
        event = Event.objects.create(creator=creator, rule=mondays_at_noon, startdatetime=datetime(2014,6,2,12,0,0), enddatetime=datetime(2014,6,2,13,0,0))
        self.assertEqual(event.get_occurrences(datetime(2014,6,4,0,0,0),datetime(2014,6,11,0,0,0))[0],datetime(2014,6,9,12,0,0))