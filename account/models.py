import uuid
from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _

PUBLIC = 0
PRIVATE = 1

PRIVACY_CHOICES = (
    (PUBLIC, 'Public'),
    (PRIVATE, 'Private')
)

class CustomUserManager(BaseUserManager):
    """ Custom user manager
    """

    def _create_user(self, email, password, **extra_fields):
        # Create and saves a User with given email and password

        if not email: 
            raise ValueError('Email is required.')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self._create_user(email, '', **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        # Create and save a superuser

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Custom user where username is email
    """
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=128, null=True)
    first_name = models.CharField(null=True, blank=True, max_length=128)
    last_name = models.CharField(null=True, blank=True, max_length=128)
    profile_photo = models.ImageField(upload_to='profiles/', null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    bio = models.TextField(null=True, blank=True)
    privacy = models.CharField(max_length=1, choices=PRIVACY_CHOICES, default=PUBLIC)


    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=False,
        help_text = _('Designates whether this user is active'),
    )
    is_superuser = models.BooleanField(
        _('super user'),
        default=False,
        help_text="Designates whether the user is super user or site admin")

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ('first_name', 'last_name')
    
    objects  = CustomUserManager()

    def __str__(self):
        return f'{self.email}'


class ResetPassword(models.Model):
    """ Reset password for user
    """ 
    email = models.EmailField()
    date_created = models.DateTimeField(auto_now_add=True)
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email}'


    def is_expired(self):
        pass
