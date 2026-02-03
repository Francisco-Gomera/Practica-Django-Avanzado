from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.utils import timezone
from .models import Writer, Book, Loan
from viewset_users.models import User
from viewset_bibliotecary.models import Bibliotecary


class WriterModelTest(TestCase):
    """Tests para el modelo Writer"""
    
    def test_crear_escritor(self):
        """Test: Crear un escritor correctamente"""
        writer = Writer.objects.create(name='Gabriel García Márquez')
        self.assertEqual(writer.name, 'Gabriel García Márquez')
        self.assertEqual(str(writer), 'Gabriel García Márquez')
    
    def test_nombre_escritor_unico(self):
        """Test: El nombre del escritor debe ser único"""
        Writer.objects.create(name='Jorge Luis Borges')
        with self.assertRaises(Exception):
            Writer.objects.create(name='Jorge Luis Borges')


class BookModelTest(TestCase):
    """Tests para el modelo Book"""
    
    def setUp(self):
        """Configuración inicial"""
        self.writer = Writer.objects.create(name='Isabel Allende')
    
    def test_crear_libro(self):
        """Test: Crear un libro correctamente"""
        book = Book.objects.create(
            title='La casa de los espíritus',
            writer=self.writer
        )
        self.assertEqual(book.title, 'La casa de los espíritus')
        self.assertEqual(book.writer, self.writer)
    
    def test_libro_string_representation(self):
        """Test: Representación en string del libro"""
        book = Book.objects.create(
            title='Cien años de soledad',
            writer=self.writer
        )
        self.assertIn('Cien años de soledad', str(book))
        self.assertIn('Isabel Allende', str(book))
    
    def test_titulo_libro_unico(self):
        """Test: El título del libro debe ser único"""
        Book.objects.create(title='El amor en los tiempos del cólera', writer=self.writer)
        with self.assertRaises(Exception):
            Book.objects.create(title='El amor en los tiempos del cólera', writer=self.writer)
    
    def test_eliminar_escritor_elimina_libros(self):
        """Test: Al eliminar un escritor, se eliminan sus libros (CASCADE)"""
        book = Book.objects.create(title='Test Book', writer=self.writer)
        self.assertEqual(Book.objects.count(), 1)
        
        self.writer.delete()
        self.assertEqual(Book.objects.count(), 0)


class LoanModelTest(TestCase):
    """Tests para el modelo Loan"""
    
    def setUp(self):
        """Configuración inicial"""
        self.writer = Writer.objects.create(name='Pablo Neruda')
        self.book = Book.objects.create(title='Veinte poemas de amor', writer=self.writer)
        self.user = User.objects.create(
            username='reader',
            email='reader@example.com',
            full_name='Test Reader'
        )
        self.bibliotecary = Bibliotecary.objects.create(
            username='librarian',
            email='librarian@example.com',
            full_name='Test Librarian'
        )
    
    def test_crear_prestamo(self):
        """Test: Crear un préstamo correctamente"""
        loan = Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary
        )
        self.assertEqual(loan.book, self.book)
        self.assertEqual(loan.user, self.user)
        self.assertEqual(loan.bibliotecary, self.bibliotecary)
        self.assertTrue(loan.is_active)
        self.assertIsNone(loan.return_date)
        self.assertIsNotNone(loan.loan_date)
    
    def test_prestamo_string_representation(self):
        """Test: Representación en string del préstamo"""
        loan = Loan.objects.create(
            book=self.book,
            user=self.user
        )
        loan_str = str(loan)
        self.assertIn('Veinte poemas de amor', loan_str)
        self.assertIn('reader', loan_str)
        self.assertIn('Activo', loan_str)
    
    def test_devolver_prestamo(self):
        """Test: Marcar un préstamo como devuelto"""
        loan = Loan.objects.create(
            book=self.book,
            user=self.user
        )
        self.assertTrue(loan.is_active)
        
        # Marcar como devuelto
        loan.is_active = False
        loan.return_date = timezone.now()
        loan.save()
        
        self.assertFalse(loan.is_active)
        self.assertIsNotNone(loan.return_date)
    
    def test_eliminar_libro_elimina_prestamos(self):
        """Test: Al eliminar un libro, se eliminan sus préstamos (CASCADE)"""
        loan = Loan.objects.create(book=self.book, user=self.user)
        self.assertEqual(Loan.objects.count(), 1)
        
        self.book.delete()
        self.assertEqual(Loan.objects.count(), 0)
    
    def test_eliminar_bibliotecario_mantiene_prestamos(self):
        """Test: Al eliminar un bibliotecario, los préstamos se mantienen con NULL"""
        loan = Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary
        )
        
        self.bibliotecary.delete()
        loan.refresh_from_db()
        self.assertIsNone(loan.bibliotecary)


