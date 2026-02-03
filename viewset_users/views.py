from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
from rest_framework import status
from .models import User
from .serializer import UserSerializer
import logging

logger = logging.getLogger(__name__)

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar usuarios.
    
        Proporciona operaciones CRUD completas para el modelo User.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'


# Vistas genéricas basadas en clases

class UserListView(generics.ListAPIView):
    """Vista genérica para listar todos los usuarios"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateView(generics.CreateAPIView):
    """Vista genérica para crear un usuario"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveAPIView):
    """Vista genérica para obtener detalles de un usuario"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'


class UserUpdateView(generics.UpdateAPIView):
    """Vista genérica para actualizar un usuario"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'
