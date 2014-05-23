# CBVs for API Viewsets
from rest_framework import viewsets, permissions
from api.permissions import IsManager, IsMember
from api.serializers import (
    UserSerializer, GroupSerializer, SchoolSerializer, LocationSerializer, CourseSerializer,
)
from django.contrib.auth.models import User, Group
from schools.models import School, Location, Course, Session

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    model = User
    serializer_class = UserSerializer
    permission_classes = (IsManager,)

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsManager,)

class SchoolViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows schools to be viewed or edited.
    """
    model = School
    serializer_class = SchoolSerializer
    permission_classes = (IsManager, IsMember,)
    def pre_save(self, obj):
        obj.members += self.request.user

    def get_queryset(self):
        return School.objects.filter(members=self.request.user)

class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows locations to be viewed or edited.
    """
    model = Location
    permission_classes = (IsMember,)
    serializer_class = LocationSerializer
    def get_queryset(self):
        return Location.objects.filter(school__members=self.request.user)

class CourseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Courses to be viewed or edited.
    """
    model = Course
    permission_classes = (IsMember,)
    serializer_class = CourseSerializer
    def get_queryset(self):
        return Course.objects.filter(location__school__members=self.request.user)

class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users in the Students group to be viewed or edited.
    """
    model = User
    permission_classes = (IsManager, IsMember,)
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(groups__name='Students', school__members=self.request.user)

class InstructorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Users in the Students group to be viewed or edited.
    """
    model = User
    permission_classes = (IsManager,)
    serializer_class = UserSerializer
    def get_queryset(self):
        return User.objects.filter(groups__name='Instructors', school__members=self.request.user)