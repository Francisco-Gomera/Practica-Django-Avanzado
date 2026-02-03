from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    BookViewSet, WriterViewSet, LoanViewSet,
    WriterListView, WriterCreateView, WriterDetailView, WriterUpdateView,
    BookListView, BookCreateView, BookDetailView, BookUpdateView,
    LoanListView, LoanCreateView, LoanDetailView, LoanUpdateView,
    user_loan_history, book_loan_statistics, library_statistics
)
#ViewSets
router = DefaultRouter()
router.register(r'books', BookViewSet, basename='book')
router.register(r'writers', WriterViewSet, basename='writer')
router.register(r'loans', LoanViewSet, basename='loan')

urlpatterns = [
    # Vistas genéricas para Writer
    path('generic/writers/', WriterListView.as_view(), name='writer-list-generic'),
    path('generic/writers/create/', WriterCreateView.as_view(), name='writer-create-generic'),
    path('generic/writers/<int:pk>/', WriterDetailView.as_view(), name='writer-detail-generic'),
    path('generic/writers/<int:pk>/update/', WriterUpdateView.as_view(), name='writer-update-generic'),
    
    # Vistas genéricas para Book
    path('generic/books/', BookListView.as_view(), name='book-list-generic'),
    path('generic/books/create/', BookCreateView.as_view(), name='book-create-generic'),
    path('generic/books/<int:pk>/', BookDetailView.as_view(), name='book-detail-generic'),
    path('generic/books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update-generic'),
    
    # Vistas genéricas para Loan
    path('generic/loans/', LoanListView.as_view(), name='loan-list-generic'),
    path('generic/loans/create/', LoanCreateView.as_view(), name='loan-create-generic'),
    path('generic/loans/<int:pk>/', LoanDetailView.as_view(), name='loan-detail-generic'),
    path('generic/loans/<int:pk>/update/', LoanUpdateView.as_view(), name='loan-update-generic'),
    
    # API Views personalizadas que enlazan modelos
    path('api/users/<int:user_id>/loan-history/', user_loan_history, name='user-loan-history'),
    path('api/books/<int:book_id>/loan-statistics/', book_loan_statistics, name='book-loan-statistics'),
    path('api/library/statistics/', library_statistics, name='library-statistics'),
] + router.urls