class WriterAPITest(APITestCase):
    """Tests para la API de escritores"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.writer = Writer.objects.create(name='Octavio Paz')
    
    def test_listar_escritores(self):
        """Test: GET /writers/ - Listar escritores"""
        response = self.client.get('/writers/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_crear_escritor(self):
        """Test: POST /writers/ - Crear escritor"""
        data = {'name': 'Mario Vargas Llosa'}
        response = self.client.post('/writers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Writer.objects.count(), 2)


class BookAPITest(APITestCase):
    """Tests para la API de libros"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.writer = Writer.objects.create(name='Julio Cortázar')
        self.book = Book.objects.create(title='Rayuela', writer=self.writer)
    
    def test_listar_libros(self):
        """Test: GET /books/ - Listar libros"""
        response = self.client.get('/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Rayuela')
    
    def test_crear_libro_con_writer_name(self):
        """Test: POST /books/ - Crear libro con writer_name"""
        data = {
            'title': 'El túnel',
            'writer_name': 'Ernesto Sábato'
        }
        response = self.client.post('/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Writer.objects.filter(name='Ernesto Sábato').count(), 1)
    
    def test_crear_libro_con_writer_existente(self):
        """Test: POST /books/ - Crear libro con escritor existente"""
        data = {
            'title': 'Bestiario',
            'writer_name': 'Julio Cortázar'  # Ya existe
        }
        response = self.client.post('/books/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # No debe crear un nuevo escritor
        self.assertEqual(Writer.objects.filter(name='Julio Cortázar').count(), 1)


class LoanAPITest(APITestCase):
    """Tests para la API de préstamos"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.writer = Writer.objects.create(name='Carlos Fuentes')
        self.book = Book.objects.create(title='La muerte de Artemio Cruz', writer=self.writer)
        self.user = User.objects.create(
            username='borrower',
            email='borrower@example.com',
            full_name='Book Borrower'
        )
        self.bibliotecary = Bibliotecary.objects.create(
            username='admin',
            email='admin@example.com',
            full_name='Admin User'
        )
    
    def test_crear_prestamo(self):
        """Test: POST /loans/ - Crear un préstamo"""
        data = {
            'book_id': self.book.id,
            'user_id': self.user.id,
            'bibliotecary_id': self.bibliotecary.id
        }
        response = self.client.post('/loans/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_active'])
        self.assertIsNone(response.data['return_date'])
    
    def test_devolver_libro(self):
        """Test: POST /loans/{id}/return_book/ - Devolver un libro"""
        loan = Loan.objects.create(
            book=self.book,
            user=self.user,
            bibliotecary=self.bibliotecary
        )
        response = self.client.post(f'/loans/{loan.id}/return_book/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_active'])
        self.assertIsNotNone(response.data['return_date'])
    
    def test_devolver_libro_ya_devuelto(self):
        """Test: Intentar devolver un libro ya devuelto"""
        loan = Loan.objects.create(
            book=self.book,
            user=self.user,
            is_active=False,
            return_date=timezone.now()
        )
        response = self.client.post(f'/loans/{loan.id}/return_book/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_listar_prestamos_activos(self):
        """Test: GET /loans/active/ - Listar solo préstamos activos"""
        # Crear préstamos activos e inactivos
        Loan.objects.create(book=self.book, user=self.user, is_active=True)
        Loan.objects.create(
            book=self.book,
            user=self.user,
            is_active=False,
            return_date=timezone.now()
        )
        
        response = self.client.get('/loans/active/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertTrue(response.data[0]['is_active'])


class CustomAPIViewsTest(APITestCase):
    """Tests para las API views personalizadas con @api_view"""
    
    def setUp(self):
        """Configuración inicial"""
        self.client = APIClient()
        self.writer = Writer.objects.create(name='Jorge Amado')
        self.book = Book.objects.create(title='Capitanes de la arena', writer=self.writer)
        self.user = User.objects.create(
            username='avid_reader',
            email='reader@example.com',
            full_name='Avid Reader'
        )
        self.loan = Loan.objects.create(book=self.book, user=self.user)
    
    def test_user_loan_history(self):
        """Test: GET /api/users/{id}/loan-history/"""
        response = self.client.get(f'/api/users/{self.user.id}/loan-history/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('statistics', response.data)
        self.assertIn('loan_history', response.data)
        self.assertEqual(response.data['statistics']['total_loans'], 1)
    
    def test_book_loan_statistics(self):
        """Test: GET /api/books/{id}/loan-statistics/"""
        response = self.client.get(f'/api/books/{self.book.id}/loan-statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('book', response.data)
        self.assertIn('statistics', response.data)
        self.assertEqual(response.data['statistics']['total_loans'], 1)
    
    def test_library_statistics(self):
        """Test: GET /api/library/statistics/"""
        response = self.client.get('/api/library/statistics/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('catalog', response.data)
        self.assertIn('loans', response.data)
        self.assertIn('rankings', response.data)

