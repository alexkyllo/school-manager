from django.db import models
from django.contrib.auth.models import User
from schools.models import School, Course, Location


class Student(models.Model):
    """A view into the world of students"""

    BELT_RANKS = (
        ('WHITE', 'White Belt'),
        ('BLUE', 'Blue Belt'),
        ('PURPLE', 'Purple Belt'),
        ('BLACK', 'Black Belt'),
        ('RED', 'Red Belt'),
    )

    STUDENT_ACTIVITY_TYPE = (
        ('YOGA', 'Yoga Student'),
        ('BJJ', 'Brazilian Jiu-Jitsu'),
    )

    name = models.ForeignKey(User, verbose_name="The students user profile")
    current_affiliation = models.ForeignKey(School, verbose_name="The current school affiliation")
    belt_rank = models.CharField(max_length=10,
                                      choices=BELT_RANKS,
                                      default='WHITE')
    activity_type = models.CharField(max_length=10,
                                      choices=STUDENT_ACTIVITY_TYPE,
                                      default='BJJ')
    last_competition = models.DateTimeField('last competition')
    notes = models.TextField()

    def __str__(self):
        """Name of the model class"""
        return str(self.name) + ' is representing ' + str(self.current_affiliation)

    class Meta:
        verbose_name_plural = "Students"
