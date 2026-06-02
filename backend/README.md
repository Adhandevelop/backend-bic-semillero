# Backend - Sistema de Gestion de Transporte

API REST construida con Django y Django REST Framework para gestionar buses, conductores, rutas y viajes.

## Requisitos

- Python 3.10 o superior
- pip
- Entorno virtual recomendado
- PostgreSQL/PostGIS disponible en Docker

## Instalacion Rapida

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py check
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

## Configuracion

El backend carga variables desde `.env` usando `python-dotenv`. El archivo `.env` no debe subirse al repositorio; usa `.env.example` como plantilla.

```env
SECRET_KEY=change-me
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost,72.60.175.200
CORS_ALLOWED_ORIGINS=http://localhost:4200,http://72.60.175.200,http://72.60.175.200:4200

DB_NAME=semillero_transporte
DB_USER=semillero_user
DB_PASSWORD=tu_password
DB_HOST=127.0.0.1
DB_PORT=5431

# Opcional si el servidor requiere rutas explicitas:
GDAL_LIBRARY_PATH=
GEOS_LIBRARY_PATH=
```

La base de datos usa el backend PostGIS de Django:

```text
django.contrib.gis.db.backends.postgis
```

CORS permite solicitudes desde:

```text
http://localhost:4200
```

Tambien se permite el frontend desplegado en:

```text
http://72.60.175.200
http://72.60.175.200:4200
```

GeoDjango con PostGIS requiere que las librerias nativas GDAL/GEOS esten instaladas en el sistema o disponibles dentro del contenedor/servidor. Si Django no las detecta automaticamente, define `GDAL_LIBRARY_PATH` y `GEOS_LIBRARY_PATH` en `.env`.

## Modelos

| Modelo | Campos principales |
| --- | --- |
| Bus | `placa`, `capacidad`, `modelo`, `estado` |
| Conductor | `nombre`, `licencia`, `telefono`, `estado` |
| Ruta | `origen`, `destino`, `distancia_km`, `estado` |
| Viaje | `bus`, `conductor`, `ruta`, `fecha_hora_inicio`, `fecha_hora_fin`, `estado` |

## Endpoints

### Autenticacion JWT

```text
POST /api/token/
POST /api/token/refresh/
```

Login:

```bash
curl -X POST http://72.60.175.200/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"TU_PASSWORD"}'
```

La respuesta contiene:

```json
{
  "access": "token_access",
  "refresh": "token_refresh"
}
```

Enviar el access token en las peticiones protegidas:

```text
Authorization: Bearer token_access
```

| Recurso | Endpoint |
| --- | --- |
| Buses | `/api/buses/` |
| Conductores | `/api/conductores/` |
| Rutas | `/api/rutas/` |
| Viajes | `/api/viajes/` |

Endpoints adicionales:

```text
GET   /api/buses/activos/
GET   /api/conductores/activos/
GET   /api/rutas/activas/
GET   /api/viajes/programados/
GET   /api/viajes/en-curso/
GET   /api/viajes/finalizados/
PATCH /api/viajes/{id}/iniciar/
PATCH /api/viajes/{id}/finalizar/
PATCH /api/viajes/{id}/cancelar/
```

## Pruebas

```bash
python manage.py test
```

## Notas de Desarrollo

- Los serializers validan las reglas de negocio del proyecto.
- `ViajeSerializer` permite enviar IDs de `bus`, `conductor` y `ruta`.
- Las respuestas de viajes incluyen detalles de bus, conductor y ruta mediante campos de solo lectura.
- Todos los modelos estan registrados en el admin de Django.
