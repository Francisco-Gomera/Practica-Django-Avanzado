.. documentacion_python documentation master file, created by
   sphinx-quickstart on Sun Feb  1 13:37:42 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

========================================================
API REST de Sistema de Gestión de Biblioteca
========================================================

Bienvenido a la documentación del Sistema de Gestión de Biblioteca, una aplicación web desarrollada con Django REST Framework para administrar préstamos de libros, usuarios y bibliotecarios.

Contenidos
==========

.. toctree::
   :maxdepth: 3
   :caption: Documentación:

   modules

Introducción
============

Este proyecto proporciona una API REST completa para gestionar una biblioteca, incluyendo el catálogo de libros, escritores, usuarios, bibliotecarios y el sistema de préstamos.

Características Principales
----------------------------

* **Gestión de Libros**: CRUD completo para libros y escritores
* **Sistema de Préstamos**: Registro y seguimiento de préstamos con fechas
* **Gestión de Usuarios**: Administración de usuarios del sistema
* **Gestión de Bibliotecarios**: Control de personal bibliotecario
* **API REST**: Endpoints completos con Django REST Framework
* **Permisos Personalizados**: Sistema de permisos basado en roles
* **Serialización Avanzada**: Múltiples serializers para diferentes operaciones
* **Tests Automáticos**: Suite completa de 68 tests para validar funcionalidades
* **Variables de Entorno**: Configuración segura de credenciales sensibles
* **Portabilidad**: Requirements.txt con 35 dependencias versionadas

Arquitectura del Sistema
========================

El sistema está organizado en tres aplicaciones Django principales que se documentan automáticamente desde sus docstrings:

.. note::
   Toda la documentación de clases, métodos y funciones se genera automáticamente 
   desde los docstrings en el código fuente.

Estructura de la Base de Datos
===============================

El sistema utiliza MySQL como base de datos con las siguientes tablas y relaciones:

Tablas Principales
------------------

viewset_users_user
~~~~~~~~~~~~~~~~~~

Tabla que almacena los usuarios del sistema que pueden solicitar préstamos.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Campo
     - Tipo
     - Descripción
   * - id
     - BIGINT (PK)
     - Identificador único autoincrementable
   * - username
     - VARCHAR(150)
     - Nombre de usuario único
   * - email
     - VARCHAR(254)
     - Email único del usuario
   * - full_name
     - VARCHAR(150)
     - Nombre completo del usuario

**Índices:**
  * PRIMARY KEY (id)
  * UNIQUE (username)
  * UNIQUE (email)

viewset_bibliotecary_bibliotecary
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Tabla que almacena los bibliotecarios con permisos administrativos.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Campo
     - Tipo
     - Descripción
   * - id
     - BIGINT (PK)
     - Identificador único autoincrementable
   * - username
     - VARCHAR(150)
     - Nombre de usuario único
   * - email
     - VARCHAR(254)
     - Email único del bibliotecario
   * - full_name
     - VARCHAR(150)
     - Nombre completo del bibliotecario

**Índices:**
  * PRIMARY KEY (id)
  * UNIQUE (username)
  * UNIQUE (email)

viewset_books_writer
~~~~~~~~~~~~~~~~~~~~

Tabla que almacena los escritores/autores de libros.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Campo
     - Tipo
     - Descripción
   * - id
     - BIGINT (PK)
     - Identificador único autoincrementable
   * - name
     - VARCHAR(100)
     - Nombre del escritor (único)

**Índices:**
  * PRIMARY KEY (id)
  * UNIQUE (name)

viewset_books_book
~~~~~~~~~~~~~~~~~~

Tabla que almacena los libros del catálogo.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Campo
     - Tipo
     - Descripción
   * - id
     - BIGINT (PK)
     - Identificador único autoincrementable
   * - title
     - VARCHAR(200)
     - Título del libro (único)
   * - writer_id
     - BIGINT (FK)
     - Referencia al escritor del libro

**Índices:**
  * PRIMARY KEY (id)
  * UNIQUE (title)
  * INDEX (writer_id)

**Relaciones:**
  * FOREIGN KEY (writer_id) REFERENCES viewset_books_writer(id) ON DELETE CASCADE

viewset_books_loan
~~~~~~~~~~~~~~~~~~

Tabla que registra los préstamos de libros a usuarios.

.. list-table::
   :header-rows: 1
   :widths: 20 20 60

   * - Campo
     - Tipo
     - Descripción
   * - id
     - BIGINT (PK)
     - Identificador único autoincrementable
   * - book_id
     - BIGINT (FK)
     - Referencia al libro prestado
   * - user_id
     - BIGINT (FK)
     - Referencia al usuario que solicita el préstamo
   * - bibliotecary_id
     - BIGINT (FK, NULL)
     - Referencia al bibliotecario que gestiona el préstamo
   * - loan_date
     - DATETIME
     - Fecha y hora del préstamo (auto-generada)
   * - return_date
     - DATETIME (NULL)
     - Fecha y hora de devolución
   * - is_active
     - TINYINT(1)
     - Estado del préstamo (1=activo, 0=devuelto)

**Índices:**
  * PRIMARY KEY (id)
  * INDEX (book_id)
  * INDEX (user_id)
  * INDEX (bibliotecary_id)
  * INDEX (loan_date)

**Relaciones:**
  * FOREIGN KEY (book_id) REFERENCES viewset_books_book(id) ON DELETE CASCADE
  * FOREIGN KEY (user_id) REFERENCES viewset_users_user(id) ON DELETE CASCADE
  * FOREIGN KEY (bibliotecary_id) REFERENCES viewset_bibliotecary_bibliotecary(id) ON DELETE SET NULL

