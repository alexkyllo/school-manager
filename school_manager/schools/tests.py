from django.test import TestCase
from schools.models import *

# Create your tests here.

class TestModelRelations(TestCase):
    def setUp(self):
        cool_school = School.objects.create(name="A Cool School")
        cool_school_location = Location.objects.create(school=cool_school, name="Kirkland")
        john_doe_user = User.objects.create_user('johndoe','johndoe@johndoe.com','password')
        jane_doe_user = User.objects.create_user('janedoe','janedoe@janedoe.com','password')
        cool_school_instructor = Person.objects.create(user=john_doe_user, first_name="John", last_name="Doe")
        cool_school_student = Person.objects.create(user=jane_doe_user, first_name="Jane", last_name="Doe")
        cool_school_course = Course.objects.create(name="Yoga 101", location=cool_school_location)
        cool_school_course.instructors.add(cool_school_instructor)
        cool_school_course.students.add(cool_school_student)

    def testSchoolHasLocation(self):
        cool_school = School.objects.get(name="A Cool School")
        location = Location.objects.get(name="Kirkland")
        self.assertEqual(location.school, cool_school)

    def testLocationHasCourse(self):
        cool_school_course = Course.objects.get(name="Yoga 101")
        cool_school_location = Location.objects.get(name="Kirkland")
        self.assertEqual(cool_school_course.location,cool_school_location)

    def testCourseHasStudentAndInstructor(self):
        cool_school_course = Course.objects.get(name="Yoga 101")
        cool_school_instructor = Person.objects.get(first_name="John", last_name="Doe")
        cool_school_student = Person.objects.get(first_name="Jane", last_name="Doe")

        self.assertTrue(cool_school_instructor in cool_school_course.instructors.all())
        self.assertTrue(cool_school_student in cool_school_course.students.all())
        