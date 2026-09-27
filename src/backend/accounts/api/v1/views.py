from .serializers import *
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import GenericAPIView,ListAPIView
from rest_framework.views import APIView


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
                max_age= 60 * 60)
            
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
        
            
                

            
class TherapistRegisterApiView(GenericAPIView):
    serializer_class = TherapistRegisterSerializer
    
    def post(self,request):
        serializer= self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Therapist Register Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
            
class PatientRegisterApiView(GenericAPIView):
    serializer_class = PatientRegisterSerializer
    
    def post(self,request):
        serializer= self.serializer_class(data=request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Patient Register Successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
        
        
        
        
class PatientListApiView(ListAPIView):
    serializer_class = PatientSerializers
    queryset = Patient.objects.all()
    
    
    
class TherapistPanelPatientDetailApiView(GenericAPIView):
    serializer_class=PatientSerializers
    
    
    def get_object(self,pk):
        return Patient.objects.get(pk=pk)
    
    
    def get(self,request,pk):
        obj = self.get_object(pk)
        serializer = self.serializer_class(instance=obj,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
        
        
        
        
        
class PatientDetailApiView(GenericAPIView):
    serializer_class= PatientSerializers
    
    
    def get_object(self):
        return Patient.objects.get(user=self.request.user)
    
    
    def get(self,request):
        obj = self.get_object()
        serializer = self.serializer_class(instance = obj,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
        





class TherapistDetailApiView(GenericAPIView):
    serializer_class= TherapistSerializers
    
    def get_object(self):
        return Therapist.objects.get(user=self.request.user)
    
    def get(self,request):
        obj = self.get_object()
        serializer = self.serializer_class(instance = obj,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
        
    
    
    
class ChangePasswordApiView(GenericAPIView):
    serializer_class = ChangePasswordSerializer
    
    def put(self,request):
        serializer = self.serializer_class(data=request.data,context = {'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'password changed successfully'},status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            
            

class JwtRefreshApiView(APIView):
    
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token not found."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)

            access_token = str(refresh.access_token)

            response = Response(
                {"detail": "Token refreshed successfully."},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Strict",
                max_age=60 * 60,
            )

            return response

        except Exception:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
            
            
            


class JwtLogoutApiView(APIView):

    def post(self, request, *args, **kwargs):
        response = Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )

        response.delete_cookie(
            key="access_token",
            samesite="Strict",
        )

        response.delete_cookie(
            key="refresh_token",
            samesite="Strict",
        )

        return response

