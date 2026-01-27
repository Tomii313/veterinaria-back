from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)
from .views import UserPermissionsView, MyTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', MyTokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('logout/', TokenBlacklistView.as_view(), name="logout"),
    # APIs / apps
    path('', include('animales.routers')),
    path('', include('duenios.routers')),
    path('', include('veterinarios.routers')),
    path('', include('turnos.routers')),
    path('', include('internacion.routers')),
    path('', include('inventario.routers')),
    path("permisos/", UserPermissionsView.as_view(), name="user-permissions"),
  

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)