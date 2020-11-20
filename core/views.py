from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView

from rest_framework import status

from .serializers import PostSerializer
from .models import Post

from account.models import User

class PostPermissions:
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


class PostViewSet(viewsets.ViewSet):
    """ post viewsets 
    """
    serializer_class = PostSerializer
    parser_class = (FileUploadParser,)

    def get_posts(self, *args, **kwargs):
        user = User.objects.first()
        qs = Post.objects.all()
        serializer = self.serializer_class(qs,  user=user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            #FORCE to select first user since we don't have authentication on frontend
            serializer.save(user=User.objects.first())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailViewset(viewsets.ViewSet, PostPermissions):
    """ Post object view, get and delete functions
    """
    serializer_class = PostSerializer

    def get_detail(self, *args, **kwargs):
        try:
            obj = Post.objects.get(id=kwargs.get('id'))
            serializer = self.serializer_class(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def set_action(self, *args, **kwargs):
        user = User.objects.first()
        try:
            obj = Post.objects.get(id=kwargs.get('id'))
            action = self.request.data.get('action')
            if action == 'like':
                obj.likes.add(user) #to be remove
                # obj.likes.add(self.request.user)
            elif action == 'unlike':
                # obj.likes.remove(self.request.user)
                obj.likes.remove(user)
            elif action == 'archive':
                obj.is_archived = True
            obj.save()
            serializer = self.serializer_class(obj, user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)