from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from .models import Bibliotecary
from viewset_books.models import Writer, Book, Loan
from viewset_users.models import User


class BibliotecaryModelTest(TestCase):
    """Tests para el modelo Bibliotecary"""
    
    def test_crear_bibliotecario(self):
        """Test: Crear un bibliotecario correctamente"""
        bibliotecary = Bibliotecary.objects.create(
            username='biblio1',
            email='biblio1@library.com',
            full_name='Bibliotecario Uno'
        )
        self.assertEqual(bibliotecary.username, 'biblio1')
        self.assertEqual(bibliotecary.email, 'biblio1@library.com')
        self.assertEqual(bibliotecary.full_name, 'Bibliotecario Uno')
    
    def test_bibliotecario_string_representation(self):
        """Test: Representación en string del bibliotecario"""
        bibliotecary = Bibliotecary.objects.create(
            username='biblio2',
            email='biblio2@library.com',
            full_name='Ana García'
        )
        self.assertIn('biblio2', str(bibliotecary))
    
    def test_username_unico(self):
        """Test: El username debe ser único"""
        Bibliotecary.objects.create(
            username='unique_user',
            email='email1@library.com',
            full_name='User One'
        )
        with self.assertRaises(Exception):
            Bibliotecary.objects.create(
                username='unique_user',
                email='email2@library.com',
                full_name='User Two'
            )
    
    def test_email_unico(self):
        """Test: El email debe ser único"""
        Bibliotecary.objects.create(
            username='user1',
            email='unique@library.com',
            full_name='User One'
        )
        with self.assertRaises(Exception):
            Bibliotecary.objects.create(
                username='user2',
                email='unique@library.com',
                full_name='User Two'
            )


class BibliotecaryAPITest(APITestCase):
    """Tests para la API de bibliotecarios"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.bibliotecary = Bibliotecary.objects.create(
            username='admin_biblio',
            email='admin@library.com',
            full_name='Admin Bibliotecario'
        )
        self.writer = Writer.objects.create(name='Laura Esquivel')
        self.book = Book.objects.create(title='Como agua para chocolate', writer=self.writer)
        self.user = User.objects.create(
            username='reader1',
            email='reader1@example.com',
            full_name='Reader One'
        )
    
    def test_listar_bibliotecarios(self):
        """Test: GET /bibliotecaries/ - Listar bibliotecarios"""
        response = self.client.get('/bibliotecaries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_obtener_bibliotecario(self):
        """Test: GET /bibliotecaries/{id}/ - Obtener detalle"""
        response = self.client.get(f'/bibliotecaries/{self.bibliotecary.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'admin_biblio')
    
    def test_crear_bibliotecario(self):
        """Test: POST /bibliotecaries/ - Crear bibliotecario"""
        data = {
            'username': 'new_biblio',
            'email': 'new@library.com',
            'full_name': 'New Bibliotecario'
        }
        response = self.client.post('/bibliotecaries/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Bibliotecary.objects.count(), 2)
    
    def test_actualizar_bibliotecario(self):
        """Test: PUT /bibliotecaries/{id}/ - Actualizar bibliotecario"""
        data = {
            'username': 'admin_biblio',
            'email': 'updated@library.com',
            'full_name': 'Updated Name'
        }
        response = self.client.put(
            f'/bibliotecaries/{self.bibliotecary.id}/',
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.bibliotecary.refresh_from_db()
        self.assertEqual(self.bibliotecary.full_name, 'Updated Name')
    
    def test_eliminar_bibliotecario(self):
        """Test: DELETE /bibliotecaries/{id}/ - Eliminar bibliotecario"""
        response = self.client.delete(f'/bibliotecaries/{self.bibliotecary.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Bibliotecary.objects.count(), 0)
    
    def test_managed_loans_action(self):
        """Test: GET /bibliotecaries/{id}/managed_loans/ - Préstamos gestionados"""
        # Crear préstamos gestionados por este bibliotecario
        Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary,
            is_active=True
        )
        
        response = self.client.get(f'/bibliotecaries/{self.bibliotecary.id}/managed_loans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_active_loans_action(self):
        """Test: GET /bibliotecaries/{id}/active_loans/ - Préstamos activos"""
        # Crear un préstamo activo
        Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary,
            is_active=True
        )
        # Crear un préstamo inactivo
        Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary,
            is_active=False,
            return_date=timezone.now()
        )
        
        response = self.client.get(f'/bibliotecaries/{self.bibliotecary.id}/active_loans/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Solo debe devolver el préstamo activo
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['is_active'])
    
    def test_statistics_action(self):
        """Test: GET /bibliotecaries/{id}/statistics/ - Estadísticas"""
        # Crear préstamos para las estadísticas
        Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary,
            is_active=True
        )
        Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary,
            is_active=False,
            return_date=timezone.now()
        )
        
        response = self.client.get(f'/bibliotecaries/{self.bibliotecary.id}/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_loans', response.data)
        self.assertIn('active_loans', response.data)
        # El campo puede ser 'returned_loans' o 'completed_loans' según la implementación
        self.assertIn('completed_loans' if 'completed_loans' in response.data else 'returned_loans', response.data)
        self.assertEqual(response.data['total_loans'], 2)
        self.assertEqual(response.data['active_loans'], 1)
    
    def test_bibliotecario_no_existente(self):
        """Test: Error 404 al buscar bibliotecario no existente"""
        response = self.client.get('/bibliotecaries/9999/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_crear_bibliotecario_sin_datos_requeridos(self):
        """Test: Error 400 al crear bibliotecario sin datos obligatorios"""
        data = {'username': 'incomplete'}  # Falta email y full_name
        response = self.client.post('/bibliotecaries/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

