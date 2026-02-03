from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    UserListView,
    UserCreateView,
    UserDetailView,
    UserUpdateView
)
#ViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Vistas genéricas
    path('generic/users/', UserListView.as_view(), name='user-list-generic'),
    path('generic/users/create/', UserCreateView.as_view(), name='user-create-generic'),
    path('generic/users/<int:pk>/', UserDetailView.as_view(), name='user-detail-generic'),
    path('generic/users/<int:pk>/update/', UserUpdateView.as_view(), name='user-update-generic'),
] + router.urls