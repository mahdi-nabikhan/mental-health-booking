from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import *
from rest_framework.response import Response
from rest_framework import status
class JwtLoginApiView(TokenObtainPairView):
    serializer_class = CustomObtainPairTokenSerializer
    
    
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data= request.data)
        if serializer.is_valid():
            user = serializer.user
            data = serializer.validated_data
            access_token = data['access']
            refresh_token = data['refresh']
            redirect_url = None
            
            
            if Therapist.objects.filter(user=user).exists():
                redirect_url = 'therapist'
                
            response = Response({'user_id':user.id,'redirect_url':redirect_url},status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age= 60 * 15)
            
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age= 60 *60*24* 7)
            return response
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        
            
            
            

            
            