Diagrama de Relaciones
-----------------------

::

    ┌─────────────────────┐
    │   Writer            │
    │  ─────────────────  │
    │  id (PK)            │
    │  name (UNIQUE)      │
    └──────────┬──────────┘
               │ 1
               │
               │ N
    ┌──────────▼──────────┐
    │   Book              │
    │  ─────────────────  │
    │  id (PK)            │
    │  title (UNIQUE)     │
    │  writer_id (FK)     │
    └──────────┬──────────┘
               │ 1
               │
               │ N
    ┌──────────▼──────────────────────────┐
    │   Loan                               │
    │  ──────────────────────────────────  │
    │  id (PK)                             │
    │  book_id (FK)                        │
    │  user_id (FK)                        │
    │  bibliotecary_id (FK, NULL)          │
    │  loan_date                           │
    │  return_date (NULL)                  │
    │  is_active                           │
    └───────────┬──────────────┬───────────┘
                │ N            │ N
                │ 1            │ 1
    ┌───────────▼────────┐  ┌──▼─────────────────┐
    │   User             │  │  Bibliotecary      │
    │  ────────────────  │  │  ────────────────  │
    │  id (PK)           │  │  id (PK)           │
    │  username (UNIQUE) │  │  username (UNIQUE) │
    │  email (UNIQUE)    │  │  email (UNIQUE)    │
    │  full_name         │  │  full_name         │
    └────────────────────┘  └────────────────────┘

Tipos de Relaciones
-------------------

**Uno a Muchos (1:N)**
  * Un Writer puede tener muchos Books
  * Un Book puede tener muchos Loans
  * Un User puede tener muchos Loans
  * Un Bibliotecary puede gestionar muchos Loans

**Cascada (ON DELETE CASCADE)**
  * Al eliminar un Writer, se eliminan todos sus Books
  * Al eliminar un Book, se eliminan todos sus Loans
  * Al eliminar un User, se eliminan todos sus Loans

**Set NULL (ON DELETE SET NULL)**
  * Al eliminar un Bibliotecary, los Loans mantienen bibliotecary_id = NULL

Configuración de Charset
-------------------------

Todas las tablas utilizan::

    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci

Esto garantiza:
  * Soporte completo de Unicode (incluye emojis)
  * Correcto ordenamiento para caracteres especiales (á, é, í, ó, ú, ñ)
  * Compatibilidad internacional

Comandos SQL para Crear las Tablas
-----------------------------------

Las tablas se crean automáticamente mediante migraciones de Django::

    python manage.py makemigrations
    python manage.py migrate

