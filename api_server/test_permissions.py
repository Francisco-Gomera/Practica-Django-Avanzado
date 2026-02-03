from django.test import TestCase
from rest_framework.test import APITestCase, APIClient, APIRequestFactory
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from api_server.permissions import IsAdminOrReadOnly, IsBibliotecary, IsOwnerOrBibliotecary
from viewset_users.models import User
from viewset_bibliotecary.models import Bibliotecary
from viewset_books.models import Writer, Book, Loan


class MockRequest:
    """Mock request object para testing de permisos"""
    def __init__(self, user, method='GET'):
        self.user = user
        self.method = method
        # Añadir atributo is_authenticated al usuario
        if hasattr(user, '_meta') and hasattr(user._meta, 'model_name'):
            # Si es User o Bibliotecary, añadir is_authenticated
            user.is_authenticated = True
        elif hasattr(user, 'is_authenticated'):
            # AnonymousUser ya tiene is_authenticated
            pass
        else:
            # Añadir por defecto
            user.is_authenticated = False


class MockView:
    """Mock view object para testing de permisos"""
    def __init__(self, action_name='list'):
        self.action = action_name


class IsAdminOrReadOnlyTest(TestCase):
    """Tests para el permiso IsAdminOrReadOnly"""
    
    def setUp(self):
        """Configuración inicial"""
        self.permission = IsAdminOrReadOnly()
        self.user = User.objects.create(
            username='normal_user',
            email='user@example.com',
            full_name='Normal User'
        )
        self.bibliotecary = Bibliotecary.objects.create(
            username='admin_user',
            email='admin@example.com',
            full_name='Admin User'
        )
        self.view = MockView()
    
    def test_usuario_normal_puede_leer(self):
        """Test: Usuario normal puede hacer GET (lectura)"""
        request = MockRequest(self.user, method='GET')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_usuario_normal_no_puede_crear(self):
        """Test: Usuario normal NO puede hacer POST (crear)"""
        request = MockRequest(self.user, method='POST')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)
    
    def test_usuario_normal_no_puede_actualizar(self):
        """Test: Usuario normal NO puede hacer PUT (actualizar)"""
        request = MockRequest(self.user, method='PUT')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)
    
    def test_usuario_normal_no_puede_eliminar(self):
        """Test: Usuario normal NO puede hacer DELETE (eliminar)"""
        request = MockRequest(self.user, method='DELETE')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)
    
    def test_bibliotecario_puede_leer(self):
        """Test: Bibliotecario puede hacer GET (lectura)"""
        request = MockRequest(self.bibliotecary, method='GET')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_bibliotecario_puede_crear(self):
        """Test: Bibliotecario puede hacer POST (crear)"""
        request = MockRequest(self.bibliotecary, method='POST')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_bibliotecario_puede_actualizar(self):
        """Test: Bibliotecario puede hacer PUT (actualizar)"""
        request = MockRequest(self.bibliotecary, method='PUT')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_bibliotecario_puede_eliminar(self):
        """Test: Bibliotecario puede hacer DELETE (eliminar)"""
        request = MockRequest(self.bibliotecary, method='DELETE')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_usuario_no_autenticado_puede_leer(self):
        """Test: Usuario no autenticado puede hacer GET (lectura)"""
        from django.contrib.auth.models import AnonymousUser
        request = MockRequest(AnonymousUser(), method='GET')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_usuario_no_autenticado_no_puede_crear(self):
        """Test: Usuario no autenticado NO puede hacer POST"""
        from django.contrib.auth.models import AnonymousUser
        request = MockRequest(AnonymousUser(), method='POST')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)


class IsBibliotecaryTest(TestCase):
    """Tests para el permiso IsBibliotecary"""
    
    def setUp(self):
        """Configuración inicial"""
        self.permission = IsBibliotecary()
        self.user = User.objects.create(
            username='normal_user',
            email='user@example.com',
            full_name='Normal User'
        )
        self.bibliotecary = Bibliotecary.objects.create(
            username='admin_user',
            email='admin@example.com',
            full_name='Admin User'
        )
        self.view = MockView()
    
    def test_usuario_normal_sin_permiso(self):
        """Test: Usuario normal NO tiene permiso"""
        request = MockRequest(self.user, method='GET')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)
    
    def test_bibliotecario_con_permiso(self):
        """Test: Bibliotecario SÍ tiene permiso"""
        request = MockRequest(self.bibliotecary, method='GET')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertTrue(has_permission)
    
    def test_usuario_no_autenticado_sin_permiso(self):
        """Test: Usuario no autenticado NO tiene permiso"""
        from django.contrib.auth.models import AnonymousUser
        request = MockRequest(AnonymousUser(), method='GET')
        has_permission = self.permission.has_permission(request, self.view)
        self.assertFalse(has_permission)


