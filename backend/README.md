# Sistema de Gestion de Transporte

Backend academico construido con Django y Django REST Framework para gestionar buses, conductores, rutas y viajes.

## Requisitos

- Python 3.10 o superior
- pip

## Instalacion

```bash
pip install -r requirements.txt
```

## Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

## Crear superusuario

```bash
python manage.py createsuperuser
```

## Ejecutar servidor

```bash
python manage.py runserver
```

La API queda disponible en:

```text
http://127.0.0.1:8000/api/
```

El panel de administracion queda disponible en:

```text
http://127.0.0.1:8000/admin/
```

## Endpoints principales

- `/api/buses/`
- `/api/conductores/`
- `/api/rutas/`
- `/api/viajes/`

Cada endpoint principal soporta `GET`, `POST`, `GET /{id}/`, `PUT`, `PATCH` y `DELETE`.

## Endpoints adicionales

- `GET /api/buses/activos/`
- `GET /api/conductores/activos/`
- `GET /api/rutas/activas/`
- `GET /api/viajes/programados/`
- `GET /api/viajes/en-curso/`
- `GET /api/viajes/finalizados/`
- `PATCH /api/viajes/{id}/iniciar/`
- `PATCH /api/viajes/{id}/finalizar/`
- `PATCH /api/viajes/{id}/cancelar/`

## CORS

El proyecto permite solicitudes desde Angular en:

```text
http://localhost:4200
```

## Pruebas

```bash
python manage.py test
```
