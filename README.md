# 📚 Sistema de Gestión de Biblioteca - Django REST API

Sistema completo de gestión de biblioteca desarrollado con Django y Django REST Framework. Permite administrar usuarios, libros, autores, préstamos y personal bibliotecario a través de una API RESTful.

## 🚀 Características

- **Gestión de Usuarios**: CRUD completo con autenticación
- **Gestión de Libros**: Control de títulos, autores y disponibilidad
- **Sistema de Préstamos**: Registro y seguimiento de préstamos de libros
- **Personal Bibliotecario**: Gestión de bibliotecarios
- **API REST**: Endpoints documentados con Django REST Framework
- **Permisos Personalizados**: Control de acceso segun el tipo de usuario
- **Documentación Sphinx**: Documentación técnica completa del código

## 📋 Requisitos Previos

- Python 3.10 o superior
- pip
- Virtualenv (recomendado)

## 🔧 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/Francisco-Gomera/Practica-Django-Avanzado.git
cd "Practica Django Avanzado"
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

```bash
python manage.py migrate
```

### 5. Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

### 6. Cargar datos de prueba (opcional)

```bash
python manage.py loaddata datadump.json
```

## ▶️ Ejecución

Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

La API estará disponible en: `http://localhost:8000/`

Panel de administración: `http://localhost:8000/admin/`

## 📁 Estructura del Proyecto

```
├── api_server/              # Configuración principal del proyecto
│   ├── settings.py          # Configuración de Django
│   ├── urls.py              # URLs principales
│   ├── permissions.py       # Permisos personalizados
│   └── test_permissions.py  # Tests de permisos
├── viewset_users/           # App de gestión de usuarios
│   ├── models.py            # Modelo User
│   ├── serializer.py        # Serializadores
│   ├── views.py             # ViewSets
│   └── tests.py             # Tests
├── viewset_books/           # App de gestión de libros
│   ├── models.py            # Modelos Book, Writer, Loan
│   ├── serializer.py        # Serializadores
│   ├── views.py             # ViewSets
│   └── tests.py             # Tests
├── viewset_bibliotecary/    # App de gestión de bibliotecarios
│   ├── models.py            # Modelo Bibliotecary
│   ├── serializer.py        # Serializadores
│   ├── views.py             # ViewSets
│   └── tests.py             # Tests
├── docs/                    # Documentación Sphinx
├── db.sqlite3               # Base de datos SQLite
├── manage.py                # Script de gestión Django
└── requirements.txt         # Dependencias del proyecto
```

## 🔌 Endpoints de la API

### Usuarios
- `GET /users/` - Listar usuarios
- `POST /users/` - Crear usuario
- `GET /users/{id}/` - Detalle de usuario
- `PUT /users/{id}/` - Actualizar usuario
- `DELETE /users/{id}/` - Eliminar usuario

### Libros
- `GET /books/` - Listar libros
- `POST /books/` - Crear libro
- `GET /books/{id}/` - Detalle de libro
- `PUT /books/{id}/` - Actualizar libro
- `DELETE /books/{id}/` - Eliminar libro

### Autores
- `GET /writers/` - Listar autores
- `POST /writers/` - Crear autor
- `GET /writers/{id}/` - Detalle de autor
- `PUT /writers/{id}/` - Actualizar autor
- `DELETE /writers/{id}/` - Eliminar autor

### Préstamos
- `GET /loans/` - Listar préstamos
- `POST /loans/` - Crear préstamo
- `GET /loans/{id}/` - Detalle de préstamo
- `PUT /loans/{id}/` - Actualizar préstamo
- `DELETE /loans/{id}/` - Eliminar préstamo

### Bibliotecarios
- `GET /bibliotecaries/` - Listar bibliotecarios
- `POST /bibliotecaries/` - Crear bibliotecario
- `GET /bibliotecaries/{id}/` - Detalle de bibliotecario
- `PUT /bibliotecaries/{id}/` - Actualizar bibliotecario
- `DELETE /bibliotecaries/{id}/` - Eliminar bibliotecario

## 🧪 Ejecutar Tests

Ejecutar todos los tests:

```bash
python manage.py test
```

Ejecutar tests de una app específica:

```bash
python manage.py test viewset_books
python manage.py test viewset_users
python manage.py test api_server
```

Ver cobertura de tests (si está instalado coverage):

```bash
coverage run --source='.' manage.py test
coverage report
```

## 📖 Documentación

### Ver documentación HTML

La documentación técnica está generada con Sphinx:

**Opción 1 - Abrir en navegador:**
```bash
# Windows
start docs/build/html/index.html

# Linux/Mac
open docs/build/html/index.html
```

**Opción 2 - Servidor local:**
```bash
cd docs/build/html
python -m http.server 8000
# Visita http://localhost:8000
```

### Regenerar documentación

```bash
cd docs
make html
# O en Windows: .\make.bat html
```

## 🛠️ Tecnologías Utilizadas

- **Django 6.0.1** - Framework web
- **Django REST Framework 3.16.1** - API REST
- **PyMySQL 1.1.2** - Conector MySQL
- **Sphinx 9.1.0** - Generación de documentación
- **SQLite** - Base de datos (desarrollo)

## 🔒 Permisos y Seguridad

El proyecto implementa permisos personalizados para controlar el acceso a los recursos:

- Autenticación requerida para operaciones sensibles
- Permisos basados en roles
- Validación de datos en serializadores

## 📝 Licencia

Este proyecto es parte de una práctica del máster y está disponible para fines educativos.

## 👤 Autor

**Francisco Gomera**
- GitHub: [@Francisco-Gomera](https://github.com/Francisco-Gomera)

---

⭐ Si este proyecto te fue útil, no olvides darle una estrella en GitHub!
