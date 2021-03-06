from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
#This is used to retreieve from settings.py file in project settings of our project

class UserProfileManager(BaseUserManager):
    """Manager for users profile"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have Email Address ')

        email = self.normalize_email(email)
        user = self.model(email=email,name=name)

        #AbstractBaseUser.set_password()
        """Password is stored has hash(encrypted)"""
        user.set_password(password)
        """Django can supprt multiple DB, we are using one DB"""
        user.save(using=self.db)

        return user

    def create_superuser(self,email,name,password):
        """Create a new Super user with given details"""
        user = self.create_user(email,name,password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self.db)

        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255,unique=True) #PK
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD ='email' #overriding the field
    REQUIRED_FIELDS =['name']


    def get_full_name(self):
        """ Retrieve full name of user"""
        return self.name

    def retrieve_short_name(self):
        """ Retrieve full name of user"""
        return self.name

    def __str__(self):
        """Return String represenation of user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile Status update"""
    #retrieve the other models details from settings.py
    #Reason : It is better than hard coding
    #on_delete: To let Django know what to do when primary key is removed
    user_profile=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
        )
    status_text = models.CharField(max_length=255)
    created_on =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return model as a String"""
        return self.status_text
