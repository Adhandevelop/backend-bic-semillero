# Sistema de Gestion de Transporte

Backend academico desarrollado con Django y Django REST Framework para administrar buses, conductores, rutas y viajes. El proyecto expone una API REST preparada para ser consumida por un frontend en Angular.

## Tabla de Contenido

- [Caracteristicas](#caracteristicas)
- [Tecnologias](#tecnologias)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Instalacion](#instalacion)
- [Ejecucion](#ejecucion)
- [Endpoints](#endpoints)
- [Validaciones Principales](#validaciones-principales)
- [Pruebas](#pruebas)

## Caracteristicas

- Gestion completa de buses, conductores, rutas y viajes.
- API REST con operaciones CRUD mediante `ModelViewSet`.
- Rutas generadas automaticamente con routers de Django REST Framework.
- Endpoints adicionales para filtrar recursos activos y viajes por estado.
- Acciones personalizadas para iniciar, finalizar y cancelar viajes.
- Validaciones de negocio desde serializers.
- Panel administrativo de Django con todos los modelos registrados.
- CORS configurado para integracion con Angular en `http://localhost:4200`.
- Base de datos PostgreSQL/PostGIS configurada mediante variables de entorno.

## Tecnologias

| Herramienta | Uso |
| --- | --- |
| Django | Framework principal del backend |
| Django REST Framework | Construccion de la API REST |
| django-cors-headers | Configuracion CORS para Angular |
| python-dotenv | Carga de variables desde `.env` |
| PostgreSQL/PostGIS | Base de datos del proyecto |
| GDAL/GEOS | Librerias nativas requeridas por GeoDjango/PostGIS |

## Estructura del Proyecto

```text
backend/
|-- manage.py
|-- requirements.txt
|-- .env.example
|-- README.md
|-- backend/
|   |-- settings.py
|   |-- urls.py
|   |-- asgi.py
|   `-- wsgi.py
`-- transporte/
    |-- admin.py
    |-- apps.py
    |-- models.py
    |-- serializers.py
    |-- views.py
    |-- urls.py
    |-- tests.py
    `-- migrations/
```

## Instalacion

1. Clonar el repositorio:

```bash
git clone https://github.com/Adhandevelop/backend-bic-semillero.git
cd backend-bic-semillero/backend
```

2. Crear y activar un entorno virtual:

```bash
python -m venv .venv
```

En Windows:

```bash
.venv\Scripts\activate
```

En macOS o Linux:

```bash
source .venv/bin/activate
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Crear el archivo `.env` desde la plantilla:

```bash
copy .env.example .env
```

En macOS o Linux:

```bash
cp .env.example .env
```

5. Configurar `.env` con los datos de PostgreSQL/PostGIS:

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
CORS_ALLOWED_ORIGINS=http://localhost:4200

DB_NAME=semillero_transporte
DB_USER=semillero_user
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=5431

# Opcional si el servidor requiere rutas explicitas:
GDAL_LIBRARY_PATH=
GEOS_LIBRARY_PATH=
```

6. Verificar configuracion, crear migraciones y aplicar la base de datos:

```bash
python manage.py check
python manage.py makemigrations
python manage.py migrate
```

7. Crear un superusuario:

```bash
python manage.py createsuperuser
```

## Ejecucion

```bash
python manage.py runserver
```

Servicios disponibles:

| Servicio | URL |
| --- | --- |
| API REST | `http://127.0.0.1:8000/api/` |
| Admin Django | `http://127.0.0.1:8000/admin/` |

## Variables de Entorno

| Variable | Descripcion | Ejemplo |
| --- | --- | --- |
| `SECRET_KEY` | Clave secreta de Django | `change-me` |
| `DEBUG` | Activa modo desarrollo | `True` |
| `ALLOWED_HOSTS` | Hosts permitidos separados por coma | `127.0.0.1,localhost` |
| `CORS_ALLOWED_ORIGINS` | Origenes CORS separados por coma | `http://localhost:4200` |
| `DB_NAME` | Nombre de la base de datos | `semillero_transporte` |
| `DB_USER` | Usuario de PostgreSQL | `semillero_user` |
| `DB_PASSWORD` | Password del usuario de base de datos | `tu_password` |
| `DB_HOST` | Host de PostgreSQL/PostGIS | `127.0.0.1` |
| `DB_PORT` | Puerto de PostgreSQL/PostGIS | `5431` |
| `GDAL_LIBRARY_PATH` | Ruta opcional a la libreria GDAL | vacio si el sistema ya la encuentra |
| `GEOS_LIBRARY_PATH` | Ruta opcional a la libreria GEOS | vacio si el sistema ya la encuentra |

> Nota: GeoDjango con PostGIS requiere las librerias nativas GDAL/GEOS instaladas en el sistema o disponibles dentro del contenedor/servidor.

## Endpoints

### CRUD principal

| Recurso | Endpoint |
| --- | --- |
| Buses | `/api/buses/` |
| Conductores | `/api/conductores/` |
| Rutas | `/api/rutas/` |
| Viajes | `/api/viajes/` |

Cada recurso principal soporta:

```text
GET, POST, GET /{id}/, PUT, PATCH, DELETE
```

### Consultas adicionales

| Metodo | Endpoint | Descripcion |
| --- | --- | --- |
| GET | `/api/buses/activos/` | Lista buses activos |
| GET | `/api/conductores/activos/` | Lista conductores activos |
| GET | `/api/rutas/activas/` | Lista rutas activas |
| GET | `/api/viajes/programados/` | Lista viajes programados |
| GET | `/api/viajes/en-curso/` | Lista viajes en curso |
| GET | `/api/viajes/finalizados/` | Lista viajes finalizados |
| PATCH | `/api/viajes/{id}/iniciar/` | Cambia un viaje a `en_curso` |
| PATCH | `/api/viajes/{id}/finalizar/` | Cambia un viaje a `finalizado` |
| PATCH | `/api/viajes/{id}/cancelar/` | Cambia un viaje a `cancelado` |

## Validaciones Principales

- La capacidad de un bus debe ser mayor que cero.
- La placa del bus se almacena en mayuscula.
- La licencia del conductor se almacena en mayuscula.
- No se permiten viajes con buses inactivos o en mantenimiento.
- No se permiten viajes con conductores inactivos.
- No se permiten viajes con rutas inactivas.
- Si `fecha_hora_fin` existe, debe ser mayor que `fecha_hora_inicio`.
- Todo viaje debe tener bus, conductor y ruta.

## Pruebas

```bash
python manage.py test
```

## Autor

Proyecto academico para semillero backend.
