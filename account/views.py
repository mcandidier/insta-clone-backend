from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView

from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.parsers import FileUploadParser

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserSerializer,
    ChangePasswordSerializer
)

from .models import User
from core.models import Post, Following
from core.serializers import PostSerializer


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

class UserChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.data.get('password')
            user.set_password(password)
            user.save()
            return Response({'message': 'password updated successfully.'}, status=200)
        return Response(serializer.errors, status=400)


class UserViewSet(APIView):
    """ Authenticated user views
    """ 
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=200)


class UserProfileView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    parser_class = (FileUploadParser,)


    def post(self, request, *args, **kwargs):
        # upload user profile photo
        if request.FILES.get('profile_photo'):
            request.user.profile_photo = request.FILES.get('profile_photo')
            request.user.save()
            return Response({'profile_photo': request.user.profile_photo.url}, status=200)
        return Response(status=400)

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=200)

    def delete(self, request, *args, **kwargs):
        request.user.profile_photo.delete()
        return Response(status=204)


class ProfileView(APIView):
    """ Profile View
        lookup username
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, *args, **kwargs):
        username = kwargs.get('username')
        try:
            user = User.objects.get(username=username)
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=200)
        except User.DoesNotExist:
            return Response({}, status=404)

    def post(self, *args, **kwargs):
        # follow user 
        # lookup : username
        action = self.request.data.get('action')
        username = kwargs.get('username')
        user_to_follow = User.objects.filter(username=username)
        if user_to_follow.exists():
            user = user_to_follow.first()
            if action == 'follow':
                Following.objects.create(
                    user=self.request.user,
                    follower=user
                )
            else:
                Following.objects.filter(follower__username=username).delete()
            return Response({'id': user.id}, status=200)
        return Response({'msg': 'User does not exists'}, status=400)


class ProfilePostView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get('username', '')
        user = User.objects.filter(username=username).first()
        queryset = Post.objects.filter(user=user)
        serializer = self.serializer_class(queryset, many=True, user=user)
        return Response(serializer.data, status=200)