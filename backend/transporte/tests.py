from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Bus, Conductor, Ruta, Viaje


class TransporteAPITests(APITestCase):
    def setUp(self):
        self.bus = Bus.objects.create(placa="abc123", capacidad=40, modelo="2024")
        self.conductor = Conductor.objects.create(
            nombre="Juan Perez",
            licencia="lic123",
            telefono="3001234567",
        )
        self.ruta = Ruta.objects.create(
            origen="Bogota",
            destino="Medellin",
            distancia_km=415,
        )

    def test_crear_bus_guarda_placa_en_mayuscula(self):
        response = self.client.post(
            reverse("bus-list"),
            {"placa": "xyz789", "capacidad": 25, "modelo": "2023"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["placa"], "XYZ789")

    def test_no_permite_bus_con_capacidad_cero(self):
        response = self.client.post(
            reverse("bus-list"),
            {"placa": "zzz999", "capacidad": 0},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_crear_viaje_con_detalles(self):
        response = self.client.post(
            reverse("viaje-list"),
            {
                "bus": self.bus.id,
                "conductor": self.conductor.id,
                "ruta": self.ruta.id,
                "fecha_hora_inicio": timezone.now() + timedelta(hours=1),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["bus_detalle"]["placa"], "ABC123")
        self.assertEqual(response.data["conductor_detalle"]["nombre"], "Juan Perez")
        self.assertEqual(response.data["ruta_detalle"]["origen"], "Bogota")

    def test_no_permite_viaje_con_bus_inactivo(self):
        self.bus.estado = Bus.ESTADO_INACTIVO
        self.bus.save()

        response = self.client.post(
            reverse("viaje-list"),
            {
                "bus": self.bus.id,
                "conductor": self.conductor.id,
                "ruta": self.ruta.id,
                "fecha_hora_inicio": timezone.now() + timedelta(hours=1),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_endpoint_buses_activos(self):
        Bus.objects.create(
            placa="ina001",
            capacidad=20,
            estado=Bus.ESTADO_INACTIVO,
        )

        response = self.client.get(reverse("bus-activos"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["estado"], Bus.ESTADO_ACTIVO)

    def test_accion_iniciar_viaje(self):
        viaje = Viaje.objects.create(
            bus=self.bus,
            conductor=self.conductor,
            ruta=self.ruta,
            fecha_hora_inicio=timezone.now() + timedelta(hours=1),
        )

        response = self.client.patch(reverse("viaje-iniciar", args=[viaje.id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["estado"], Viaje.ESTADO_EN_CURSO)

    def test_fecha_fin_debe_ser_mayor_a_inicio(self):
        inicio = timezone.now() + timedelta(hours=2)
        response = self.client.post(
            reverse("viaje-list"),
            {
                "bus": self.bus.id,
                "conductor": self.conductor.id,
                "ruta": self.ruta.id,
                "fecha_hora_inicio": inicio,
                "fecha_hora_fin": inicio - timedelta(minutes=5),
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
