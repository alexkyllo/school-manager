from school_calendar.models import *
from django import forms
from django.forms.extras.widgets import SelectDateWidget

class DateTimeWidget(forms.MultiWidget):
    def decompress(self, value):
        if value:
            return [value.date(), value.time().replace(microsecond=0)]
        return [None, None]

class RecurrenceRuleForm(forms.ModelForm):
    class Meta:
        model = RecurrenceRule

class EventForm(forms.ModelForm):
    startdatetime = forms.SplitDateTimeField(label="Start Date/Time", widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    enddatetime = forms.SplitDateTimeField(label="End Date/Time", widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    class Meta:
        model = Event
        exclude = ('school','attendees','creator','rule')

class CourseSessionForm(EventForm):
    class Meta:
        model = Event
        exclude = ('name','course','school','attendees','creator','rule')
