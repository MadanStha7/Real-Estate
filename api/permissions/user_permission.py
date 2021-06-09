from user.models import AgentDetail, UserProfile, AdminProfile
from django.contrib.auth.models import Group
from rest_framework import permissions


class UserIsAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False


class UserIsAdmin(permissions.BasePermission):
    """
    if the user here is an admin member.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name="Admin"):
            return True
        return False


class UserIsStaffDetail(permissions.BasePermission):
    """
    if the user here is an staff member.
    """

    def has_permission(self, request, view):
        print("has permissions")
        if request.user.is_authenticated and request.user.groups.filter(name="Staff"):
            return True
        # else not permission.has_permission(request, self):

        return False


class UserIsBuyerOrSeller(permissions.BasePermission):
    """
    if the user here is an buyer or seller.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(
            name="BuyerOrSeller"
        ):
            return True
        return False


class UserIsAgentDetail(permissions.BasePermission):
    """
    if the user here is an agent.
    """

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.groups.filter(name="Agent"):
            return True
        return False
