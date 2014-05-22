#!/school-manager/school_manager/analytics/views.py
"""
This Base view for for the Analytics app will facilitate the
analysis and metrics of this application
"""
from django.shortcuts import render
#from django.template import RequestContext, loader
#from django.http import HttpResponse, HttpResponseRedirect
from schools.models import School  #, Course, Location
from analytics.models import Analysis
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


def analytics_home(request):
    test_list = Analysis.objects.all()
    context = {'test_list': test_list}
    return render(request, 'analytics/index.html', context)


def simple_chart(request):
    """The first try at creating analytics"""
    import random
    import django
    from schools.models import School
    import numpy as np
    import pandas as pd
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    from django.forms.models import model_to_dict

    # Specific Variables
    filtered_data = School.objects.all().values().exclude(name='Jims') #.filter(name='Jims')
    model_names = School._meta.get_all_field_names()
    ddict = model_to_dict(School.objects.get(pk=1))
    ndict = []
    ndict = ddict.keys
    df = pd.DataFrame.from_records(filtered_data)
    df['y'] = random.randint(0, 1000)
    #df    = df[ df.name != 'Jims']
    h = 5
    w = 8
    x = []
    y = []
    chart_label = "First Analytic Chart Label"
    xlabel = "This is the X Label"
    ylabel = "This is the y label"

    # Get the data from the database
    num_obj_returned = len(model_names)
    chart_index = np.arange(num_obj_returned)

    # Create a figure object
    fig = Figure()
    fig.set_tight_layout(True)
    fig.set_size_inches(w, h)
    fig.set_frameon(False)
    # create an axis
    ax = fig.add_subplot(111)
    new_labels = df.name
    for i in range(num_obj_returned):
        y.append(random.randint(0, 1000))
    # Create a bar chart
    x_var = chart_index - .25
    y_var = y
    ax.bar(x_var, y_var, color='grey', width=.5)
    ax.set_xlim(xmin=-0.25, xmax=num_obj_returned - 0.75)

    # Where the x ticks are placed and set the labels
    ax.set_xticks(chart_index)
    ax.set_xticklabels(model_names, ha='center')
    # Set the chart title
    ax.set_title(chart_label, loc="center")
    # Set the x and y labels
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    canvas = FigureCanvas(fig)
    response = django.http.HttpResponse(content_type='image/png')
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