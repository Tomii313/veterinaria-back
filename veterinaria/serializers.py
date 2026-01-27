from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        #llamamos al meetodo original para obtener los tokens
        data = super().validate(attrs)
        #agregamos la informacion del usuario
        data['rol'] = self.user.groups.first().name if self.user.groups.exists() else "Sin Rol"
        data['is_superuser'] = self.user.is_superuser
        #permisos
        data['permisos'] = list(self.user.get_all_permissions())
        return data