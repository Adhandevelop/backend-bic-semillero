from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Bus, Conductor, Ruta, Viaje
from .serializers import (
    BusSerializer,
    ConductorSerializer,
    RutaSerializer,
    ViajeSerializer,
)


class BusViewSet(viewsets.ModelViewSet):
    queryset = Bus.objects.all()
    serializer_class = BusSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False, methods=["get"])
    def activos(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(estado=Bus.ESTADO_ACTIVO),
            many=True,
        )
        return Response(serializer.data)


class ConductorViewSet(viewsets.ModelViewSet):
    queryset = Conductor.objects.all()
    serializer_class = ConductorSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False, methods=["get"])
    def activos(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(estado=Conductor.ESTADO_ACTIVO),
            many=True,
        )
        return Response(serializer.data)


class RutaViewSet(viewsets.ModelViewSet):
    queryset = Ruta.objects.all()
    serializer_class = RutaSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False, methods=["get"])
    def activas(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(estado=Ruta.ESTADO_ACTIVA),
            many=True,
        )
        return Response(serializer.data)


class ViajeViewSet(viewsets.ModelViewSet):
    queryset = Viaje.objects.select_related("bus", "conductor", "ruta")
    serializer_class = ViajeSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.query_params.get("estado")
        if estado:
            queryset = queryset.filter(estado=estado)
        return queryset

    @action(detail=False, methods=["get"])
    def programados(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(estado=Viaje.ESTADO_PROGRAMADO),
            many=True,
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="en-curso")
    def en_curso(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(estado=Viaje.ESTADO_EN_CURSO),
            many=True,
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def finalizados(self, request):
        serializer = self.get_serializer(
            self.get_queryset().filter(estado=Viaje.ESTADO_FINALIZADO),
            many=True,
        )
        return Response(serializer.data)

    @action(detail=True, methods=["patch"])
    def iniciar(self, request, pk=None):
        viaje = self.get_object()
        viaje.estado = Viaje.ESTADO_EN_CURSO
        viaje.save(update_fields=["estado"])
        return Response(self.get_serializer(viaje).data)

    @action(detail=True, methods=["patch"])
    def finalizar(self, request, pk=None):
        viaje = self.get_object()
        fecha_hora_fin = request.data.get("fecha_hora_fin")

        viaje.estado = Viaje.ESTADO_FINALIZADO
        if fecha_hora_fin:
            serializer = self.get_serializer(
                viaje,
                data={"fecha_hora_fin": fecha_hora_fin, "estado": viaje.estado},
                partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        viaje.fecha_hora_fin = timezone.now()
        if viaje.fecha_hora_fin <= viaje.fecha_hora_inicio:
            return Response(
                {
                    "fecha_hora_fin": (
                        "La fecha y hora de fin debe ser mayor que la fecha "
                        "y hora de inicio."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        viaje.save(update_fields=["estado", "fecha_hora_fin"])
        return Response(self.get_serializer(viaje).data)

    @action(detail=True, methods=["patch"])
    def cancelar(self, request, pk=None):
        viaje = self.get_object()
        viaje.estado = Viaje.ESTADO_CANCELADO
        viaje.save(update_fields=["estado"])
        return Response(self.get_serializer(viaje).data)
