from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User


class UserModelTest(TestCase):
    """Tests para el modelo User"""
    
    def setUp(self):
        """Configuración inicial para cada test"""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'full_name': 'Test User'
        }
    
    def test_crear_usuario(self):
        """Test: Crear un usuario correctamente"""
        user = User.objects.create(**self.user_data)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.full_name, 'Test User')
    
    def test_usuario_string_representation(self):
        """Test: Representación en string del usuario"""
        user = User.objects.create(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_username_unico(self):
        """Test: Username debe ser único"""
        User.objects.create(**self.user_data)
        
        # Intentar crear otro usuario con el mismo username
        with self.assertRaises(Exception):
            User.objects.create(
                username='testuser',
                email='otro@example.com',
                full_name='Otro Usuario'
            )
    
    def test_email_unico(self):
        """Test: Email debe ser único"""
        User.objects.create(**self.user_data)
        
        # Intentar crear otro usuario con el mismo email
        with self.assertRaises(Exception):
            User.objects.create(
                username='otrousuario',
                email='test@example.com',
                full_name='Otro Usuario'
            )


class UserAPITest(APITestCase):
    """Tests para la API de usuarios"""
    
    def setUp(self):
        """Configuración inicial para cada test de API"""
        self.client = APIClient()
        self.user_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'full_name': 'API User'
        }
        self.user = User.objects.create(**self.user_data)
    
    def test_listar_usuarios(self):
        """Test: GET /users/ - Listar todos los usuarios"""
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['username'], 'apiuser')
    
    def test_obtener_usuario_detalle(self):
        """Test: GET /users/{id}/ - Obtener detalles de un usuario"""
        response = self.client.get(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'apiuser')
        self.assertEqual(response.data['email'], 'api@example.com')
    
    def test_crear_usuario_via_api(self):
        """Test: POST /users/ - Crear un nuevo usuario"""
        new_user_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'full_name': 'New User'
        }
        response = self.client.post('/users/', new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.data['username'], 'newuser')
    
    def test_actualizar_usuario(self):
        """Test: PUT /users/{id}/ - Actualizar un usuario"""
        updated_data = {
            'username': 'apiuser',
            'email': 'api@example.com',
            'full_name': 'Updated User Name'
        }
        response = self.client.put(
            f'/users/{self.user.id}/', 
            updated_data, 
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.full_name, 'Updated User Name')
    
    def test_eliminar_usuario(self):
        """Test: DELETE /users/{id}/ - Eliminar un usuario"""
        response = self.client.delete(f'/users/{self.user.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)
    
    def test_usuario_no_existente(self):
        """Test: GET /users/999/ - Usuario que no existe"""
        response = self.client.get('/users/999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_crear_usuario_sin_datos_requeridos(self):
        """Test: POST /users/ - Intentar crear usuario sin campos requeridos"""
        incomplete_data = {
            'username': 'incompleteuser'
            # Faltan email y full_name
        }
        response = self.client.post('/users/', incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

