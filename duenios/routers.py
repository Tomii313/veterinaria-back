from rest_framework.routers import DefaultRouter
from .views import DuenioViewSet

router = DefaultRouter()
router.register(r'duenios', DuenioViewSet, basename="duenios")

urlpatterns = router.urls