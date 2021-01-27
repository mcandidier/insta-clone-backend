from django.conf import settings
from django.contrib.auth import authenticate
import django.contrib.auth.password_validation as validators
from django.utils.translation import ugettext_lazy as _
from django.core import exceptions


from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import User
from core.models import Following


class FollowingSerializer(serializers.ModelSerializer):
    """ User Following
    """
    class Meta:
        model = Following
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    followers = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'profile_photo', 'bio', 'followers', 'following']
        # extra_kwargs = {'username': {'required': False}} 


    def get_followers(self, obj):
        return obj.followers.all().values_list('user__id', flat=True)

    def get_following(self, obj):
        return obj.following.all().values_list('follower__id', flat=True)


class UserRegistrationSerializer(serializers.Serializer):
    """ User Registration using email
    """
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.is_active = True
        user.save()
        return user

    def validate_email(self, value):
        users = User.objects.filter(email=value)
        if users.exists():
            raise serializers.ValidationError("User already exist")
        return value

    def validate_username(self, value):
        users = User.objects.filter(username=value)
        if users.exists():
            raise serializers.ValidationError("User already exist using that username")
        return value

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords don't match.")
        return data


class UserLoginSerializer(serializers.Serializer):
    """ Usere login serializer
    """
    token = None
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        return super(UserLoginSerializer, self).__init__(*args, **kwargs)

    def validate(self, data):
        email, password = data.values()
        user = authenticate(self.request, email=email, password=password)
        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise serializers.ValidationError(msg, code='authorization')
        self._create_token(user)
        return data

    def _create_token(self, user):
        token = Token.objects.filter(user=user)
        if token.exists():
            token.delete()
        token = Token.objects.create(user=user)
        self.token = token.key
        return token


class ChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate_password(self, value):
        try:
            validators.validate_password(value)
        except exceptions.ValidationError as exc:
            errors = list(exc)
            raise serializers.ValidationError(errors)
        return value

    def validate_confirm_password(self, value):
        password = self.get_initial().get('password')
        if value != password: 
            raise serializers.ValidationError("Passwords don't match")
        return value