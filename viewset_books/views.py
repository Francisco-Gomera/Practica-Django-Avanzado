from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action, api_view
from rest_framework import viewsets, generics
from rest_framework import status
from viewset_books.models import Book, Writer, Loan
from viewset_books.serializer import (
    BookSerializer, WriterSerializer, BookCreateSerializer, 
    LoanSerializer, LoanReturnSerializer
)
from viewset_users.models import User
from django.utils import timezone
from django.db.models import Count, Q

class WriterViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar escritores.
    
    Proporciona operaciones CRUD completas para el modelo Writer.
    """
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
    lookup_field = 'id'

class BookViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar libros.
    
    Proporciona operaciones CRUD completas para el modelo Book.
    Usa diferentes serializers para creación y otras operaciones.
    """
    queryset = Book.objects.all()
    lookup_field = 'id'
    
    def get_serializer_class(self):
        """Retorna el serializer apropiado según la acción.
        
        Returns:
            BookCreateSerializer para creación, BookSerializer para el resto
        """
        if self.action == 'create':
            return BookCreateSerializer
        return BookSerializer

class LoanViewSet(viewsets.ModelViewSet):
    """ViewSet para gestionar préstamos de libros.
    
    Proporciona operaciones CRUD completas y acciones personalizadas
    para devolver libros y listar préstamos activos.
    """
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'id'
    
    @action(detail=True, methods=['post'])
    def return_book(self, request, id=None):
        """Registra la devolución de un libro prestado.
        
        Args:
            request: Objeto de petición HTTP
            id: ID del préstamo
            
        Returns:
            Response con los datos actualizados del préstamo o error
        """
        loan = self.get_object()
        if not loan.is_active:
            return Response(
                {'error': 'Este préstamo ya fue devuelto'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        loan.return_date = timezone.now()
        loan.is_active = False
        loan.save()
        
        serializer = self.get_serializer(loan)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Lista todos los préstamos activos.
        
        Args:
            request: Objeto de petición HTTP
            
        Returns:
            Response con la lista de préstamos activos
        """
        active_loans = Loan.objects.filter(is_active=True)
        serializer = self.get_serializer(active_loans, many=True)
        return Response(serializer.data) 


# Vistas genéricas para Writer
class WriterListView(generics.ListAPIView):
    """Vista genérica para listar todos los escritores"""
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer


class WriterCreateView(generics.CreateAPIView):
    """Vista genérica para crear un escritor"""
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer


class WriterDetailView(generics.RetrieveAPIView):
    """Vista genérica para obtener detalles de un escritor"""
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
    lookup_field = 'pk'


class WriterUpdateView(generics.UpdateAPIView):
    """Vista genérica para actualizar un escritor"""
    queryset = Writer.objects.all()
    serializer_class = WriterSerializer
    lookup_field = 'pk'


# Vistas genéricas para Book
class BookListView(generics.ListAPIView):
    """Vista genérica para listar todos los libros"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookCreateView(generics.CreateAPIView):
    """Vista genérica para crear un libro"""
    queryset = Book.objects.all()
    serializer_class = BookCreateSerializer


class BookDetailView(generics.RetrieveAPIView):
    """Vista genérica para obtener detalles de un libro"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


class BookUpdateView(generics.UpdateAPIView):
    """Vista genérica para actualizar un libro"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'pk'


# Vistas genéricas para Loan
class LoanListView(generics.ListAPIView):
    """Vista genérica para listar todos los préstamos"""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanCreateView(generics.CreateAPIView):
    """Vista genérica para crear un préstamo"""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer


class LoanDetailView(generics.RetrieveAPIView):
    """Vista genérica para obtener detalles de un préstamo"""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'pk'


class LoanUpdateView(generics.UpdateAPIView):
    """Vista genérica para actualizar un préstamo"""
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    lookup_field = 'pk' 


# API Views personalizadas que enlazan modelos
@api_view(['GET'])
def user_loan_history(request, user_id):
    """Vista personalizada que enlaza User con Loan y Book.
    
    Proporciona un historial completo de préstamos de un usuario específico,
    incluyendo información de los libros prestados y estadísticas.
    
    Args:
        request: Objeto de petición HTTP
        user_id: ID del usuario
        
    Returns:
        Response con el historial de préstamos y estadísticas del usuario
    """
    try:
        user = User.objects.get(id=user_id)
        loans = Loan.objects.filter(user=user).select_related('book', 'book__writer', 'bibliotecary')
        
        # Estadísticas
        total_loans = loans.count()
        active_loans = loans.filter(is_active=True).count()
        completed_loans = loans.filter(is_active=False).count()
        
        # Detalle de préstamos
        loan_list = []
        for loan in loans:
            loan_list.append({
                'loan_id': loan.id,
                'book': {
                    'id': loan.book.id,
                    'title': loan.book.title,
                    'writer': loan.book.writer.name
                },
                'bibliotecary': loan.bibliotecary.username if loan.bibliotecary else None,
                'loan_date': loan.loan_date,
                'return_date': loan.return_date,
                'is_active': loan.is_active
            })
        
        data = {
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name
            },
            'statistics': {
                'total_loans': total_loans,
                'active_loans': active_loans,
                'completed_loans': completed_loans
            },
            'loan_history': loan_list
        }
        return Response(data)
    except User.DoesNotExist:
        return Response(
            {'error': 'Usuario no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def book_loan_statistics(request, book_id):
    """Vista personalizada que enlaza Book con Loan y User.
    
    Proporciona estadísticas completas de préstamos de un libro específico,
    incluyendo información de los usuarios que lo han solicitado.
    
    Args:
        request: Objeto de petición HTTP
        book_id: ID del libro
        
    Returns:
        Response con estadísticas de préstamos del libro
    """
    try:
        book = Book.objects.select_related('writer').get(id=book_id)
        loans = Loan.objects.filter(book=book).select_related('user', 'bibliotecary')
        
        # Estadísticas
        total_loans = loans.count()
        active_loans = loans.filter(is_active=True).count()
        completed_loans = loans.filter(is_active=False).count()
        unique_users = loans.values('user').distinct().count()
        
        # Usuarios que han solicitado el libro
        users_list = []
        for loan in loans:
            users_list.append({
                'loan_id': loan.id,
                'user': {
                    'id': loan.user.id,
                    'username': loan.user.username,
                    'email': loan.user.email
                },
                'loan_date': loan.loan_date,
                'return_date': loan.return_date,
                'is_active': loan.is_active,
                'bibliotecary': loan.bibliotecary.username if loan.bibliotecary else None
            })
        
        data = {
            'book': {
                'id': book.id,
                'title': book.title,
                'writer': {
                    'id': book.writer.id,
                    'name': book.writer.name
                }
            },
            'statistics': {
                'total_loans': total_loans,
                'active_loans': active_loans,
                'completed_loans': completed_loans,
                'unique_users': unique_users
            },
            'loan_history': users_list
        }
        return Response(data)
    except Book.DoesNotExist:
        return Response(
            {'error': 'Libro no encontrado'}, 
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def library_statistics(request):
    """Vista personalizada que enlaza todos los modelos principales.
    
    Proporciona estadísticas globales de la biblioteca, enlazando
    Writer, Book, User, Loan y Bibliotecary.
    
    Args:
        request: Objeto de petición HTTP
        
    Returns:
        Response con estadísticas completas de la biblioteca
    """
    from viewset_bibliotecary.models import Bibliotecary
    
    # Estadísticas generales
    total_writers = Writer.objects.count()
    total_books = Book.objects.count()
    total_users = User.objects.count()
    total_bibliotecaries = Bibliotecary.objects.count()
    
    # Estadísticas de préstamos
    total_loans = Loan.objects.count()
    active_loans = Loan.objects.filter(is_active=True).count()
    completed_loans = Loan.objects.filter(is_active=False).count()
    
    # Top 5 libros más prestados
    most_loaned_books = Book.objects.annotate(
        loan_count=Count('loans')
    ).order_by('-loan_count')[:5]
    
    top_books = []
    for book in most_loaned_books:
        top_books.append({
            'id': book.id,
            'title': book.title,
            'writer': book.writer.name,
            'total_loans': book.loan_count
        })
    
    # Top 5 usuarios más activos
    most_active_users = User.objects.annotate(
        loan_count=Count('loans')
    ).order_by('-loan_count')[:5]
    
    top_users = []
    for user in most_active_users:
        top_users.append({
            'id': user.id,
            'username': user.username,
            'total_loans': user.loan_count
        })
    
    # Escritores con más libros prestados
    most_popular_writers = Writer.objects.annotate(
        loan_count=Count('books__loans')
    ).order_by('-loan_count')[:5]
    
    top_writers = []
    for writer in most_popular_writers:
        top_writers.append({
            'id': writer.id,
            'name': writer.name,
            'total_books': writer.books.count(),
            'total_loans': writer.loan_count
        })
    
    data = {
        'catalog': {
            'total_writers': total_writers,
            'total_books': total_books,
            'total_users': total_users,
            'total_bibliotecaries': total_bibliotecaries
        },
        'loans': {
            'total_loans': total_loans,
            'active_loans': active_loans,
            'completed_loans': completed_loans
        },
        'rankings': {
            'top_books': top_books,
            'top_users': top_users,
            'top_writers': top_writers
        }
    }
    return Response(data) 
    