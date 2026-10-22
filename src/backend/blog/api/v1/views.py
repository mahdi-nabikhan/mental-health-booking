from rest_framework import generics
from.serializers import (BlogSerializer,BlogStatusUpdateSerializer,BlogCreationSerializer)
from rest_framework.response import Response
from rest_framework import status
from blog import models
from rest_framework.permissions import IsAuthenticated


class BlogListApiView(generics.ListAPIView):
    serializer_class=BlogSerializer
    
    def get_queryset(self):
        return models.Blog.objects.all()
    
    
    
class BlogDetailApiView(generics.RetrieveAPIView):
    serializer_class= BlogSerializer
    queryset = models.Blog.objects.all()
    
class BlogCreateApiView(generics.GenericAPIView):
    serializer_class = BlogCreationSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self,request):
        serializer = self.serializer_class(data= request.data,context={'request':request})
        if serializer.is_valid():
            serializer.save()
            return Response(data={'message':'blog added successfully'},status=status.HTTP_201_CREATED)
        else:
            return Response(data={serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        
        
class BlogUpdatedAPiView(generics.UpdateAPIView,generics.DestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Blog.objects.filter(owner__user =self.request.user)
    
    
class BlogUpdatedStatusApiView(generics.UpdateAPIView):
    serializer_class =BlogStatusUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    
    
    def get_queryset(self):
        return models.Blog.objects.filter(owner__user =self.request.user)
    