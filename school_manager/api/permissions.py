from rest_framework import permissions
from schools.models import School
from django.contrib.auth.models import User, Group

class IsManager(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to see it.
    Assumes the model instance has a `manager` attribute.
    """

    def has_permission(self, request, view):
        return request.user in User.objects.filter(groups__name='Managers')

class IsManagerOrInstructor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user in User.objects.filter(groups__name__in=('Managers', 'Instructors',))

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_schools = School.objects.filter(members__id=request.user.id)
        if isinstance(obj, School):
            return obj in user_schools
        else:
            return obj.school in user_schools