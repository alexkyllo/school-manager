#!/school-manager/school_manager/analytics/views.py
"""
This Base view for for the Analytics app will facilitate the
analysis and metrics of this application
"""
from django.shortcuts import render
#from django.template import RequestContext, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

import random
import numpy as np
import pandas as pd

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from schools.models import School  #, Course, Location
from analytics.models import Analysis

def analytics_home(request):
    test_list = Analysis.objects.all()
    context = {'test_list': test_list}
    return render(request, 'analytics/index.html', context)

def model_names(request):
    """ Accepts a model name and returns the fields
    """
    model_names = School._meta.get_all_field_names()
    context = model_names
    return render(request, 'analytics/index.html', context)

def simple_chart(request):
    """
    The first try at creating analytics 
    server side with matplotlib
    """

    # Get the specific model field names that will appear
    # on the X axis    

    # Method 1 - get_all_field_names()
    model_names = School._meta.get_all_field_names()

    # Determine the qty of fields in the model
    num_obj_returned = len(model_names)

    # The chart index, is where the x ticks will be placed
    chart_index = np.arange(num_obj_returned)

    # Populating the Y axis with random numbers 0 - 1000
    y_values = []
    for i in range(num_obj_returned):
        y_values.append(random.randint(0, 100000))

    # Populating the x axis, not the labels, with a numpy array
    # remember - .25 is array based 
    x_values = chart_index - .25

    #####  Chart Styling ######
    chart_height = 4
    chart_length = 5
    chart_label = "First Analytic Chart Label"
    xlabel = "This is the X Label"
    ylabel = "This is the y label"
    display_frame = False
    tight_layout = True
    chart_title_align = 'center'
    xtick_alignment = 'center'

    # Create a figure objectm with tight_layout automatically
    # adjusts subplot(s) fits in to the figure area
    fig = Figure()
    fig.set_tight_layout(tight_layout)
    fig.set_size_inches(chart_length, chart_height)
    fig.set_frameon(display_frame)

    # create an axis, this is 1 row, 1 column, and 1 cell or 111
    ax = fig.add_subplot(111)

    # Actually create the bar chart here
    # in this case, x asis is just 
    ax.bar(x_values, y_values, color='grey', width=.5)

    # this sets the xlim just a little to the right on the y axis
    # and aligns it on the right also
    ax.set_xlim(xmin=-0.25, xmax=num_obj_returned - 0.75)

    # Where the x ticks are placed and set the labels
    ax.set_xticks(chart_index)
    ax.set_xticklabels(model_names, ha=xtick_alignment)

    # Set the chart title
    ax.set_title(chart_label, loc=chart_title_align)
    # Set the x and y axis label
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    # The canvas the figure renders into.  
    # Calls the draw and print fig
    # methods, creates the renderers, etc...
    canvas = FigureCanvas(fig)

    # HttpResponse represents an outgoing HTTP response, 
    # including HTTP headers, cookies and body content
    response = HttpResponse(content_type='image/png')
    canvas.print_png(response)
    return response


class LoginRequiredMixin(object):
    """Simple Mixin to require login for all classes in this view"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class AnalyticsMixin(LoginRequiredMixin, object):
    """Mixin that attaches the Analysis model to classes"""
    model = Analysis

    def get_queryset(self):
        return Analysis.objects.filter(user=self.request.user)
