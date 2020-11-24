from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserRegisterView,
    UserLoginView,
    UserViewSet,
    UserProfileView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('current/', UserViewSet.as_view()), #todo: move to profile
    path('profile/', UserProfileView.as_view(), name='profile'),
]

