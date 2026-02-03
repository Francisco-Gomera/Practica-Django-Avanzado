from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Bibliotecarios (admins): pueden hacer todo
    Usuarios normales: solo lectura (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        # Permitir lectura a todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Verificar si es bibliotecario para escritura
        if hasattr(request, 'user') and request.user.is_authenticated:
            from viewset_bibliotecary.models import Bibliotecary
            return Bibliotecary.objects.filter(email=request.user.email).exists()
        
        return False

class IsBibliotecary(permissions.BasePermission):
    """
    Solo bibliotecarios pueden acceder
    """
    def has_permission(self, request, view):
        if hasattr(request, 'user') and request.user.is_authenticated:
            from viewset_bibliotecary.models import Bibliotecary
            return Bibliotecary.objects.filter(email=request.user.email).exists()
        return False

class IsOwnerOrBibliotecary(permissions.BasePermission):
    """
    Usuarios pueden ver/editar sus propios datos
    Bibliotecarios pueden ver/editar todos los datos
    """
    def has_object_permission(self, request, view, obj):
        """Verifica permisos a nivel de objeto.
        
        Args:
            request: Objeto de petición HTTP
            view: Vista que está siendo accedida
            obj: Objeto sobre el cual se verifican permisos
            
        Returns:
            bool: True si tiene permiso, False en caso contrario
        """
        # Lectura permitida para todos
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(request, 'user') and request.user.is_authenticated:
            from viewset_bibliotecary.models import Bibliotecary
            from viewset_users.models import User
            
            # Si es bibliotecario, puede hacer todo
            if Bibliotecary.objects.filter(email=request.user.email).exists():
                return True
            
            # Si es usuario, solo sus propios datos
            if hasattr(obj, 'email'):
                return obj.email == request.user.email
        
        return False
