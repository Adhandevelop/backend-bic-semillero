# Backend - Sistema de Gestion de Transporte

API REST construida con Django y Django REST Framework para gestionar buses, conductores, rutas y viajes.

## Requisitos

- Python 3.10 o superior
- pip
- Entorno virtual recomendado

## Instalacion Rapida

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

La API queda disponible en `http://127.0.0.1:8000/api/`.

## Configuracion

La configuracion actual usa SQLite por defecto para facilitar pruebas locales. CORS permite solicitudes desde:

```text
http://localhost:4200
```

## Modelos

| Modelo | Campos principales |
| --- | --- |
| Bus | `placa`, `capacidad`, `modelo`, `estado` |
| Conductor | `nombre`, `licencia`, `telefono`, `estado` |
| Ruta | `origen`, `destino`, `distancia_km`, `estado` |
| Viaje | `bus`, `conductor`, `ruta`, `fecha_hora_inicio`, `fecha_hora_fin`, `estado` |

## Endpoints

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
