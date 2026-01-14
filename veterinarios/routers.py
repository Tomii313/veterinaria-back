from rest_framework.routers import DefaultRouter
from .views import VeterinarioViewSet, HorarioViewSet


router = DefaultRouter()
router.register(r'veterinarios', VeterinarioViewSet, basename="veterinarios")
router.register(r'horarios', HorarioViewSet, basename="horarios")

urlpatterns = router.urls