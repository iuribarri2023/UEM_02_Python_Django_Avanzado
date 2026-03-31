# Construction Material Control API
Universidad Europea
Fundamentos de backend con Python
Ejercicio entregable

## Descripcion
API REST construida con Django y Django REST Framework para gestionar obras de construccion y el control de materiales recibidos en cada proyecto.

La API tiene una logica de negocio coherente:
- `ConstructionProject` representa una obra.
- `ProjectMaterial` representa una entrada de material asociada a una obra.

De esta forma se puede registrar que materiales llegan a una obra, quien los recepciona, donde se almacenan, cuanto se ha consumido y cual es el resumen total por proyecto.

## Estructura del proyecto
- `backend/manage.py`: punto de entrada de Django para arrancar el servidor, aplicar migraciones y lanzar tests.
- `backend/constru_app/settings.py`: configuracion global del proyecto, REST Framework, autenticacion por token, configuracion actual de SQLite y drf-spectacular.
- `backend/constru_app/urls.py`: rutas principales del proyecto, incluyendo schema OpenAPI y Swagger UI.
- `backend/projects/models.py`: modelos `ConstructionProject` y `ProjectMaterial`.
- `backend/projects/serializers.py`: serializers y validaciones del dominio.
- `backend/projects/permissions.py`: permisos para `Engineers` y `Workers`.
- `backend/projects/views.py`: viewset, vistas genericas y api_view personalizada.
- `backend/projects/urls.py`: rutas de la app `projects`.
- `backend/projects/tests.py`: pruebas automatizadas.
- `backend/projects/management/commands/bootstrap_demo.py`: comando para crear usuarios y datos demo reproducibles.
- `backend/projects/migrations/0001_initial.py`: migracion inicial de modelos.
- `backend/projects/migrations/0002_create_groups.py`: migracion que crea grupos y permisos.
- `backend/.env.example`: ejemplo de variables de entorno locales.
- `backend/convert-utf8.py`: script auxiliar para convertir un volcado a UTF-8 en Windows.
- `backend/db.sqlite3`: base de datos SQLite local generada por Django.
- `PruebaEndpoints.postman_collection.json`: coleccion Postman de prueba.
- `public/Memoria_API_Construccion.rtf`: memoria del proyecto.

## Requisitos del enunciado cubiertos
- Gestion de usuarios con 2 grupos: `Engineers` y `Workers`.
- Restriccion de permisos para el grupo no administrador.
- Implementacion de al menos 1 viewset: `ProjectViewSet`.
- Proyecto portable con `requirements.txt`.
- Aplicacion de DRY mediante mixins reutilizados para vistas y permisos.
- Implementacion de 2 modelos relacionados y con sentido de negocio.
- 4 vistas genericas distintas para cada modelo.
- 1 `api_view` propia que enlaza modelos: `project_materials_summary`.
- Implementacion real del proyecto con SQLite.
- Documentacion interactiva con OpenAPI y Swagger UI mediante `drf-spectacular`.
- Explicacion documental de como se haria la migracion a MySQL.

## Base de datos actual: SQLite
La base de datos real implementada en el codigo es SQLite. Django la gestiona directamente mediante el archivo:

- `backend/db.sqlite3`

No hace falta instalar servidores adicionales ni crear la base de datos manualmente. Django crea el archivo y las tablas automaticamente al ejecutar las migraciones.

## Instalacion y ejecucion
1. Crear el entorno virtual:
```powershell
py -m venv venv
```

2. Activar el entorno en Windows:
```powershell
.\venv\Scripts\activate
```

3. Instalar las librerias necesarias:
```powershell
pip install -r requirements.txt
```

4. Entrar en la carpeta del proyecto Django:
```powershell
cd backend
```

5. Aplicar las migraciones para crear las tablas de Django y de la app `projects`:
```powershell
py .\manage.py migrate
```

6. Crear usuarios y datos demo reproducibles:
```powershell
py .\manage.py bootstrap_demo
```

Este comando crea o actualiza:
- usuario `engineer` con password `engineer123`
- usuario `worker` con password `worker123`
- proyecto demo `OBR-001`
- material demo asociado al proyecto
- tokens de autenticacion para ambos usuarios

