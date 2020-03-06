from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status #list of http status codes we can use while returning response

from profiles_api import Serializes



class HelloApiView(APIView):
    """Test API View"""

    serializer_class =Serializer.HelloSerializer
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
