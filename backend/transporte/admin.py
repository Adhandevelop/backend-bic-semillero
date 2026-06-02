from django.contrib import admin

from .models import Bus, Conductor, Ruta, Viaje


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("placa", "capacidad", "modelo", "estado")
    list_filter = ("estado",)
    search_fields = ("placa", "modelo")


@admin.register(Conductor)
class ConductorAdmin(admin.ModelAdmin):
    list_display = ("nombre", "licencia", "telefono", "estado")
    list_filter = ("estado",)
    search_fields = ("nombre", "licencia")


@admin.register(Ruta)
class RutaAdmin(admin.ModelAdmin):
    list_display = ("origen", "destino", "distancia_km", "estado")
    list_filter = ("estado",)
    search_fields = ("origen", "destino")


@admin.register(Viaje)
class ViajeAdmin(admin.ModelAdmin):
    list_display = (
        "bus",
        "conductor",
        "ruta",
        "fecha_hora_inicio",
        "fecha_hora_fin",
        "estado",
    )
    list_filter = ("estado", "fecha_hora_inicio")
    search_fields = ("bus__placa", "conductor__nombre", "ruta__origen", "ruta__destino")
