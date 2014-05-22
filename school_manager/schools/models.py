from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save


class School(models.Model):
    name = models.CharField(max_length=80)
    members = models.ManyToManyField(User)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('school_detail', args=[str(self.id)])

class Location(models.Model):
    school = models.ForeignKey(School, related_name='locations')
    name = models.CharField(max_length=50)
    address_1 = models.CharField(max_length=50)
    address_2 = models.CharField(max_length=50, null=True)
    city = models.CharField(max_length=50)
    state_province = models.CharField(max_length=4)
    zip_postal_code = models.CharField(max_length=10)
    country = models.CharField(max_length=2)

    def __str__(self):
        return self.name    

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
    
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
        from django.core.urlresolvers import reverse
    
        return reverse('school_location_course_detail', args=[str(self.location.school.id), str(self.location.id), str(self.id)])

class Session(models.Model):
    school = models.ForeignKey(School)
    course = models.ForeignKey(Course)
    students = models.ManyToManyField(User)
    startdatetime = models.DateTimeField()
    enddatetime = models.DateTimeField()


    def __str__(self):
        startdatetime = timezone.localtime(self.startdatetime)
        return self.course.name + " on " + startdatetime.strftime("%A, %B %d at %X")
