from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet, EstudiosViewSet

router = DefaultRouter()
router.register(r'animales', AnimalViewSet, basename="animales")
router.register(r'estudios', EstudiosViewSet, basename="estudios")


urlpatterns = router.urls