from django.db import models

class Bibliotecary(models.Model):
    """Modelo que representa a un bibliotecario.
    
    Los bibliotecarios gestionan los préstamos y tienen permisos
    especiales en el sistema.
    """
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)

    def __str__(self):
        """Retorna el nombre de usuario del bibliotecario."""
        return self.username

