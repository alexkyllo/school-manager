from django.test import TestCase
from schools.models import *
from datetime import datetime, timedelta
from django.utils.timezone import utc


# Create your tests here.

class TestModelRelations(TestCase):
    def setUp(self):
        cool_school = School.objects.create(name="A Cool School")
        cool_school_location = Location.objects.create(school=cool_school, name="Kirkland")
        john_doe_user = User.objects.create_user('johndoe','johndoe@johndoe.com','password')
        jane_doe_user = User.objects.create_user('janedoe','janedoe@janedoe.com','password')
        bob_loblaw_user = User.objects.create_user('bobloblaw','bob@loblaw.com','password')
        cool_school_instructor = Person.objects.create(user=john_doe_user, first_name="John", last_name="Doe")
        cool_school_student_1 = Person.objects.create(user=jane_doe_user, first_name="Jane", last_name="Doe")
        cool_school_student_2 = Person.objects.create(user=bob_loblaw_user, first_name="Bob", last_name="Loblaw")
        cool_school_course = Course.objects.create(name="Yoga 101", location=cool_school_location)
        cool_school_course.instructors.add(cool_school_instructor)
        cool_school_course.students.add(cool_school_student_1)
        dt = datetime(2014, 5, 9, 5, 35, 5, 730613)
        cool_school_course_session = Session.objects.create(course=cool_school_course, startdatetime=dt, enddatetime=dt+timedelta(hours=1))
        cool_school_course_session.students.add(cool_school_student_1)
        cool_school_course_session.students.add(cool_school_student_2)

    def testSchoolHasLocation(self):
        cool_school = School.objects.get(name="A Cool School")
        location = Location.objects.get(name="Kirkland")
        self.assertEqual(location.school, cool_school)
        self.assertEqual(str(location),"Kirkland")

    def testLocationHasCourse(self):
        cool_school_course = Course.objects.get(name="Yoga 101")
        cool_school_location = Location.objects.get(name="Kirkland")
        self.assertEqual(cool_school_course.location,cool_school_location)
        self.assertEqual(str(cool_school_course),"Yoga 101")

    def testCourseHasStudentAndInstructor(self):
        cool_school_course = Course.objects.get(name="Yoga 101")
        cool_school_instructor = Person.objects.get(first_name="John", last_name="Doe")
        cool_school_student = Person.objects.get(first_name="Jane", last_name="Doe")

        self.assertTrue(cool_school_instructor in cool_school_course.instructors.all())
        self.assertTrue(cool_school_student in cool_school_course.students.all())
        self.assertEqual(str(cool_school_student), "Jane Doe")
        self.assertEqual(str(cool_school_instructor), "John Doe")

    def testSessionHasStudents(self):
        cool_school_course_session = Session.objects.get(pk=1)
        cool_school_student_1 = Person.objects.get(first_name="Jane", last_name="Doe")
        cool_school_student_2 = Person.objects.get(first_name="Bob", last_name="Loblaw")
        self.assertTrue(cool_school_student_1 in cool_school_course_session.students.all())
        self.assertTrue(cool_school_student_2 in cool_school_course_session.students.all())

    def testSessionHasDateTime(self):
        cool_school_course_session = Session.objects.get(pk=1)
        self.assertTrue(type(cool_school_course_session.startdatetime) == datetime)
        self.assertEqual(str(cool_school_course_session), "Yoga 101 on Friday, May 09 at 05:35:05")
