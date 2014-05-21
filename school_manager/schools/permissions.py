from rest_framework import permissions
from schools.models import School

class IsManager(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to see it.
    Assumes the model instance has a `manager` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        #if request.method in permissions.SAFE_METHODS:            
        #    return True

        # Instance must have an attribute named `manager`.
        return "Managers" in request.user.groups

class IsMember(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user_schools = School.objects.filter(members__id=request.user.id)
        return obj.school in user_schools