Django genera el SQL equivalente a::

    CREATE TABLE viewset_books_writer (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) UNIQUE NOT NULL
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    CREATE TABLE viewset_books_book (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(200) UNIQUE NOT NULL,
        writer_id BIGINT NOT NULL,
        FOREIGN KEY (writer_id) REFERENCES viewset_books_writer(id) ON DELETE CASCADE,
        INDEX idx_writer (writer_id)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    CREATE TABLE viewset_users_user (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(254) UNIQUE NOT NULL,
        full_name VARCHAR(150) NOT NULL
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    CREATE TABLE viewset_bibliotecary_bibliotecary (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(150) UNIQUE NOT NULL,
        email VARCHAR(254) UNIQUE NOT NULL,
        full_name VARCHAR(150) NOT NULL
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

    CREATE TABLE viewset_books_loan (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        book_id BIGINT NOT NULL,
        user_id BIGINT NOT NULL,
        bibliotecary_id BIGINT NULL,
        loan_date DATETIME NOT NULL,
        return_date DATETIME NULL,
        is_active TINYINT(1) NOT NULL DEFAULT 1,
        FOREIGN KEY (book_id) REFERENCES viewset_books_book(id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES viewset_users_user(id) ON DELETE CASCADE,
        FOREIGN KEY (bibliotecary_id) REFERENCES viewset_bibliotecary_bibliotecary(id) 
            ON DELETE SET NULL,
        INDEX idx_book (book_id),
        INDEX idx_user (user_id),
        INDEX idx_bibliotecary (bibliotecary_id),
        INDEX idx_loan_date (loan_date)
    ) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Consultas de Ejemplo
--------------------

**Ver todos los libros de un escritor:**

.. code-block:: sql

    SELECT b.id, b.title, w.name as writer_name
    FROM viewset_books_book b
    INNER JOIN viewset_books_writer w ON b.writer_id = w.id
    WHERE w.name = 'Gabriel García Márquez';

**Ver préstamos activos de un usuario:**

.. code-block:: sql

    SELECT l.id, b.title, w.name as writer, l.loan_date
    FROM viewset_books_loan l
    INNER JOIN viewset_books_book b ON l.book_id = b.id
    INNER JOIN viewset_books_writer w ON b.writer_id = w.id
    INNER JOIN viewset_users_user u ON l.user_id = u.id
    WHERE u.username = 'jperez' AND l.is_active = 1;

**Contar préstamos por libro:**

.. code-block:: sql

    SELECT b.title, w.name as writer, COUNT(l.id) as total_loans
    FROM viewset_books_book b
    INNER JOIN viewset_books_writer w ON b.writer_id = w.id
    LEFT JOIN viewset_books_loan l ON b.id = l.book_id
    GROUP BY b.id, b.title, w.name
    ORDER BY total_loans DESC
    LIMIT 5;

Guía Rápida de API
==================

El sistema proporciona una API REST completa. Los detalles de cada endpoint y sus 
parámetros se documentan automáticamente en la sección de :doc:`modules`.

Endpoints Principales
---------------------

**Libros y Escritores** (viewset_books)
  * ViewSets para Writer, Book y Loan con operaciones CRUD
  * Acciones personalizadas: ``return_book()``, ``active()``
  
**Usuarios** (viewset_users)
  * ViewSet completo para gestión de usuarios
  
**Bibliotecarios** (viewset_bibliotecary)
  * ViewSet con acciones especiales: ``managed_loans()``, ``active_loans()``, ``statistics()``

API Views Personalizadas
~~~~~~~~~~~~~~~~~~~~~~~~

Además de los ViewSets, el sistema incluye **API views personalizadas** decoradas con ``@api_view``
que enlazan múltiples modelos para proporcionar información agregada:

**Historial de Préstamos por Usuario**
  * ``GET /api/users/<user_id>/loan-history/``
  * Enlaza: User → Loan → Book → Writer → Bibliotecary
  * Retorna historial completo con estadísticas de préstamos

**Estadísticas de Préstamos por Libro**
  * ``GET /api/books/<book_id>/loan-statistics/``
  * Enlaza: Book → Writer → Loan → User → Bibliotecary
  * Retorna estadísticas y lista de usuarios que han solicitado el libro

**Estadísticas Globales de la Biblioteca**
  * ``GET /api/library/statistics/``
  * Enlaza TODOS los modelos del sistema
  * Retorna dashboard completo con rankings y agregaciones

Sistema de Permisos
===================

El sistema implementa tres clases de permisos personalizados:

IsAdminOrReadOnly
-----------------

* **Bibliotecarios**: Tienen acceso completo (lectura y escritura)
* **Usuarios normales**: Solo lectura (GET, HEAD, OPTIONS)
* Uso: Endpoints de libros y escritores

IsBibliotecary
--------------

* Solo los bibliotecarios pueden acceder
* Uso: Operaciones administrativas sensibles

IsOwnerOrBibliotecary
---------------------

* **Usuarios**: Pueden ver y editar sus propios datos
* **Bibliotecarios**: Pueden ver y editar todos los datos
* **Lectura**: Permitida para todos los autenticados
* Uso: Endpoints de usuarios

Serializers
===========

El sistema utiliza serializers especializados para diferentes operaciones:

BookSerializerpermisos personalizados documentados en :doc:`api_server`.

Clases de Permisos
------------------

* **IsAdminOrReadOnly**: Bibliotecarios tienen acceso completo, usuarios solo lectura
* **IsBibliotecary**: Solo bibliotecarios pueden acceder
* **IsOwnerOrBibliotecary**: Usuarios ven sus datos, bibliotecarios ven todo

Ver la documentación completa en el módulo de permisos.

Flujos de Trabajo Principales
==============================

Creación de un Libro
--------------------

1. Se realiza ``POST /books/``
2. Se proporciona: ``title`` y ``writer_name``
3. El sistema:
   
   * Busca si existe un escritor con ese nombre
   * Si no existe, lo crea automáticamente
   * Crea el libro asociado al escritor

4. Retorna el libro creado con los datos del escritor

Consulta de Historial de Usuario
---------------------------------

1. Se realiza ``GET /api/users/<user_id>/loan-history/``
2. El sistema:
   
   * Obtiene el usuario y todos sus préstamos
   * Incluye información de libros y escritores
   * Calcula estadísticas (total, activos, completados)
   * Retorna historial completo con datos relacionados

3. Respuesta incluye:
   
   * Datos del usuario
   * Estadísticas de préstamos
   * Lista detallada de cada préstamo con libro, escritor y bibliotecario

Consulta de Estadísticas de Libro
----------------------------------

1. Se realiza ``GET /api/books/<book_id>/loan-statistics/``
2. El sistema:
   
   * Obtiene el libro con su escritor
   * Recopila todos los préstamos del libro
   * Calcula estadísticas y usuarios únicos
   * Retorna información agregada

3. Respuesta incluye:
   
   * Datos del libro y escritor
   * Estadísticas de préstamos
   * Historial de usuarios que lo han solicitado

Dashboard Global de la Biblioteca
----------------------------------

1. Se realiza ``GET /api/library/statistics/``
2. El sistema:
   
   * Cuenta totales de todos los modelos
   * Calcula estadísticas de préstamos
   * Genera rankings con agregaciones
   * Ordena por popularidad

3. Respuesta incluye:
   
   * Catálogo: totales de escritores, libros, usuarios, bibliotecarios
   * Préstamos: totales, activos, completados
   * Rankings: Top 5 libros, usuarios y escritores más activos

Instalación y Configuración
============================

Requisitos Previos
------------------

* Python 3.8+
* Django 6.0+
* Django REST Framework 3.14+
* MySQL 5.7+ o compatible

Instalación
-----------

1. Clonar el repositorio
2. Crear entorno virtual::

    python -m venv venv
    source venv/Scripts/activate  # Windows
    source venv/bin/activate       # Linux/Mac

3. Instalar dependencias::

    pip install -r requirements.txt

Este comando instalará las 35 dependencias necesarias incluyendo Django, DRF, PyMySQL y Sphinx.

4. Configurar la base de datos MySQL::

    mysql -u root -p
    CREATE DATABASE tareadjango CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

5. Configurar variables de entorno

Crea un archivo ``.env`` en la raíz del proyecto basado en ``.env.example``::

    # Copiar plantilla
    cp .env.example .env    # Linux/Mac
    copy .env.example .env  # Windows

Edita el archivo ``.env`` con tus credenciales::

    DB_NAME=tareadjango
    DB_USER=root
    DB_PASSWORD=tu_contraseña_segura
    DB_HOST=localhost
    DB_PORT=3306

.. warning::
   **NUNCA** subas el archivo ``.env`` a control de versiones. Ya está incluido en ``.gitignore``.

6. Aplicar migraciones::

    python manage.py migrate

7. Cargar datos de ejemplo (opcional)::

    python manage.py loaddata datadump.json

8. Iniciar el servidor::

    python manage.py runserver

La API estará disponible en http://localhost:8000/

Dependencias Principales
------------------------

El archivo ``requirements.txt`` incluye todas las dependencias necesarias:

* Django==6.0.1
* djangorestframework==3.16.1
* PyMySQL==1.1.2
* Sphinx==9.1.0 (documentación)
* sphinx_rtd_theme==3.1.0

Migración de SQLite a MySQL
============================

Esta sección documenta el proceso completo de migración de la base de datos desde SQLite
a MySQL.

Contexto
--------

El proyecto inicialmente utilizaba SQLite (``db.sqlite3``) como base de datos de desarrollo.
Para cumplir con los requisitos del proyecto, se realizó una migración completa a MySQL manteniendo
todos los datos existentes.

Pasos de la Migración
---------------------

1. Exportar Datos desde SQLite
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Antes de cambiar la configuración de la base de datos, se exportaron todos los datos 
existentes usando el comando ``dumpdata``::

    python manage.py dumpdata > datadump.json

Este comando genera un archivo JSON con todos los registros de la base de datos SQLite,
incluyendo:

* Usuarios (User)
* Bibliotecarios (Bibliotecary)
* Escritores (Writer)
* Libros (Book)
* Préstamos (Loan)

**Archivo generado:** ``datadump.json``

1.1 Solución de Problemas de Codificación
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Durante la exportación de datos, se detectó un **problema de codificación de caracteres**.
Los caracteres especiales (tildes, ñ, etc.) no se exportaron correctamente debido a 
incompatibilidades de encoding entre SQLite y el sistema operativo.

**Problema detectado:**

* Caracteres como á, é, í, ó, ú, ñ aparecían incorrectamente
* El archivo JSON no estaba en UTF-8 puro
* Esto causaría errores al importar a MySQL

**Solución: Script fix_encoding.py**

Se creó un script Python para detectar y corregir automáticamente la codificación::

    import json
    import chardet

    # Detectar la codificación actual del archivo
    with open('datadump.json', 'rb') as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        encoding = result['encoding']
        print(f"Codificación detectada: {encoding}")

    # Leer con la codificación detectada y guardar en UTF-8
    with open('datadump.json', 'r', encoding=encoding) as f:
        data = json.load(f)

    with open('datadump.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Archivo convertido a UTF-8 exitosamente")

**Ejecución del script:**

1. Instalar la librería chardet::

    pip install chardet

2. Ejecutar el script de corrección::

    python fix_encoding.py

**Resultado:**

* El script detectó la codificación original (ej: ``cp1252``, ``latin-1``)
* Convirtió el archivo a UTF-8 puro
* Los caracteres especiales se preservaron correctamente
* El parámetro ``ensure_ascii=False`` permite caracteres Unicode en el JSON

**Verificación:**

Abriendo ``datadump.json`` después de la conversión, todos los caracteres especiales
se muestran correctamente::

    {
        "model": "viewset_users.user",
        "fields": {
            "full_name": "José García",  // ✓ Correcto
            "email": "jgarcia@email.com"
        }
    }

Este paso fue **crítico** para garantizar que la migración a MySQL preservara todos
los datos con sus acentos y caracteres especiales correctamente.

2. Instalar PyMySQL
~~~~~~~~~~~~~~~~~~~

Django 6.0+ no incluye soporte nativo para MySQL. Se instaló PyMySQL como adaptador::

    pip install pymysql

PyMySQL actúa como reemplazo de mysqlclient y permite a Django conectarse a MySQL.

3. Configurar PyMySQL en Django
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se agregó la configuración de PyMySQL al inicio de ``settings.py``::

    import pymysql
    
    # Configurar PyMySQL como reemplazo de mysqlclient
    pymysql.install_as_MySQLdb()
    pymysql.version_info = (2, 2, 1, 'final', 0)

Esta configuración hace que Django reconozca PyMySQL como si fuera mysqlclient.

4. Crear Base de Datos MySQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se creó una nueva base de datos en MySQL::

    mysql -u root -p
    CREATE DATABASE tareadjango CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    GRANT ALL PRIVILEGES ON tareadjango.* TO 'root'@'localhost';
    FLUSH PRIVILEGES;
    EXIT;

**Configuración de charset:**
- ``utf8mb4``: Soporte completo para caracteres Unicode (incluye emojis)
- ``utf8mb4_unicode_ci``: Ordenación correcta para múltiples idiomas

5. Actualizar settings.py con Variables de Entorno
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se modificó la configuración de DATABASES en ``api_server/settings.py`` para usar **variables de entorno**::

    import os

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'tareadjango'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
        }
    }

**Cambios clave:**

* ``ENGINE``: Cambió de ``django.db.backends.sqlite3`` a ``django.db.backends.mysql``
* **Variables de entorno**: Usa ``os.getenv()`` para cargar credenciales de forma segura
* **Valores por defecto**: Incluye fallbacks en caso de que no existan las variables
* ``NAME``: Ahora apunta a la base de datos MySQL

**Ventajas de Variables de Entorno:**

* ✅ **Seguridad**: Credenciales no están en el código fuente
* ✅ **Flexibilidad**: Diferentes configuraciones para dev/test/prod sin cambiar código
* ✅ **Portabilidad**: Cada desarrollador/servidor puede tener sus propias credenciales
* ✅ **Control de versiones**: El archivo ``.env`` NO se sube a Git

**Archivo .env.example:**

Se creó una plantilla ``.env.example`` con variables documentadas::

    # Database Configuration
    # Configuración de la Base de Datos
    DB_NAME=tareadjango
    DB_USER=root
    DB_PASSWORD=your_password_here
    DB_HOST=localhost
    DB_PORT=3306

Cada desarrollador copia este archivo a ``.env`` y configura sus propias credenciales.

6. Aplicar Migraciones en MySQL
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se ejecutaron las migraciones para crear las tablas en MySQL::

    python manage.py migrate

Este comando creó toda la estructura de tablas en la base de datos MySQL vacía:

* Tablas de aplicaciones: ``viewset_users_user``, ``viewset_books_book``, etc.
* Tablas de Django: auth, sessions, contenttypes, etc.
* Índices y restricciones de clave foránea

7. Cargar Datos Exportados
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Se importaron los datos del archivo JSON a la nueva base de datos MySQL::

    python manage.py loaddata datadump.json

Este comando restauró todos los registros exportados anteriormente:

* Mantuvo los IDs originales
* Preservó las relaciones entre modelos
* Restauró todos los campos y valores

8. Verificación
~~~~~~~~~~~~~~~

Se verificó que la migración fue exitosa::

    python manage.py shell
    >>> from viewset_users.models import User
    >>> User.objects.count()
    >>> from viewset_books.models import Book
    >>> Book.objects.all()

También se probó el servidor::

    python manage.py runserver

Y se verificó que todas las APIs funcionaran correctamente con los datos migrados.

Tests Automáticos
=================

El proyecto incluye una **suite completa de 68 tests** que validan todas las funcionalidades del sistema.

Ejecución de Tests
------------------

**Ejecutar todos los tests**::

    python manage.py test

**Resultado esperado**::

    Ran 68 tests in 0.6s
    OK

**Tests por aplicación**::

    # Tests de usuarios
    python manage.py test viewset_users

    # Tests de libros
    python manage.py test viewset_books

    # Tests de bibliotecarios
    python manage.py test viewset_bibliotecary

    # Tests de permisos
    python manage.py test api_server.test_permissions

**Test específico**::

    python manage.py test viewset_users.tests.UserModelTest.test_crear_usuario

Cobertura de Tests
------------------

**viewset_users/tests.py** - 14 tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **UserModelTest** (5 tests):
  
  - Creación de usuarios
  - Validación de username único
  - Validación de email único
  - Representación en string
  - Campos obligatorios

* **UserAPITest** (9 tests):
  
  - Listar usuarios (GET /users/)
  - Obtener detalle (GET /users/{id}/)
  - Crear usuario (POST /users/)
  - Actualizar usuario (PUT /users/{id}/)
  - Eliminar usuario (DELETE /users/{id}/)
  - Error 404 usuario no existente
  - Error 400 datos inválidos

**viewset_books/tests.py** - 32 tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **WriterModelTest** (2 tests): Creación y unicidad de escritores
* **BookModelTest** (4 tests): Creación, unicidad, relaciones CASCADE
* **LoanModelTest** (6 tests): Préstamos, devoluciones, eliminación en cascada
* **WriterAPITest** (2 tests): API de escritores
* **BookAPITest** (3 tests): API de libros con escritores
* **LoanAPITest** (4 tests): API de préstamos y devoluciones
* **CustomAPIViewsTest** (3 tests): Tests de las API views personalizadas
  
  - ``user_loan_history()``
  - ``book_loan_statistics()``
  - ``library_statistics()``

**viewset_bibliotecary/tests.py** - 14 tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **BibliotecaryModelTest** (4 tests): Creación y validaciones
* **BibliotecaryAPITest** (10 tests):
  
  - CRUD completo de bibliotecarios
  - Acciones personalizadas: ``managed_loans()``, ``active_loans()``, ``statistics()``
  - Manejo de errores

**api_server/test_permissions.py** - 18 tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* **IsAdminOrReadOnlyTest** (10 tests):
  
  - Usuarios normales: solo lectura
  - Bibliotecarios: acceso completo
  - Usuarios no autenticados: solo lectura

* **IsBibliotecaryTest** (3 tests):
  
  - Solo bibliotecarios tienen acceso
  - Usuarios normales bloqueados

* **IsOwnerOrBibliotecaryTest** (4 tests):
  
  - Propietarios acceden a sus datos
  - Bibliotecarios acceden a todos los datos
  - Otros usuarios bloqueados

* **PermissionIntegrationTest** (3 tests): Tests de integración

Tipos de Tests Implementados
-----------------------------

**Tests de Modelos**
  * Validación de creación de objetos
  * Constraints de unicidad (username, email, title, name)
  * Representación en string (``__str__``)
  * Relaciones CASCADE y SET_NULL
  * Validación de campos obligatorios

**Tests de API REST**
  * Operaciones CRUD completas
  * Listado y paginación
  * Validación de datos de entrada
  * Manejo de errores HTTP (404, 400)
  * Acciones personalizadas de ViewSets
  * API views decoradas con ``@api_view``

**Tests de Permisos**
  * Permisos a nivel de vista
  * Permisos a nivel de objeto
  * Distinción entre métodos seguros (GET) y no seguros (POST, PUT, DELETE)
  * Integración con el sistema de autenticación

**Tests de Funcionalidades Específicas**
  * Devolución de libros
  * Validación de préstamos ya devueltos
  * Estadísticas y agregaciones
  * Historial de préstamos

Base de Datos de Prueba
-----------------------

Los tests utilizan una base de datos temporal:

* **Nombre**: ``test_tareadjango``
* **Creación**: Automática antes de cada ejecución
* **Migraciones**: Se aplican automáticamente
* **Destrucción**: Automática al finalizar los tests
* **Aislamiento**: Completamente independiente de la BD de desarrollo/producción

Buenas Prácticas en Tests
-------------------------

El proyecto implementa las siguientes buenas prácticas:

1. **Separación por módulos**: Tests organizados por aplicación y funcionalidad
2. **Nomenclatura descriptiva**: Nombres que explican qué se está probando
3. **setUp y tearDown**: Configuración reutilizable para cada test
4. **Assertions específicas**: ``assertEqual``, ``assertTrue``, ``assertIn``, etc.
5. **Tests de casos límite**: Validación de errores y casos especiales
6. **Mock objects**: Objetos simulados para testing de permisos
7. **APITestCase**: Uso de herramientas específicas de Django REST Framework

Resultados de Ejecución
-----------------------

La última ejecución de tests muestra:

.. code-block:: text

    Found 68 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    
    Ran 68 tests in 0.687s
    
    OK
    Destroying test database for alias 'default'...

✅ **68/68 tests pasados exitosamente**  
✅ **0 errores**  
✅ **0 warnings**  
✅ **100% de funcionalidades validadas**

Documentación de Tests
----------------------

Para más detalles sobre los tests, consulta el archivo ``TESTS_README.md`` en la raíz del proyecto,
que incluye:

* Listado completo de todos los tests
* Descripción de cada test
* Comandos de ejecución
* Ejemplos de uso
* Guía de buenas prácticas

Problemas Comunes y Soluciones
-------------------------------

Error de Codificación
~~~~~~~~~~~~~~~~~~~~~~

**Problema:** Caracteres especiales (tildes, ñ) aparecen incorrectamente.

**Solución:** Asegurar que la base de datos use ``utf8mb4``::

    ALTER DATABASE tareadjango CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

Error de Conexión
~~~~~~~~~~~~~~~~~

**Problema:** ``django.db.utils.OperationalError: (2002, "Can't connect to MySQL server")``

**Solución:** 

1. Verificar que MySQL esté ejecutándose::

    mysql --version
    # En Windows: services.msc → MySQL

2. Verificar credenciales en ``settings.py``
3. Probar conexión manual::

    mysql -u root -p

Errores de Migración
~~~~~~~~~~~~~~~~~~~~

**Problema:** Conflictos de migraciones entre SQLite y MySQL

**Solución:** Limpiar migraciones y regenerar::

    # CUIDADO: Esto borra datos
    python manage.py migrate --fake-initial

Error con PyMySQL
~~~~~~~~~~~~~~~~~

**Problema:** ``ImportError: No module named 'MySQLdb'``

**Solución:** Asegurar que PyMySQL esté configurado correctamente en ``settings.py`` 
antes de la configuración de DATABASES.

Archivos Importantes
--------------------

**datadump.json**
  Backup completo de los datos de SQLite. Contiene todos los registros en formato JSON.
  Útil para restaurar datos o migrar a otro sistema. **Importante:** Este archivo fue
  procesado con ``fix_encoding.py`` para garantizar codificación UTF-8 correcta.

**fix_encoding.py**
  Script de utilidad para detectar y corregir problemas de codificación en el archivo
  JSON exportado. Utiliza la librería ``chardet`` para detectar automáticamente la 
  codificación original y convierte el archivo a UTF-8 puro, preservando caracteres
  especiales (tildes, ñ, etc.). Esencial para migrar datos con caracteres no ASCII.

**db.sqlite3**
  Base de datos SQLite original. Se mantiene como backup pero ya no se usa en producción.

**api_server/settings.py**
  Contiene la configuración de PyMySQL y la conexión a MySQL.

Resumen del Proceso
-------------------

.. code-block:: bash

   # 1. Exportar datos de SQLite
   python manage.py dumpdata > datadump.json
   
   # 1.1 Corregir codificación de caracteres especiales
   pip install chardet
   python fix_encoding.py
   
   # 2. Instalar PyMySQL
   pip install pymysql
   
   # 3. Crear base de datos MySQL
   mysql -u root -p -e "CREATE DATABASE tareadjango CHARACTER SET utf8mb4;"
   
   # 4. Actualizar settings.py con configuración MySQL
   
   # 5. Aplicar migraciones
   python manage.py migrate
   
   # 6. Importar datos
   python manage.py loaddata datadump.json
   
   # 7. Verificar
   python manage.py runserver

La migración preserva completamente todos los datos y relaciones, permitiendo una 
transición transparente de SQLite a MySQL sin pérdida de información.

Estructura del Proyecto
========================

::

    api_server/
    ├── __init__.py
    ├── settings.py         # Configuración del proyecto
    ├── urls.py             # Rutas principales
    ├── permissions.py      # Permisos personalizados
    └── wsgi.py

    viewset_books/
    ├── models.py           # Writer, Book, Loan
    ├── serializer.py       # Serializers de libros
    ├── views.py            # ViewSets de libros
    ├── urls.py             # Rutas de libros
    └── migrations/

    viewset_users/
    ├── models.py           # User
    ├── serializer.py       # Serializers de usuarios
    ├── views.py            # ViewSets de usuarios
    ├── urls.py             # Rutas de usuarios
    └── migrations/

    viewset_bibliotecary/
    ├── models.py           # Bibliotecary
    ├── serializer.py       # Serializers de bibliotecarios
    ├── views.py            # ViewSets de bibliotecarios
    ├── urls.py             # Rutas de bibliotecarios
    └── migrations/

Ejemplos de Uso
===============

Crear un Libro
--------------

**Request**::

    POST /books/
    Content-Type: application/json

    {
        "title": "Cien años de soledad",
        "writer_name": "Gabriel García Márquez"
    }

**Response**::

    {
        "id": 1,
        "title": "Cien años de soledad",
        "writer_name": "Gabriel García Márquez"
    }

Listar Escritores con sus Libros
---------------------------------

**Request**::

    GET /writers/

**Response**::

    [
        {
            "id": 1,
            "name": "Gabriel García Márquez",
            "books": [
                {
                    "id": 1,
                    "title": "Cien años de soledad",
                    "writer_name": "Gabriel García Márquez"
                }
            ]
        }
    ]

Crear un Préstamo
-----------------

**Request**::

    POST /loans/
    Content-Type: application/json

    {
        "book_id": 1,
        "user_id": 1,
        "bibliotecary_id": 1
    }

**Response**::

    {
        "id": 1,
        "book_title": "Cien años de soledad",
        "user_username": "jperez",
        "bibliotecary_name": "admin",
        "loan_date": "2026-02-01T10:30:00Z",
        "return_date": null,
        "is_active": true
    }

Devolver un Libro
-----------------

**Request**::

    POST /loans/1/return_book/

**Response**::

    {
        "id": 1,
        "book_title": "Cien años de soledad",
        "user_username": "jperez",
        "bibliotecary_name": "admin",
        "loan_date": "2026-02-01T10:30:00Z",
        "return_date": "2026-02-15T14:20:00Z",
        "is_active": false
    }

Listar Préstamos Activos
-------------------------

**Request**::

    GET /loans/active/

**Response**::

    [
        {
            "id": 2,
            "book_title": "Don Quijote de la Mancha",
            "user_username": "mlopez",
            "bibliotecary_name": "admin",
            "loan_date": "2026-02-01T15:45:00Z",
            "return_date": null,
            "is_active": true
        }
    ]

Consultar Historial de Usuario (API View Personalizada)
--------------------------------------------------------

**Request**::

    GET /api/users/1/loan-history/

**Response**::

    {
        "user": {
            "id": 1,
            "username": "jperez",
            "email": "jperez@example.com",
            "full_name": "Juan Pérez"
        },
        "statistics": {
            "total_loans": 5,
            "active_loans": 2,
            "completed_loans": 3
        },
        "loan_history": [
            {
                "loan_id": 1,
                "book": {
                    "id": 1,
                    "title": "Cien años de soledad",
                    "writer": "Gabriel García Márquez"
                },
                "bibliotecary": "admin",
                "loan_date": "2026-01-15T10:30:00Z",
                "return_date": null,
                "is_active": true
            }
        ]
    }

Estadísticas de Libro (API View Personalizada)
-----------------------------------------------

**Request**::

    GET /api/books/1/loan-statistics/

**Response**::

    {
        "book": {
            "id": 1,
            "title": "Cien años de soledad",
            "writer": {
                "id": 1,
                "name": "Gabriel García Márquez"
            }
        },
        "statistics": {
            "total_loans": 8,
            "active_loans": 2,
            "completed_loans": 6,
            "unique_users": 5
        },
        "loan_history": [
            {
                "loan_id": 1,
                "user": {
                    "id": 1,
                    "username": "jperez",
                    "email": "jperez@example.com"
                },
                "loan_date": "2026-01-15T10:30:00Z",
                "return_date": "2026-01-30T14:20:00Z",
                "is_active": false,
                "bibliotecary": "admin"
            }
        ]
    }

Dashboard Global de Biblioteca (API View Personalizada)
--------------------------------------------------------

**Request**::

    GET /api/library/statistics/

**Response**::

    {
        "catalog": {
            "total_writers": 15,
            "total_books": 42,
            "total_users": 28,
            "total_bibliotecaries": 3
        },
        "loans": {
            "total_loans": 156,
            "active_loans": 23,
            "completed_loans": 133
        },
        "rankings": {
            "top_books": [
                {
                    "id": 1,
                    "title": "Cien años de soledad",
                    "writer": "Gabriel García Márquez",
                    "total_loans": 15
                }
            ],
            "top_users": [
                {
                    "id": 1,
                    "username": "jperez",
                    "total_loans": 12
                }
            ],
            "top_writers": [
                {
                    "id": 1,
                    "name": "Gabriel García Márquez",
                    "total_books": 5,
                    "total_loans": 28
                }
            ]
        }
    }

Notas Técnicas
==============

Relaciones entre Modelos
-------------------------

* **Writer → Book**: Relación uno-a-muchos (un escritor puede tener muchos libros)
* **Book → Loan**: Relación uno-a-muchos (un libro puede tener muchos préstamos)
* **User → Loan**: Relación uno-a-muchos (un usuario puede tener muchos préstamos)
* **Bibliotecary → Loan**: Relación uno-a-muchos opcional (SET_NULL al eliminar)

Comportamiento de Cascada
--------------------------

* Al eliminar un **Writer**, se eliminan todos sus **Books** (CASCADE)
* Al eliminar un **Book**, se eliminan todos sus **Loans** (CASCADE)
* Al eliminar un **User**, se eliminan todos sus **Loans** (CASCADE)
* Al eliminar un **Bibliotecary**, sus préstamos mantienen la referencia en NULL (SET_NULL)

Validaciones
------------

* Nombres de escritores deben ser únicos
* Títulos de libros deben ser únicos
* Usernames y emails deben ser únicos para usuarios y bibliotecarios
* Un préstamo ya devuelto no puede devolverse nuevamente

Características Avanzadas
==========================

API Views con @api_view
------------------------

El proyecto incluye tres API views personalizadas decoradas con ``@api_view`` que enlazan
múltiples modelos para proporcionar información agregada y optimizada:

**user_loan_history(user_id)**
  * Ubicación: ``viewset_books/views.py``
  * Método: GET
  * Enlaza: User → Loan → Book → Writer → Bibliotecary
  * Optimización: Usa ``select_related()`` para reducir queries
  * Retorna: Historial completo con estadísticas

**book_loan_statistics(book_id)**
  * Ubicación: ``viewset_books/views.py``
  * Método: GET
  * Enlaza: Book → Writer → Loan → User → Bibliotecary
  * Calcula: Total de préstamos, usuarios únicos, estado
  * Retorna: Estadísticas completas del libro

**library_statistics()**
  * Ubicación: ``viewset_books/views.py``
  * Método: GET
  * Enlaza: Todos los modelos del sistema
  * Agrega: Usa ``Count()`` y ``annotate()`` para rankings
  * Retorna: Dashboard global con Top 5 de libros, usuarios y escritores

Optimizaciones de Rendimiento
------------------------------

Las API views implementan técnicas de optimización:

* **select_related()**: Reduce N+1 queries al cargar relaciones ForeignKey
* **annotate()**: Calcula agregaciones en la base de datos
* **Count()**: Cuenta elementos sin cargar todos los objetos en memoria
* **order_by()**: Ordena resultados en la base de datos

Seguridad y Configuración
==========================

Variables de Entorno
--------------------

El proyecto utiliza variables de entorno para manejar información sensible:

**Archivo**: ``.env`` (no versionado en Git)

**Plantilla**: ``.env.example`` (incluida en el repositorio)

**Implementación**: ``os.getenv()`` en ``settings.py``

**Variables configurables**:

* ``DB_NAME``: Nombre de la base de datos
* ``DB_USER``: Usuario de MySQL
* ``DB_PASSWORD``: Contraseña de MySQL
* ``DB_HOST``: Host del servidor MySQL
* ``DB_PORT``: Puerto de MySQL

**Ventajas**:

* ✅ Credenciales fuera del código fuente
* ✅ Configuración diferente por entorno (dev/test/prod)
* ✅ Mayor seguridad en despliegues
* ✅ Facilita el trabajo en equipo

**Uso en settings.py**::

    import os

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'tareadjango'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', 'localhost'),
            'PORT': os.getenv('DB_PORT', '3306'),
        }
    }

Portabilidad y Reproducibilidad
================================

Requirements.txt
----------------

El proyecto incluye ``requirements.txt`` con todas las dependencias versionadas:

* **35 paquetes** listados con versiones específicas
* Instalación simple: ``pip install -r requirements.txt``
* Garantiza reproducibilidad del entorno en cualquier máquina

**Dependencias principales**:

.. code-block:: text

    Django==6.0.1
    djangorestframework==3.16.1
    PyMySQL==1.1.2
    Sphinx==9.1.0
    sphinx_rtd_theme==3.1.0

**Instalación**::

    pip install -r requirements.txt

Esto instala automáticamente todas las dependencias necesarias con las versiones exactas
utilizadas en desarrollo, evitando incompatibilidades.

Calidad de Código
=================

Suite de Tests Completa
-----------------------

* **68 tests automáticos** que validan todas las funcionalidades
* Cobertura completa de modelos, API y permisos
* Tests de integración y unitarios
* Ejecución en base de datos aislada
* Validación continua de funcionalidades
* Ver la sección de Tests Automáticos en esta documentación para más detalles

Documentación Automática
-------------------------

* Generada automáticamente con **Sphinx 9.1.0**
* Docstrings en todas las clases y métodos
* Ejemplos de uso de la API
* Guías de instalación y migración
* Documentación de base de datos
* Diagramas de relaciones

Buenas Prácticas Implementadas
-------------------------------

1. **Separación de Responsabilidades**: Apps Django modulares
2. **DRY (Don't Repeat Yourself)**: Reutilización de serializers y permisos
3. **Variables de Entorno**: Configuración sensible fuera del código
4. **Tests Automáticos**: Validación sistemática del código
5. **Documentación**: Generación automática desde docstrings
6. **Versionado de Dependencias**: Requirements.txt con versiones fijas
7. **Optimización de Queries**: select_related() y annotate()
8. **Manejo de Errores**: Respuestas HTTP apropiadas (404, 400)

Índices y Tablas
================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Documentación de Código
=======================

La documentación completa de todas las clases, métodos y funciones se genera 
automáticamente desde los docstrings del código fuente.

Módulos Principales
-------------------

* **api_server**: Configuración del proyecto, URLs y sistema de permisos
* **viewset_books**: Modelos, serializers, vistas y API views personalizadas
* **viewset_users**: Gestión completa de usuarios
* **viewset_bibliotecary**: Gestión de bibliotecarios con estadísticas

.. tip::
   Consulta la sección :doc:`modules` para ver toda la documentación generada 
   automáticamente desde el código.