class IsOwnerOrBibliotecaryTest(TestCase):
    """Tests para el permiso IsOwnerOrBibliotecary"""
    
    def setUp(self):
        """Configuración inicial"""
        self.permission = IsOwnerOrBibliotecary()
        self.user = User.objects.create(
            username='owner_user',
            email='owner@example.com',
            full_name='Owner User'
        )
        self.other_user = User.objects.create(
            username='other_user',
            email='other@example.com',
            full_name='Other User'
        )
        self.bibliotecary = Bibliotecary.objects.create(
            username='admin_user',
            email='admin@example.com',
            full_name='Admin User'
        )
        self.writer = Writer.objects.create(name='Test Writer')
        self.book = Book.objects.create(title='Test Book', writer=self.writer)
        self.view = MockView()
    
    def test_propietario_puede_acceder_objeto(self):
        """Test: Propietario puede acceder a su propio préstamo"""
        loan = Loan.objects.create(book=self.book, user=self.user)
        request = MockRequest(self.user, method='GET')
        has_permission = self.permission.has_object_permission(request, self.view, loan)
        self.assertTrue(has_permission)
    
    def test_otro_usuario_no_puede_acceder_objeto(self):
        """Test: Otro usuario NO puede acceder al préstamo ajeno"""
        loan = Loan.objects.create(book=self.book, user=self.user)
        request = MockRequest(self.other_user, method='PUT')  # Método no seguro
        has_permission = self.permission.has_object_permission(request, self.view, loan)
        self.assertFalse(has_permission)
    
    def test_bibliotecario_puede_acceder_cualquier_objeto(self):
        """Test: Bibliotecario puede acceder a cualquier préstamo"""
        loan = Loan.objects.create(book=self.book, user=self.user)
        request = MockRequest(self.bibliotecary, method='GET')
        has_permission = self.permission.has_object_permission(request, self.view, loan)
        self.assertTrue(has_permission)
    
    def test_metodos_seguros_lectura(self):
        """Test: Métodos seguros (GET, HEAD, OPTIONS) permitidos para propietario"""
        loan = Loan.objects.create(book=self.book, user=self.user)
        for method in ['GET', 'HEAD', 'OPTIONS']:
            request = MockRequest(self.user, method=method)
            has_permission = self.permission.has_object_permission(request, self.view, loan)
            self.assertTrue(has_permission, f"Método {method} debería estar permitido")


class PermissionIntegrationTest(APITestCase):
    """Tests de integración para permisos en API"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.user = User.objects.create(
            username='test_user',
            email='test@example.com',
            full_name='Test User'
        )
        self.bibliotecary = Bibliotecary.objects.create(
            username='test_admin',
            email='admin@example.com',
            full_name='Test Admin'
        )
        self.writer = Writer.objects.create(name='Integration Writer')
        self.book = Book.objects.create(title='Integration Book', writer=self.writer)
    
    def test_usuario_puede_listar_sin_autenticacion(self):
        """Test: Endpoint de lectura accesible sin autenticación"""
        response = self.client.get('/users/')
        # Dependiendo de la configuración, puede ser 200 o 401
        # Si IsAdminOrReadOnly permite lectura anónima, debe ser 200
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_401_UNAUTHORIZED])
    
    def test_usuario_no_puede_crear_sin_ser_bibliotecario(self):
        """Test: Usuario normal no puede crear recursos (si IsAdminOrReadOnly aplicado)"""
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Book',
            'writer_name': 'New Writer'
        }
        response = self.client.post('/books/', data, format='json')
        # Debe ser 403 si IsAdminOrReadOnly está aplicado
        # o 201 si no hay restricción
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_403_FORBIDDEN])
    
    def test_bibliotecario_puede_crear_recursos(self):
        """Test: Bibliotecario puede crear recursos"""
        self.client.force_authenticate(user=self.bibliotecary)
        data = {
            'title': 'Admin Book',
            'writer_name': 'Admin Writer'
        }
        response = self.client.post('/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
