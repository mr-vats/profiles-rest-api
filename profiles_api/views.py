from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #list of http status codes we can use while returning response
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication #USer authtoken: generate random token string, add in request
from rest_framework import filters
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated
#ObtainAuthToken-> view that comes with DRF that generates auth token

from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.contrib.auth.models import User


from profiles_api import serializers
from profiles_api import models
from profiles_api import permissions



class HelloApiView(APIView):
    """Test API View"""

    serializer_class =serializers.HelloSerializer
    def get(self,request,format=None):
        """Return a list of APIView features"""
        an_apiview=[
        'Uses HTTP methods as function (get,post,patch,put, delete)',
        'IS similar to tradition Django View',
        'Gives you the most control over your App logic',
        'IS mapped manually to URLs',
        ]
        return Response({'message':'Hello Chutad', 'an_apiview':an_apiview})

    def post(self,request):
        """Create a Hello message with name"""
        serializer=self.serializer_class(data=request.data)

        #Validating the serializer object
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message=f'Hello {name}'
            return Response({'message':message})

        else:
            """ If Invalid input, then return HTTP status code 400 for Bad request
                By, Default 200 is returned                                     """
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )

    #To Update the object
    def put(self,request,pk=None):
        """Handle Update an Object"""
        """ pk stands for id of the object to be updated"""
        """ Replacing entire object"""
        return Response({'method':'PUT'})


    def patch(self,request,pk=None):
        """HAndle a Partial Update of an Object"""
        """Changes only passed values"""
        return Response({'method':'PATCH'})

    def delete(Self,request,pk=None):
        """Handle deletion of object"""

        return Response({'method':'DELETE'})


class HelloViewSet(viewsets.ViewSet):
    """ TEst API ViewSet"""
    serializer_class =serializers.HelloSerializer

    def list(self,request):
        """ Return a Hello Message"""
        as_viewset=[
        'UserActions(list,create,retreieve,update,partial_update)',
        'Automatically maps to URLs using Routers',
        'Provide more functionality with less code',

        ]
        return Response({'message':'HEllo','as_viewset':as_viewset})

    def create(self,request):
        """Create a new hello message"""
        serializer=self.serializer_class(data=request.data)

        if serializer.is_valid():
            name=serializer.validated_data.get('name')
            message=f'Hello {name}!'
            return Response({'message':message},status=status.HTTP_200_OK)

        else:
            return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
            )


    def retrieve(self,request,pk=None):
        """Handle getting an object by its ID"""
        return Response({'http_method':'GET'})

    def update(self,request,pk=None):
        """Handle updating an object"""
        return Response({'http_method':'PUT'})

    def partial_update(self,request,pk=None):
        """Handle updating part of object"""
        return Response({'http_method':'PATCH'})

    def destroy(self,request,pk=None):
        """Handle Removing an object"""
        return Response({'http_method':'DELETE'})



class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle Creating and updating profiles"""
    #connect serializer class and provide query set to ModelViewSet
    serializer_class=serializers.UserProfileSerializer
    #list if all UserProfile
    queryset=models.UserProfile.objects.all()
    #Register profile viewset with URL router
    #we want authentication_classes to be Generated as tuple
    #authentication_classes: tell how user will authenticate
    authentication_classes=(TokenAuthentication,)
    #permission classes-> How user will get permission to do certain things
    permission_classes=(permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    #this will tell which fields we have to search with search filter
    search_fields =('name','email',)


class UserLoginApiView(ObtainAuthToken):
    """ Handles creating user authentication tokens"""
    #this ObtainAuthToken ,doesnt enable itself by default
    #we ovveride this class to make it browsable
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating , reading and updating profile feed items"""
    serializer_class=serializers.ProfileFeedItemSerializer
    authentication_classes=(TokenAuthentication,)
    queryset=models.ProfileFeedItem.objects.all()
    permission_classes=(permissions.UpdateOwnStatus,IsAuthenticated)
    #Perform_create for making user_profile as read only

    def perform_create(self,serializer):
        """Sets the user profile to the logged in user"""
        #We are ovveriding djangos perform_create method,
        #Current Behaviour: When a request comes to our ViewSet,
        #it is passed in serializer_class  that is validated and later on serializer.save method is called by default
        #customized logic: This will be called everytime we do http post to our ViewSet

        serializer.save(user_profile=self.request.user)
