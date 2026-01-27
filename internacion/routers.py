from rest_framework.routers import DefaultRouter
from .views import InternacionViewSet, JaulasViewSet, ObservacionesViewSet

router = DefaultRouter()
router.register(r'internaciones', InternacionViewSet, basename="internaciones")
router.register(r'jaulas', JaulasViewSet, basename="jaulas")
router.register(r'observaciones', ObservacionesViewSet, basename="observaciones")

urlpatterns = router.urls