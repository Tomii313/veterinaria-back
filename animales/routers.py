from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, EstadoViewSet

router = DefaultRouter()
router.register(r'animales', AnimalViewSet, basename="animales")
router.register(r'estados', EstadoViewSet, basename="estados")

urlpatterns = router.urls