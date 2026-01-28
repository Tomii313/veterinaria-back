from rest_framework import serializers
from animales.models import Animal
from .models import Duenio
from turnos.models import Turno
from turnos.serializers import TurnoSerializer

class DuenioSerializer(serializers.ModelSerializer):
    mascotas = serializers.SerializerMethodField()
    ultimoturno = serializers.SerializerMethodField()
    class Meta:
        model = Duenio
        fields = (
            "id",
            "nombre",
            "apellido",
            "dni",
            "telefono",
            "email",
            "mascotas",
            "ultimoturno",
        )

    def get_mascotas(self, duenio):
        from animales.serializers import AnimalDuenioSerializer
        animales = duenio.mascotas.all()
        return AnimalDuenioSerializer(animales, many=True).data

    def get_ultimoturno(self,duenio):
        turnos = Turno.objects.filter(animal__duenio=duenio).order_by('-fecha').first()
        return turnos.fecha if turnos else None

    def validate_dni(self, dni):
        if Duenio.objects.filter(dni=dni).exists():
            raise serializers.ValidationError("El DNI ya existe")
        return dni


