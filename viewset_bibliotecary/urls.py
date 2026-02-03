from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    BibliotecaryViewSet,
    BibliotecaryListView,
    BibliotecaryCreateView,
    BibliotecaryDetailView,
    BibliotecaryUpdateView
)

router = DefaultRouter()
router.register(r'bibliotecaries', BibliotecaryViewSet, basename='bibliotecary')

urlpatterns = [
    # Vistas genéricas
    path('generic/bibliotecaries/', BibliotecaryListView.as_view(), name='bibliotecary-list-generic'),
    path('generic/bibliotecaries/create/', BibliotecaryCreateView.as_view(), name='bibliotecary-create-generic'),
    path('generic/bibliotecaries/<int:pk>/', BibliotecaryDetailView.as_view(), name='bibliotecary-detail-generic'),
    path('generic/bibliotecaries/<int:pk>/update/', BibliotecaryUpdateView.as_view(), name='bibliotecary-update-generic'),
] + router.urls
