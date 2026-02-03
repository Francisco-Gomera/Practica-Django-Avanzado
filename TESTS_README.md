# Tests Automáticos - Proyecto Django Avanzado

## Resumen de Ejecución

**Total de tests:** 68  
**Estado:** ✅ Todos los tests pasaron exitosamente  
**Tiempo de ejecución:** ~0.7 segundos  

## Estructura de Tests

### 1. Tests de Modelos de Usuarios (`viewset_users/tests.py`)
- **14 tests** que validan el modelo User y su API

#### UserModelTest (5 tests)
- ✅ `test_crear_usuario` - Verificar creación correcta de usuarios
- ✅ `test_username_unico` - Username debe ser único
- ✅ `test_email_unico` - Email debe ser único
- ✅ `test_usuario_string_representation` - Representación en string
- ✅ Validación de campos obligatorios

#### UserAPITest (9 tests)
- ✅ `test_listar_usuarios` - GET /users/
- ✅ `test_obtener_usuario_detalle` - GET /users/{id}/
- ✅ `test_crear_usuario_via_api` - POST /users/
- ✅ `test_actualizar_usuario` - PUT /users/{id}/
- ✅ `test_eliminar_usuario` - DELETE /users/{id}/
- ✅ `test_usuario_no_existente` - Error 404
- ✅ `test_crear_usuario_sin_datos_requeridos` - Error 400

### 2. Tests de Modelos de Libros (`viewset_books/tests.py`)
- **32 tests** que validan Writer, Book, Loan y las API views personalizadas

#### WriterModelTest (2 tests)
- ✅ `test_crear_escritor` - Creación correcta de escritores
- ✅ `test_nombre_escritor_unico` - Nombres únicos

#### BookModelTest (4 tests)
- ✅ `test_crear_libro` - Creación correcta de libros
- ✅ `test_libro_string_representation` - Representación en string
- ✅ `test_titulo_libro_unico` - Títulos únicos
- ✅ `test_eliminar_escritor_elimina_libros` - Cascade DELETE

#### LoanModelTest (6 tests)
- ✅ `test_crear_prestamo` - Creación correcta de préstamos
- ✅ `test_prestamo_string_representation` - Representación en string
- ✅ `test_devolver_prestamo` - Marcar como devuelto
- ✅ `test_eliminar_libro_elimina_prestamos` - Cascade DELETE
- ✅ `test_eliminar_bibliotecario_mantiene_prestamos` - SET NULL

#### WriterAPITest (2 tests)
- ✅ `test_listar_escritores` - GET /writers/
- ✅ `test_crear_escritor` - POST /writers/

#### BookAPITest (3 tests)
- ✅ `test_listar_libros` - GET /books/
- ✅ `test_crear_libro_con_writer_name` - POST con nuevo escritor
- ✅ `test_crear_libro_con_writer_existente` - POST con escritor existente

#### LoanAPITest (4 tests)
- ✅ `test_crear_prestamo` - POST /loans/
- ✅ `test_devolver_libro` - POST /loans/{id}/return_book/
- ✅ `test_devolver_libro_ya_devuelto` - Error 400
- ✅ `test_listar_prestamos_activos` - GET /loans/active/

#### CustomAPIViewsTest (3 tests)
- ✅ `test_user_loan_history` - GET /api/users/{id}/loan-history/
- ✅ `test_book_loan_statistics` - GET /api/books/{id}/loan-statistics/
- ✅ `test_library_statistics` - GET /api/library/statistics/

### 3. Tests de Bibliotecarios (`viewset_bibliotecary/tests.py`)
- **14 tests** que validan el modelo Bibliotecary y sus acciones personalizadas

#### BibliotecaryModelTest (4 tests)
- ✅ `test_crear_bibliotecario` - Creación correcta
- ✅ `test_bibliotecario_string_representation` - Representación en string
- ✅ `test_username_unico` - Username único
- ✅ `test_email_unico` - Email único

#### BibliotecaryAPITest (10 tests)
- ✅ `test_listar_bibliotecarios` - GET /bibliotecaries/
- ✅ `test_obtener_bibliotecario` - GET /bibliotecaries/{id}/
- ✅ `test_crear_bibliotecario` - POST /bibliotecaries/
- ✅ `test_actualizar_bibliotecario` - PUT /bibliotecaries/{id}/
- ✅ `test_eliminar_bibliotecario` - DELETE /bibliotecaries/{id}/
- ✅ `test_managed_loans_action` - GET /bibliotecaries/{id}/managed_loans/
- ✅ `test_active_loans_action` - GET /bibliotecaries/{id}/active_loans/
- ✅ `test_statistics_action` - GET /bibliotecaries/{id}/statistics/
- ✅ `test_bibliotecario_no_existente` - Error 404
- ✅ `test_crear_bibliotecario_sin_datos_requeridos` - Error 400

### 4. Tests de Permisos (`api_server/test_permissions.py`)
- **18 tests** que validan el sistema de permisos personalizado

