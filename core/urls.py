from django.urls import path
from .views import (
    PostViewSet,
    PostDetailViewset
) 

urlpatterns = [
    path('', PostViewSet.as_view({'get': 'get_posts', 'post': 'create_post'})),
    path('<int:id>/', PostDetailViewset.as_view({'get': 'get_detail', 'post': 'set_action'})),
]
