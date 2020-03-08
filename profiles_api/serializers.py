from rest_framework import serializers

from profiles_api import models

class HelloSerializer(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    name=serializers.CharField(max_length=10)

#model Serializer: extra
class UserProfileSerializer(serializers.ModelSerializer):
    """ Serializes a user profile object """

    class Meta:
         model=models.UserProfile
         #list of field we want to work with
         fields=('id','email','name','password')
         extra_kwargs={
         'password':{
            'write_only':True,
            'style':{'input_type':'password'}

         }
         }

    #Once a new object is created with serializer,it will validate the object and then call create function
    #to parse validated data
    def create(self,validated_data):
        """Create and return a new User"""
        user=models.UserProfile.objects.create_user(
        email=validated_data['email'],
        name=validated_data['name'],
        password=validated_data['name']
        )

        return user

    def update(self,instance,validated_data):
        """ Handle updating user account """
        if 'password' in validated_data:
            password=validated_data.pop('password')
            instance.set_password(password)

        return super().update(instance,validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    """Serializes ProfileFeedItem"""

    class Meta:
        #By default Django adds primary key ID to all the models that we create
        #This sets serializer to ProfileFeedItem
        model=models.ProfileFeedItem
        fields=('id','user_profile','status_text','created_on')
        extra_kwargs={'user_profile':{'read_only':True}}
