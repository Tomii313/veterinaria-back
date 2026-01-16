from rest_framework.routers import DefaultRouter
from .views import AnimalViewSet

router = DefaultRouter()
router.register(r'animales', AnimalViewSet, basename="animales")


urlpatterns = router.urls