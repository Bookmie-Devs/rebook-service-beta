from agents_app.models import HostelAgent
from rest_framework.permissions import BasePermission
from quick_rooms.models import GuestHouseManager
from hostel_app.models import HostelManagement
"""Custom class to check is user is a manager"""
class IsHostelManager(BasePermission):

    def has_permission(self, request, view):

        # is a user and a manager
        return bool(request.user and request.user.is_hostel_manager)
    

"""Check if user is a hostel worker """
class IsHostelManagement(BasePermission):

    def has_permission(self, request, view):
        try:
            management = HostelManagement.objects.get(user=request.user)
            # is a user and hostel worker/porter
            is_portar = request.user and request.user.is_hostel_worker and management.is_active
            return bool(is_portar or request.user.is_hostel_manager)
        except HostelManagement.DoesNotExist:
            return False

# is a hostel manager
class IsHostelAgent(BasePermission):
    def has_permission(self, request, view):
        try:
            agent = HostelAgent.objects.get(user=request.user)
            # is a user and hostel worker/porter
            return bool(request.user and request.user.is_hostel_agent and agent.is_verified and agent.is_active)
        except HostelAgent.DoesNotExist:
            return False

class IsGuestHouseManager(BasePermission):
    def has_permission(self, request, view):
        try:
            manager = GuestHouseManager.objects.get(user=request.user)
            # is a user and hostel worker/porter
            return bool(request.user and request.user.is_guest_house_manager and manager.is_verified and manager.is_active)
        except GuestHouseManager.DoesNotExist:
            return False



class CanRequestOtpCode(BasePermission):

    def has_permission(self, request, view):
        worker = request.user.is_hostel_agent or request.user.is_hostel_worker or request.user.is_hostel_manager    
        return bool(request.user and worker)