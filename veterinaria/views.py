from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer

class UserPermissionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        perms = request.user.get_all_permissions()
        return Response(list(perms))


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer