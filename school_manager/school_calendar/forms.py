from django import forms
from school_calendar.models import *
from school_calendar.widgets import *
from school_calendar.fields import *
from dateutil import rrule

DAY_CHOICES = (
    (MO,"Monday"),
    (TU,"Tuesday"),
    (WE,"Wednesday"),
    (TH,"Thursday"),
    (FR,"Friday" ),
    (SA,"Saturday"),
    (SU,"Sunday"),
)

#class RecurrenceRuleForm(forms.ModelForm):
#    params = RecurrenceRuleParamsField(
#        label="Recurrence", 
#        required=False, 
#        widget=RecurrenceRuleParamsWidget(
#            [
#                forms.CheckboxSelectMultiple(choices=DAY_CHOICES),
#                SelectDateWidget(),
#            ]
#       )
#    )
#    class Meta:
#        model = RecurrenceRule
#        exclude = ('name',)

class RuleForm(forms.ModelForm):
    byweekday = forms.MultipleChoiceField(label="Recur on weekdays", required=False, widget=forms.CheckboxSelectMultiple(), choices=DAY_CHOICES)
    until = forms.DateField(label="Recur until", required=False, widget=SelectDateWidget())
    class Meta:
        model = Rule
        exclude = ('name',)

class EventForm(forms.ModelForm):
    startdatetime = forms.SplitDateTimeField(label="Start Date/Time", required=True, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    enddatetime = forms.SplitDateTimeField(label="End Date/Time", required=False, widget=DateTimeWidget([SelectDateWidget, forms.TimeInput,]))
    class Meta:
        model = Event
        exclude = ('school','attendees','creator','rule')

class CourseSessionForm(EventForm):
    class Meta:
        model = Event
        exclude = ('name','course','school','attendees','creator','rule')
