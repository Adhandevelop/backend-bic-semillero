from rest_framework import serializers

from .models import Bus, Conductor, Ruta, Viaje


class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = ["id", "placa", "capacidad", "modelo", "estado"]

    def validate_placa(self, value):
        return value.upper()

    def validate_capacidad(self, value):
        if value <= 0:
            raise serializers.ValidationError("La capacidad debe ser mayor que 0.")
        return value


class ConductorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conductor
        fields = ["id", "nombre", "licencia", "telefono", "estado"]

    def validate_licencia(self, value):
        return value.upper()


class RutaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ruta
        fields = ["id", "origen", "destino", "distancia_km", "estado"]


class ViajeSerializer(serializers.ModelSerializer):
    bus_detalle = serializers.SerializerMethodField(read_only=True)
    conductor_detalle = serializers.SerializerMethodField(read_only=True)
    ruta_detalle = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Viaje
        fields = [
            "id",
            "bus",
            "conductor",
            "ruta",
            "fecha_hora_inicio",
            "fecha_hora_fin",
            "estado",
            "bus_detalle",
            "conductor_detalle",
            "ruta_detalle",
        ]

    def get_bus_detalle(self, obj):
        return {
            "id": obj.bus_id,
            "placa": obj.bus.placa,
        }

    def get_conductor_detalle(self, obj):
        return {
            "id": obj.conductor_id,
            "nombre": obj.conductor.nombre,
        }

    def get_ruta_detalle(self, obj):
        return {
            "id": obj.ruta_id,
            "origen": obj.ruta.origen,
            "destino": obj.ruta.destino,
        }

    def validate(self, attrs):
        bus = attrs.get("bus", getattr(self.instance, "bus", None))
        conductor = attrs.get("conductor", getattr(self.instance, "conductor", None))
        ruta = attrs.get("ruta", getattr(self.instance, "ruta", None))
        fecha_hora_inicio = attrs.get(
            "fecha_hora_inicio",
            getattr(self.instance, "fecha_hora_inicio", None),
        )
        fecha_hora_fin = attrs.get(
            "fecha_hora_fin",
            getattr(self.instance, "fecha_hora_fin", None),
        )

        if bus is None:
            raise serializers.ValidationError({"bus": "Este campo es obligatorio."})
        if conductor is None:
            raise serializers.ValidationError(
                {"conductor": "Este campo es obligatorio."}
            )
        if ruta is None:
            raise serializers.ValidationError({"ruta": "Este campo es obligatorio."})

        if bus.estado != Bus.ESTADO_ACTIVO:
            raise serializers.ValidationError(
                {"bus": "No se permiten viajes con buses inactivos o en mantenimiento."}
            )
        if conductor.estado != Conductor.ESTADO_ACTIVO:
            raise serializers.ValidationError(
                {"conductor": "No se permiten viajes con conductores inactivos."}
            )
        if ruta.estado != Ruta.ESTADO_ACTIVA:
            raise serializers.ValidationError(
                {"ruta": "No se permiten viajes con rutas inactivas."}
            )
        if fecha_hora_fin and fecha_hora_inicio and fecha_hora_fin <= fecha_hora_inicio:
            raise serializers.ValidationError(
                {
                    "fecha_hora_fin": (
                        "La fecha y hora de fin debe ser mayor que la fecha "
                        "y hora de inicio."
                    )
                }
            )

        return attrs
