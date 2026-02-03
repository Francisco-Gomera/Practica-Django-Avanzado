from django.db import models
from viewset_users.models import User

class Writer(models.Model):
    """Modelo que representa a un escritor/autor de libros."""
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        """Retorna el nombre del escritor."""
        return self.name

class Book(models.Model):
    """Modelo que representa un libro con su título y escritor asociado."""
    title = models.CharField(max_length=200, unique=True)
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, related_name='books')
    

    def __str__(self):
        """Retorna el título del libro y su autor."""
        return f"{self.title} by {self.writer.name}"

class Loan(models.Model):
    """Modelo que representa el préstamo de un libro a un usuario.
    
    Registra la información del préstamo incluyendo el libro prestado,
    el usuario que lo solicitó, el bibliotecario que gestionó el préstamo,
    las fechas de préstamo y devolución, y el estado activo.
    """
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='loans')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    bibliotecary = models.ForeignKey('viewset_bibliotecary.Bibliotecary', on_delete=models.SET_NULL, 
    null=True, blank=True, related_name='managed_loans')
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-loan_date']
    
    def __str__(self):
        """Retorna una representación del préstamo con libro, usuario y estado."""
        status = "Activo" if self.is_active else "Devuelto"
        return f"{self.book.title} - {self.user.username} ({status})"