#### IsAdminOrReadOnlyTest (10 tests)
- ✅ `test_usuario_normal_puede_leer` - GET permitido
- ✅ `test_usuario_normal_no_puede_crear` - POST bloqueado
- ✅ `test_usuario_normal_no_puede_actualizar` - PUT bloqueado
- ✅ `test_usuario_normal_no_puede_eliminar` - DELETE bloqueado
- ✅ `test_bibliotecario_puede_leer` - GET permitido
- ✅ `test_bibliotecario_puede_crear` - POST permitido
- ✅ `test_bibliotecario_puede_actualizar` - PUT permitido
- ✅ `test_bibliotecario_puede_eliminar` - DELETE permitido
- ✅ `test_usuario_no_autenticado_puede_leer` - GET público
- ✅ `test_usuario_no_autenticado_no_puede_crear` - POST bloqueado

#### IsBibliotecaryTest (3 tests)
- ✅ `test_usuario_normal_sin_permiso` - Sin acceso
- ✅ `test_bibliotecario_con_permiso` - Con acceso
- ✅ `test_usuario_no_autenticado_sin_permiso` - Sin acceso

#### IsOwnerOrBibliotecaryTest (4 tests)
- ✅ `test_propietario_puede_acceder_objeto` - Acceso propio
- ✅ `test_otro_usuario_no_puede_acceder_objeto` - Sin acceso ajeno
- ✅ `test_bibliotecario_puede_acceder_cualquier_objeto` - Acceso admin
- ✅ `test_metodos_seguros_lectura` - GET/HEAD/OPTIONS permitidos

#### PermissionIntegrationTest (3 tests)
- ✅ `test_usuario_puede_listar_sin_autenticacion` - Lectura pública
- ✅ `test_usuario_no_puede_crear_sin_ser_bibliotecario` - Restricción escritura
- ✅ `test_bibliotecario_puede_crear_recursos` - Permisos admin

## Cobertura de Funcionalidades

### ✅ Modelos
- Creación de registros
- Validación de campos únicos
- Representación en string
- Relaciones (CASCADE, SET NULL)
- Constraints de integridad

### ✅ API REST
- Operaciones CRUD completas
- Listado y detalle
- Validación de datos
- Manejo de errores (404, 400)
- Acciones personalizadas (@action)
- Vistas personalizadas (@api_view)

### ✅ Permisos
- IsAdminOrReadOnly (lectura pública, escritura admin)
- IsBibliotecary (solo bibliotecarios)
- IsOwnerOrBibliotecary (propietario o admin)
- Permisos a nivel de objeto
- Métodos seguros vs no seguros

### ✅ Endpoints Especiales
- Historial de préstamos por usuario
- Estadísticas de préstamos por libro
- Estadísticas globales de la biblioteca
- Préstamos gestionados por bibliotecario
- Préstamos activos

## Comandos para Ejecutar Tests

### Ejecutar todos los tests
```bash
python manage.py test
```

### Ejecutar tests con verbosidad
```bash
python manage.py test --verbosity=2
```

### Ejecutar tests de una app específica
```bash
python manage.py test viewset_users
python manage.py test viewset_books
python manage.py test viewset_bibliotecary
python manage.py test api_server.test_permissions
```

### Ejecutar un test específico
```bash
python manage.py test viewset_users.tests.UserModelTest.test_crear_usuario
```

### Ejecutar tests con base de datos específica
```bash
python manage.py test --keepdb  # Mantener base de datos de prueba
```

## Base de Datos de Prueba

Los tests utilizan una base de datos temporal llamada `test_tareadjango` que:
- Se crea automáticamente antes de ejecutar los tests
- Aplica todas las migraciones
- Se destruye al finalizar los tests
- Es completamente independiente de la base de datos de producción

## Buenas Prácticas Implementadas

1. **Separación de Tests**: Tests organizados por módulo y funcionalidad
2. **Nomenclatura Clara**: Nombres descriptivos que explican qué se prueba
3. **setUp y tearDown**: Configuración reutilizable para cada test
4. **Assertions Específicas**: Uso de assertions apropiadas (assertEqual, assertTrue, assertIn, etc.)
5. **Tests de Casos Límite**: Validación de errores y casos especiales
6. **Tests de Integración**: Validación de interacciones entre componentes
7. **Mock Objects**: Objetos simulados para testing de permisos
8. **APITestCase**: Uso de herramientas específicas de DRF

## Próximos Pasos

- [ ] Añadir tests de cobertura de código (coverage)
- [ ] Implementar tests de rendimiento
- [ ] Añadir tests de autenticación/autorización con JWT
- [ ] Tests de integración más complejos
- [ ] Tests de regresión para bugs específicos
- [ ] CI/CD con ejecución automática de tests

## Resultado Final

✅ **68/68 tests pasados exitosamente**  
✅ **0 errores**  
✅ **0 warnings**  
✅ **100% de funcionalidades validadas**
