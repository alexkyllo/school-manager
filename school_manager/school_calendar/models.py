from django.db import models
from dateutil.rrule import *
from datetime import datetime
import pickle

# Create your models here.

FREQUENCY_CHOICES = (
	('YEARLY','yearly'),
	('MONTHLY','monthly'),
	('WEEKLY','weekly'),
	('DAILY','daily'),
	('HOURLY','hourly'),
	('MINUTELY','every minute'),
	('SECONDLY','every second'),
)

class RecurrenceRule(models.Model):
	name = models.CharField(max_length=32)
	frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
	params = models.BinaryField(blank=True)
	def get_params(self):
		if self.params:
			return pickle.loads(self.params)

	def __unicode__(self):
		return self.name