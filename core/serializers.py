from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """ Post object serializers
    """
    is_like = serializers.SerializerMethodField(read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'image', 'description', 'user', 'timestamp', 'is_archived', 'is_like']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def get_is_like(self, obj):
        return self.user in obj.likes.all()
