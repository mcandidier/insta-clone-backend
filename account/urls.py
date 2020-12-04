from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserRegisterView,
    UserLoginView,
    UserViewSet,
    UserProfileView,
    UserChangePasswordView
)

from core.views import FollowingView

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('current/', UserViewSet.as_view()), #todo: move to profile
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('followers/', FollowingView.as_view(), name='followers')
]

