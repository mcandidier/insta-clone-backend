from django.urls import path, include

from .views import (
    UserRegisterView,
    UserLoginView
) 

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegisterView.as_view(), name='register'),
]

