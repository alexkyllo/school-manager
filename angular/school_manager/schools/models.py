from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.utils.text import slugify
from django.core.urlresolvers import reverse

class School(models.Model):
    '''
    A School instance is the overarching model for organizing all of the information related to the school being managed.
    :name: The name of the school.
    :members: A ManyToMany relation to User (django.contrib.auth.models.User) instances.
    '''
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(User)
    #slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('school_detail', args=[str(self.id)])

    #def save(self, *args, **kwargs):
    #    self.slug = slugify(self.name)
    #    super(School, self).save(*args, **kwargs)

class Location(models.Model):
    school = models.ForeignKey(School, related_name='locations')
    name = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=4)
    zip_postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=2)

    def __str__(self):
        return self.name    

    def get_absolute_url(self):
        return reverse('location_detail', args=[str(self.id)])

class Course(models.Model):
    school = models.ForeignKey(School)
    location = models.ForeignKey(Location, related_name='courses')
    name = models.CharField(max_length=50)
    instructors = models.ManyToManyField(User, related_name="course_instructors")
    students = models.ManyToManyField(User, related_name="course_students")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course_detail', args=[str(self.id)])

class Session(models.Model):
    #This will be replaced by Event model in the school_calendar app.
    #A Session will just be a recurring Event related to a Course.
    school = models.ForeignKey(School)
    course = models.ForeignKey(Course)
    students = models.ManyToManyField(User)
    startdatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()

    def __str__(self):
        startdatetime = timezone.localtime(self.startdatetime)
        return self.course.name + " on " + startdatetime.strftime("%A, %B %d at %X")

    def get_absolute_url(self):
        return reverse('session_detail', args=[str(self.id)])
