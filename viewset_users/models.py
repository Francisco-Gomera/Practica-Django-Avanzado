from django.db import models

# Create your models here.
class User(models.Model):
    """Modelo que representa a un usuario del sistema.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)

    def __str__(self):
        """Retorna el nombre de usuario."""
        return self.username