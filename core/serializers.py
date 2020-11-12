from rest_framework import serializers

from .models import Post

class PostSerializer(serializers.ModelSerializer):
    """ Post object serializers
    """
    username = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'image', 'description', 'user', 'timestamp', 'is_archived', 'username', 'is_like']
        read_only_fields = ['user']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def get_username(self, obj):
        return obj.user.username

    def get_is_like(self, obj):
        return self.user in obj.likes.all()