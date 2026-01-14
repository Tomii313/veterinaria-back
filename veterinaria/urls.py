from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', TokenObtainPairView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name="refresh"),
    path('logout/', TokenBlacklistView.as_view(), name="logout"),
    # APIs / apps
    path('', include('animales.routers')),
    path('', include('duenios.routers')),
    path('', include('veterinarios.routers')),
    path('', include('turnos.routers')),
  
]