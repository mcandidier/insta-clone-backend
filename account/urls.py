from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserRegisterView,
    UserLoginView,
    UserViewSet,
    UserProfileView,
    ProfileView,
    ProfilePostView,
    UserChangePasswordView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('current/', UserViewSet.as_view()), #todo: move to profile
    path('change-password/', UserChangePasswordView.as_view(), name='change_password'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('<str:username>/', ProfileView.as_view(), name='profile_view'),
    path('<str:username>/posts/', ProfilePostView.as_view(), name='profile'),
    path('<str:username>/followers/', ProfileView.as_view(), name='profile_view'),
    path('<str:username>/following/', ProfileView.as_view(), name='profile_view'),
]