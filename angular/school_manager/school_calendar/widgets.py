from django import forms
from django.forms.extras.widgets import SelectDateWidget

class DateTimeWidget(forms.MultiWidget):
    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

class RecurrenceRuleParamsWidget(forms.MultiWidget):
	def decompress(self, value):
		if value:
			return [value.byweekday, value.until,]
		return []
