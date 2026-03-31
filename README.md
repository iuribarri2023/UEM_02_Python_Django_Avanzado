# Construction Material Control API

API REST construida con Django y Django REST Framework para gestionar obras de construccion y el control de materiales recibidos en cada proyecto.

## Idea del proyecto

La API tiene sentido de negocio: una obra puede recibir multiples materiales y cada entrega queda registrada con informacion util para el seguimiento real de obra.

- `ConstructionProject` representa una obra.
- `ProjectMaterial` representa una entrega o registro de material asociado a una obra.

De esta forma se puede conocer que materiales se han recibido, donde se almacenan, quien los recepciono, cuanto se ha consumido y el resumen total por proyecto.

## Requisitos del enunciado cubiertos

- Gestion de usuarios con 2 grupos: `Engineers` y `Workers`.
- Restriccion de permisos para el grupo no administrador.
- Al menos 1 viewset: `ProjectViewSet`.
- Uso de MySQL como base de datos principal.
- Proyecto portable con `requirements.txt`.
- Aplicacion de DRY mediante mixins reutilizados para vistas, permisos y configuracion comun.
- Implementacion de 2 modelos con relacion real de negocio.
- 4 vistas genericas distintas para cada modelo:
  `ListAPIView`, `CreateAPIView`, `RetrieveAPIView` y `UpdateAPIView`.
- 1 `api_view` propia que enlaza modelos:
  `project_materials_summary`.

## Estructura Django

La estructura actual del proyecto sigue la organizacion habitual de Django:

- `constru_app/constru_app/`
  paquete interno del proyecto con `settings.py`, `urls.py`, `wsgi.py` y `asgi.py`.
- `constru_app/projects/`
  app principal con modelos, serializers, permisos, vistas, tests, admin y migraciones.

## Modelos

### ConstructionProject

Modelo rico para representar una obra:

- `code`
- `name`
- `project_type`
- `client_name`
- `site_address`
- `city`
- `project_manager`
- `engineer_in_charge`
- `contract_reference`
- `start_date`
- `expected_end_date`
- `budget`
- `status`
- `progress_percentage`
- `notes`

### ProjectMaterial

Modelo rico para registrar materiales recibidos en obra:

- `project`
- `category`
- `material_name`
- `supplier`
- `delivery_note`
- `batch_reference`
- `storage_zone`
- `received_by`
- `unit`
- `planned_quantity`
- `received_quantity`
- `consumed_quantity`
- `unit_cost`
- `received_on`
- `quality_checked`
- `remarks`
- `updated_at`

## Roles y permisos

### Engineers

Responsables tecnicos con control completo.

- Pueden crear, listar, consultar, modificar y borrar proyectos.
- Pueden crear, listar, consultar, modificar y borrar materiales.
- Pueden usar el endpoint de resumen que enlaza proyecto y materiales.

### Workers

Personal de obra con permisos limitados.

- Pueden consultar proyectos.
- Pueden consultar materiales.
- Pueden registrar nuevas recepciones de material.
- No pueden crear proyectos.
- No pueden modificar proyectos.
- No pueden modificar ni borrar materiales ya registrados.

Los grupos y permisos se crean automaticamente en la migracion `projects.0002_create_groups`.

## Endpoints

Base URL: `http://127.0.0.1:8000/`

### Autenticacion

- `POST /auth/token/`

### Viewset de proyectos

- `GET /api/projects/viewset/`
- `POST /api/projects/viewset/`
- `GET /api/projects/viewset/<code>/`
- `PUT /api/projects/viewset/<code>/`
- `PATCH /api/projects/viewset/<code>/`
- `DELETE /api/projects/viewset/<code>/`

### Vistas genericas de proyectos

- `GET /api/projects/list/`
- `POST /api/projects/create/`
- `GET /api/projects/<code>/detail/`
- `PUT/PATCH /api/projects/<code>/update/`

### Vistas genericas de materiales

- `GET /api/materials/list/`
- `POST /api/materials/create/`
- `GET /api/materials/<id>/detail/`
- `PUT/PATCH /api/materials/<id>/update/`

### API personalizada que enlaza modelos

- `GET /api/projects/<code>/materials-summary/`

Devuelve:

- informacion del proyecto
- listado de materiales del proyecto
- resumen agregado de cantidades planificadas, recibidas, consumidas y disponibles

## Instalacion

1. Crear un entorno virtual:

```powershell
py -m venv venv
```

2. Activarlo:

```powershell
.\venv\Scripts\activate
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Crear `constru_app/.env` a partir de `constru_app/.env.example`:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
DB_ENGINE=mysql
DB_NAME=construction_material_control
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
```

5. Entrar en la carpeta del proyecto Django:

```powershell
cd .\constru_app\
```

6. Ejecutar migraciones:

```powershell
..\venv\Scripts\python.exe manage.py migrate
```

7. Crear superusuario:

```powershell
..\venv\Scripts\python.exe manage.py createsuperuser
```

8. Lanzar el servidor:

```powershell
..\venv\Scripts\python.exe manage.py runserver
```

## MySQL y migracion desde SQLite paso a paso

La base de datos principal del proyecto es MySQL. Si el proyecto hubiese empezado en SQLite, la migracion recomendada es esta:

1. Trabajar inicialmente con SQLite usando:

```env
DB_ENGINE=sqlite
```

2. Cuando el modelo ya este estable, instalar el driver de MySQL:

```powershell
pip install mysqlclient
```

3. Crear la base de datos en MySQL:

```sql
CREATE DATABASE construction_material_control
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

4. Cambiar `.env` para apuntar a MySQL:

```env
DB_ENGINE=mysql
DB_NAME=construction_material_control
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
```

5. Generar un volcado de los datos desde SQLite:

```powershell
..\venv\Scripts\python.exe manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission --indent 2 > datadump.json
```

6. Si Windows genera el archivo con una codificacion conflictiva, convertirlo con:

```powershell
..\venv\Scripts\python.exe .\convert-utf8.py
```

7. Crear la estructura en MySQL:

```powershell
..\venv\Scripts\python.exe manage.py migrate
```

8. Cargar los datos en MySQL:

```powershell
..\venv\Scripts\python.exe manage.py loaddata datadump_utf8.json
```

9. Verificar que usuarios, grupos, proyectos y materiales se han importado correctamente.

## Tests

Los tests comprueban:

- que `Engineers` pueden crear proyectos
- que `Workers` no pueden crear proyectos
- que `Workers` pueden registrar materiales
- que `Workers` no pueden modificar materiales
- que `Engineers` si pueden modificar materiales
- que la `api_view` de resumen enlaza correctamente ambos modelos

Ejecucion:

```powershell
cd .\constru_app\
..\venv\Scripts\python.exe manage.py test projects
```

Durante los tests se usa SQLite automaticamente para no depender de un servidor MySQL local.
