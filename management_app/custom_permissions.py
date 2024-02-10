
from rest_framework.permissions import BasePermission


"""Custom class to check is user is a manager"""
class IsHostelManager(BasePermission):

    def has_permission(self, request, view):

        # is a user and a manager
        return bool(request.user and request.user.is_hostel_manager)
    

"""Check if user is a hostel worker """
class IsHostelPortar(BasePermission):

    def has_permission(self, request, view):

        # is a user and hostel worker/porter
        return bool(request.user and request.user.is_hostel_worker)

# is a hostel agent
class IsHostelAgent(BasePermission):

    def has_permission(self, request, view):
        # is a user and hostel worker/porter
        return bool(request.user and request.user.is_hostel_agent)