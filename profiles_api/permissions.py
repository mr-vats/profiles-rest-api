#This is gonna provide us base class that we can use to create custom permision class
from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """ Allow users to edit their own profile"""
    #has object permission function to class, which is called everytime request is made to API that we assign our permission to.
    #This function will return true/False to determine that the user has permision to update the profile
    #obj: actual object against which we are Checking permission
    #We are gonna allow users to view other user profile

    def has_object_permission(self,request,view,obj):
        """Check user is trying to edit their own profile"""
        #safe method :HTTP GET
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""
    #USer should update their own feed items

    def has_object_permission(self,request,view,obj):
        """Check the user which is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.user_profile.id == request.user.id
