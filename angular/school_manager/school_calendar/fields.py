from django import forms
from datetime import datetime
from django.forms.util import from_current_timezone

class RecurrenceRuleParamsField(forms.MultiValueField):
    def compress(self, values):
    	if values:
    		untildate = from_current_timezone(datetime(values[1]))
    		return {'byweekday':values[0],'until':untildate}
    	return {}