7. Crear un superusuario si se quiere acceder al panel de administracion:
```powershell
py .\manage.py createsuperuser
```

8. Ejecutar el servidor:
```powershell
py .\manage.py runserver
```

9. Probar la API en:
- `http://127.0.0.1:8000/admin/`
- `http://127.0.0.1:8000/auth/token/`
- `http://127.0.0.1:8000/api/schema/`
- `http://127.0.0.1:8000/api/docs/`
- `http://127.0.0.1:8000/api/projects/list/`
- `http://127.0.0.1:8000/api/materials/list/`

## Variables de entorno
El proyecto puede leer configuracion desde:
- `backend/.env.example`
- `backend/.env`

En la implementacion actual con SQLite, un ejemplo suficiente seria:
```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

No es necesario incluir variables de base de datos porque `backend/constru_app/settings.py` usa SQLite directamente.

## Usuarios, grupos y permisos
La API define dos grupos distintos, creados automaticamente en la migracion `backend/projects/migrations/0002_create_groups.py`:
- `Engineers`
- `Workers`

Permisos principales:
- `Engineers`: pueden crear, consultar, actualizar y borrar proyectos y materiales.
- `Workers`: pueden consultar proyectos, consultar materiales y registrar nuevas entradas de material.
- `Workers` no pueden crear proyectos.
- `Workers` no pueden actualizar ni borrar materiales ya registrados.

## Endpoints principales
Raiz local de la API:
- `http://127.0.0.1:8000/`

Autenticacion:
- `POST /auth/token/`

Documentacion API:
- `GET /api/schema/`: esquema OpenAPI generado por `drf-spectacular`.
- `GET /api/docs/`: interfaz Swagger UI para consumir y probar la API.

Proyectos:
- `GET /api/projects/viewset/`
- `POST /api/projects/viewset/`
- `GET /api/projects/viewset/<code>/`
- `PUT /api/projects/viewset/<code>/`
- `PATCH /api/projects/viewset/<code>/`
- `DELETE /api/projects/viewset/<code>/`
- `GET /api/projects/list/`
- `POST /api/projects/create/`
- `GET /api/projects/<code>/detail/`
- `PUT/PATCH /api/projects/<code>/update/`

Materiales:
- `GET /api/materials/list/`
- `POST /api/materials/create/`
- `GET /api/materials/<id>/detail/`
- `PUT/PATCH /api/materials/<id>/update/`

API personalizada que enlaza modelos:
- `GET /api/projects/<code>/materials-summary/`

## Swagger y consumo de la API
La documentacion interactiva se genera con `drf-spectacular`.

- `GET /api/schema/` devuelve el esquema OpenAPI de la API.
- `GET /api/docs/` abre Swagger UI.

Desde Swagger UI se pueden inspeccionar los endpoints, ver sus parametros y probar peticiones directamente. En los endpoints protegidos por token, basta con obtener primero un token en `/auth/token/` y despues incluirlo en Swagger con el formato `Token <tu_token>`.

## Coleccion Postman
La coleccion `PruebaEndpoints.postman_collection.json` esta preparada para funcionar con el flujo real del proyecto. Antes de usarla se recomienda ejecutar:
```powershell
py .\manage.py bootstrap_demo
```

Luego, en Postman, basta con lanzar las peticiones en este orden:
1. `Auth - Engineer Token`
2. `Auth - Worker Token`
3. `Projects - Create With Engineer`
4. `Materials - Create With Worker`
5. `Materials - Update With Engineer`
6. `Projects - Materials Summary`

La coleccion guarda automaticamente tokens, `projectId`, `projectCode` y `materialId` para no depender de identificadores fijos.

## Interaccion entre Django y SQLite
En `backend/constru_app/settings.py` la base de datos configurada es SQLite. Esto implica que Django trabaja sobre el archivo `backend/db.sqlite3` y utiliza el ORM para gestionar automaticamente tablas, relaciones y consultas.

