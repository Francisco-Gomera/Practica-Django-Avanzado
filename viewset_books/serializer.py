from rest_framework import serializers
from .models import Book, Writer, Loan
from viewset_users.models import User
from viewset_bibliotecary.models import Bibliotecary
from django.utils import timezone

class BookSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Book.
    
    Incluye el nombre del escritor como campo de solo lectura.
    """
    writer_name = serializers.CharField(source='writer.name', read_only=True)

    class Meta:
        model = Book
        fields = 'id', 'title', 'writer_name'
        read_only_fields = 'id',

class WriterSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Writer.
    
    Incluye la lista de libros del escritor anidados.
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Writer
        fields = 'id', 'name', 'books'

class BookCreateSerializer(serializers.ModelSerializer):
    """Serializer especializado para la creación de libros.
    
    Permite crear libros usando el nombre del escritor en lugar del ID.
    Si el escritor no existe, se crea automáticamente.
    """
    writer_name = serializers.CharField(write_only=True)

    class Meta:
        model = Book
        fields = 'id', 'title', 'writer_name'
        read_only_fields = 'id',
    
    def create(self, validated_data):
        """Crea un libro y su escritor si no existe.
        
        Args:
            validated_data: Datos validados que incluyen title y writer_name
            
        Returns:
            Book: El libro creado
        """
        writer_name = validated_data.pop('writer_name')
        writer, created = Writer.objects.get_or_create(name=writer_name)
        book = Book.objects.create(writer=writer, **validated_data)
        return book

class LoanSerializer(serializers.ModelSerializer):
    """Serializer para el modelo Loan.
    
    Proporciona campos para escribir IDs y campos de solo lectura
    para mostrar nombres y títulos relacionados.
    """
    book_title = serializers.CharField(source='book.title', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    bibliotecary_name = serializers.CharField(source='bibliotecary.username', read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    bibliotecary_id = serializers.PrimaryKeyRelatedField(
        queryset=Bibliotecary.objects.all(), 
        source='bibliotecary', write_only=True, required=False
    )

    class Meta:
        model = Loan
        fields = ['id', 'book_id', 'user_id', 'bibliotecary_id', 'book_title', 
                'user_username', 'bibliotecary_name', 'loan_date', 'return_date', 'is_active']
        read_only_fields = ['id', 'loan_date', 'return_date']
    
    def create(self, validated_data):
        """Crea un nuevo préstamo con estado activo.
        
        Args:
            validated_data: Datos validados del préstamo
            
        Returns:
            Loan: El préstamo creado
        """
        validated_data['is_active'] = True
        validated_data['return_date'] = None
        return super().create(validated_data)

class LoanReturnSerializer(serializers.ModelSerializer):
    """Serializer para gestionar la devolución de préstamos.
    
    Solo expone campos de solo lectura para mostrar el estado
    de devolución de un préstamo.
    """
    class Meta:
        model = Loan
        fields = ['id', 'return_date', 'is_active']
        read_only_fields = ['id', 'return_date', 'is_active']