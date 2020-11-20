from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer
)

from .models import User

class UserLoginView(APIView):
    """ User login API view
    """ 
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer
    
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(
            data=self.request.data,
            request=self.request
            )
        serializer.is_valid(raise_exception=True)
        return Response({
            'token': serializer.token,
        }, status=200)


class UserRegisterView(APIView):
    """ User Registration using email
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer
    
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({}, status=200)
        return Response(serializer.errors, status=400)
        

class UserViewSet(APIView):
    """ Authenticated user views
    """ 
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=200)
