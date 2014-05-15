from django.db import models


class Analysis(models.Model):
    """rying to start an analytics app"""
    name = models.CharField(max_length=20)
    analysis_title = models.CharField(max_length=30)
    user = models.CharField(max_length=30)
    startdatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()
    group = models.CharField(max_length=50)
    active_users_now = models.IntegerField()

    def __str__(self):
        """Name of the model class"""
        return self.name


    class Meta:
        verbose_name_plural = "Analyses"