El flujo real es este:
1. Django arranca con la configuracion definida en `settings.py`.
2. La seccion `DATABASES` utiliza `django.db.backends.sqlite3`.
3. Al ejecutar `py .\manage.py migrate`, Django crea `backend/db.sqlite3` si no existe.
4. Las migraciones crean las tablas de autenticacion, permisos, sesiones y las tablas de `ConstructionProject` y `ProjectMaterial`.
5. A partir de ese momento, todas las operaciones CRUD se realizan contra SQLite mediante el ORM de Django.

## Exportar datos desde SQLite
Aunque el proyecto actual se entrega con SQLite, se puede explicar como exportar sus datos para una futura migracion.

Desde la carpeta `backend/`, el comando recomendado es:
```powershell
py .\manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission --indent 4 --output datadump.json
```

Este comando genera un fichero `datadump.json` con los datos del proyecto excluyendo contenido que no conviene volcar directamente, como `contenttypes` y `auth.permission`.

### Conversion a UTF-8 en Windows
En sistemas Windows puede ocurrir que el volcado no quede en UTF-8. Si eso sucede, se puede convertir ejecutando:
```powershell
py .\convert-utf8.py
```

El script intenta leer primero en UTF-8 y, si fuera necesario, prueba codificaciones tipicas de Windows antes de generar `datadump_utf8.json` en UTF-8.

## Como se haria esta misma solucion en MySQL
MySQL no esta implementado en el codigo actual, pero en la memoria del trabajo es importante explicar como se haria la migracion desde SQLite. El proceso, siguiendo una logica como la del ejemplo aportado, seria el siguiente.

### 1. Crear una base de datos MySQL
Por ejemplo:
```sql
CREATE DATABASE construction_material_control CHARACTER SET UTF8;

GRANT ALL PRIVILEGES ON construction_material_control.* TO construction_user@localhost;
```

### 2. Crear un fichero `.env`
Ese fichero se colocaria en `backend/`, junto a `manage.py`, con informacion como esta:
```env
DB_NAME=construction_material_control
DB_USER=construction_user
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
```

### 3. Adaptar `backend/constru_app/settings.py`
Habria que sustituir la configuracion SQLite por una configuracion con `django.db.backends.mysql` y leer las credenciales anteriores.

### 4. Crear las tablas en MySQL
Una vez adaptada la configuracion, se ejecutaria:
```powershell
py .\manage.py migrate
```

Con ello Django crearia en MySQL todas las tablas necesarias del proyecto y del propio framework.

### 5. Exportar los datos existentes desde SQLite
Si previamente el proyecto ya contuviera informacion en `backend/db.sqlite3`, se exportaria con:
```powershell
py .\manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission --indent 4 --output datadump.json
```

### 6. Convertir el volcado si fuera necesario
En Windows, si el fichero no estuviera en UTF-8, se usaria:
```powershell
py .\convert-utf8.py
```

### 7. Importar los datos en MySQL
Con la base de datos MySQL ya creada y las tablas migradas, se cargarian los datos con:
```powershell
py .\manage.py loaddata .\datadump_utf8.json
```

### 8. Arrancar el servidor ya sobre MySQL
Finalmente, se levantaria el proyecto con:
```powershell
py .\manage.py runserver
```

## Tests
Hay una serie de tests en `backend/projects/tests.py` que verifican el buen funcionamiento de la API. Para ejecutarlos:
```powershell
cd backend
py .\manage.py test projects
```

Tambien es recomendable ejecutar:
```powershell
py .\manage.py check
```

## Conclusiones
Django resulta muy comodo para este tipo de practicas porque automatiza gran parte del trabajo relacionado con modelos, migraciones, validaciones y permisos.

En este proyecto, SQLite simplifica mucho la ejecucion local y permite que la API funcione sin configuracion adicional. Ademas, `drf-spectacular` aporta una forma clara de consumir y probar la API desde Swagger UI. Por otro lado, tambien queda documentado como se podria migrar el mismo proyecto a MySQL exportando los datos desde SQLite, convirtiendo el volcado a UTF-8 si fuera necesario e importandolo despues en la nueva base de datos.
