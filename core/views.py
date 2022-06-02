from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework.views import APIView

from rest_framework import status

from .serializers import PostSerializer, CommentSerializer
from .models import Post, Following, Comment

from account.models import User

class PostPermissions:
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class PostViewSet(PostPermissions, viewsets.ViewSet):
    """ post viewsets 
    """
    serializer_class = PostSerializer
    parser_class = (FileUploadParser,)

    def get_posts(self, *args, **kwargs):
        qs = Post.objects.filter(user=self.request.user)
        following_ids = self.request.user.following.all().values_list('follower__id')
        follow = Post.objects.filter(user__in=following_ids)
        posts = qs | follow
        recent_posts = posts.distinct().order_by('-timestamp')
        serializer = self.serializer_class(recent_posts, user=self.request.user,  many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create_post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailViewset(PostPermissions, viewsets.ViewSet):
    """ Post object view, get and delete functions
    """
    serializer_class = PostSerializer

    def get_detail(self, *args, **kwargs):
        try:
            obj = Post.objects.get(id=kwargs.get('id'))
            serializer = self.serializer_class(obj, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def set_action(self, *args, **kwargs):
        try:
            obj = Post.objects.get(id=kwargs.get('id'))
            action = self.request.data.get('action')
            if action == 'like':
                obj.likes.add(self.request.user)
            elif action == 'unlike':
                obj.likes.remove(self.request.user)
            elif action == 'archive':
                obj.is_archived = True
            obj.save()
            serializer = self.serializer_class(obj, user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class CommentViewSet(APIView):

    serializer_class = CommentSerializer

    def get(self, *args, **kwargs):
        comments = Comment.objects.filter(post__id=kwargs.get('post_id'))
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, *args, **kwargs):
        # Add comment to a post
        post_obj = Post.objects.filter(id=kwargs.get('post_id')).first()
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save(user=self.request.user, post=post_obj)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)