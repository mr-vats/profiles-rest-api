from reset_framework.views import APIView
from reset_framework.response import Response

class HelloApiView(APIView):
    """Test API View"""
    def get(self,request,format=None):
        """Return a list of APIView features"""
        an_apiview=[
        'Uses HTTP methods as function (get,post,patch,put, delete)',
        'IS similar to tradition Django View',
        'Gives you the most control over your App logic',
        'IS mapped manually to URLs',
        ]
        return Response({'message':'Hello Chutad', 'an_apiview':an_apiview})
        
