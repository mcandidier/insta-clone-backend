from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """ Post object serializers
    """

    class Meta:
        model = Post
        fields = ['id', 'image', 'description', 'user', 'likes', 'timestamp', 'is_archived']
        read_only_fields = ['user']
