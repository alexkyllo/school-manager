from django.db import models
from django.contrib.auth.models import User
from schools.models import School, Course, Location


class Analysis(models.Model):
    """rying to start an analytics app"""
    user = models.ForeignKey(User, verbose_name="The user who runs the analysis")
    #school = models.ForeignKey(School, verbose_name="The schools being analyzed")
    #courses = models.ForeignKey(Course, verbose_name="The courses being analyzed")
    #locations = models.ForeignKey(Location, verbose_name="The locations being analyzed")
    #analytics_group = models.CharField(max_length=50)
    active_users_now = models.IntegerField()

    def __str__(self):
        """Name of the model class"""
        return str(self.active_users_now) + ' active user right now'

    def create_analysis(self):
        return 'Hello World'

    def current_date(self):
        return 'Hello World'

    class Meta:
        verbose_name_plural = "Analyses"

    def save(self, auser, *args, **kwargs):
        self.active_users_now = User.objects.all().count()
        self.user = auser
        super(Analysis, self).save(*args, **kwargs)

