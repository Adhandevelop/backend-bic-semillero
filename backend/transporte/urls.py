from rest_framework.routers import DefaultRouter

from .views import BusViewSet, ConductorViewSet, RutaViewSet, ViajeViewSet


router = DefaultRouter()
router.register("buses", BusViewSet, basename="bus")
router.register("conductores", ConductorViewSet, basename="conductor")
router.register("rutas", RutaViewSet, basename="ruta")
router.register("viajes", ViajeViewSet, basename="viaje")

urlpatterns = router.urls
