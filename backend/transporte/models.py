from django.core.validators import MinValueValidator
from django.db import models


class Bus(models.Model):
    ESTADO_ACTIVO = "activo"
    ESTADO_INACTIVO = "inactivo"
    ESTADO_MANTENIMIENTO = "mantenimiento"

    ESTADO_CHOICES = [
        (ESTADO_ACTIVO, "Activo"),
        (ESTADO_INACTIVO, "Inactivo"),
        (ESTADO_MANTENIMIENTO, "Mantenimiento"),
    ]

    placa = models.CharField(max_length=10, unique=True)
    capacidad = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    modelo = models.CharField(max_length=50, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_ACTIVO,
    )

    class Meta:
        ordering = ["placa"]
        verbose_name = "bus"
        verbose_name_plural = "buses"

    def save(self, *args, **kwargs):
        if self.placa:
            self.placa = self.placa.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.placa} ({self.estado})"


class Conductor(models.Model):
    ESTADO_ACTIVO = "activo"
    ESTADO_INACTIVO = "inactivo"

    ESTADO_CHOICES = [
        (ESTADO_ACTIVO, "Activo"),
        (ESTADO_INACTIVO, "Inactivo"),
    ]

    nombre = models.CharField(max_length=100)
    licencia = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=20, blank=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_ACTIVO,
    )

    class Meta:
        ordering = ["nombre"]
        verbose_name = "conductor"
        verbose_name_plural = "conductores"

    def save(self, *args, **kwargs):
        if self.licencia:
            self.licencia = self.licencia.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} - {self.licencia}"


class Ruta(models.Model):
    ESTADO_ACTIVA = "activa"
    ESTADO_INACTIVA = "inactiva"

    ESTADO_CHOICES = [
        (ESTADO_ACTIVA, "Activa"),
        (ESTADO_INACTIVA, "Inactiva"),
    ]

    origen = models.CharField(max_length=100)
    destino = models.CharField(max_length=100)
    distancia_km = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_ACTIVA,
    )

    class Meta:
        ordering = ["origen", "destino"]
        verbose_name = "ruta"
        verbose_name_plural = "rutas"

    def __str__(self):
        return f"{self.origen} - {self.destino}"


class Viaje(models.Model):
    ESTADO_PROGRAMADO = "programado"
    ESTADO_EN_CURSO = "en_curso"
    ESTADO_FINALIZADO = "finalizado"
    ESTADO_CANCELADO = "cancelado"

    ESTADO_CHOICES = [
        (ESTADO_PROGRAMADO, "Programado"),
        (ESTADO_EN_CURSO, "En curso"),
        (ESTADO_FINALIZADO, "Finalizado"),
        (ESTADO_CANCELADO, "Cancelado"),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.PROTECT, related_name="viajes")
    conductor = models.ForeignKey(
        Conductor,
        on_delete=models.PROTECT,
        related_name="viajes",
    )
    ruta = models.ForeignKey(Ruta, on_delete=models.PROTECT, related_name="viajes")
    fecha_hora_inicio = models.DateTimeField()
    fecha_hora_fin = models.DateTimeField(blank=True, null=True)
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_CHOICES,
        default=ESTADO_PROGRAMADO,
    )

    class Meta:
        ordering = ["-fecha_hora_inicio"]
        verbose_name = "viaje"
        verbose_name_plural = "viajes"

    def __str__(self):
        return f"{self.ruta} - {self.fecha_hora_inicio:%Y-%m-%d %H:%M}"
