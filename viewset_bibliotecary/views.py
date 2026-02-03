from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, generics
from rest_framework import status
from .models import Bibliotecary
from .serializer import BibliotecarySerializer
import logging

logger = logging.getLogger(__name__)

class BibliotecaryViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar bibliotecarios.
    
    Proporciona operaciones CRUD completas y acciones personalizadas
    para obtener préstamos gestionados y estadísticas.
    """
    queryset = Bibliotecary.objects.all()
    serializer_class = BibliotecarySerializer
    lookup_field = 'id'
    
    @action(detail=True, methods=['get'])
    def managed_loans(self, request, id=None):
        """Ver todos los préstamos gestionados por este bibliotecario"""
        bibliotecary = self.get_object()
        from viewset_books.models import Loan
        from viewset_books.serializer import LoanSerializer
        
        loans = Loan.objects.filter(bibliotecary=bibliotecary)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def active_loans(self, request, id=None):
        """Ver préstamos activos gestionados por este bibliotecario"""
        bibliotecary = self.get_object()
        from viewset_books.models import Loan
        from viewset_books.serializer import LoanSerializer
        
        loans = Loan.objects.filter(bibliotecary=bibliotecary, is_active=True)
        serializer = LoanSerializer(loans, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def statistics(self, request, id=None):
        """Estadísticas de préstamos del bibliotecario"""
        bibliotecary = self.get_object()
        from viewset_books.models import Loan
        
        total_loans = Loan.objects.filter(bibliotecary=bibliotecary).count()
        active_loans = Loan.objects.filter(bibliotecary=bibliotecary, is_active=True).count()
        completed_loans = Loan.objects.filter(bibliotecary=bibliotecary, is_active=False).count()
        
        return Response({
            'bibliotecary': bibliotecary.username,
            'total_loans': total_loans,
            'active_loans': active_loans,
            'completed_loans': completed_loans
        })


# Vistas genéricas basadas en clases
class BibliotecaryListView(generics.ListAPIView):
    """Vista genérica para listar todos los bibliotecarios"""
    queryset = Bibliotecary.objects.all()
    serializer_class = BibliotecarySerializer


class BibliotecaryCreateView(generics.CreateAPIView):
    """Vista genérica para crear un bibliotecario"""
    queryset = Bibliotecary.objects.all()
    serializer_class = BibliotecarySerializer


class BibliotecaryDetailView(generics.RetrieveAPIView):
    """Vista genérica para obtener detalles de un bibliotecario"""
    queryset = Bibliotecary.objects.all()
    serializer_class = BibliotecarySerializer
    lookup_field = 'pk'


class BibliotecaryUpdateView(generics.UpdateAPIView):
    """Vista genérica para actualizar un bibliotecario"""
    queryset = Bibliotecary.objects.all()
    serializer_class = BibliotecarySerializer
    lookup_field = 'pk'


