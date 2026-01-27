from rest_framework import serializers
from .models import Internacion, Jaulas, Observaciones
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class ObservacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observaciones
        fields = '__all__'

class InternacionSerializer(serializers.ModelSerializer):
    nombre_animal = serializers.CharField(source='animal.nombre', read_only=True)
    raza_animal = serializers.CharField(source='animal.raza', read_only=True)
    especie_animal = serializers.CharField(source='animal.especie', read_only=True)
    historial_observaciones = ObservacionesSerializer(many=True, read_only=True)
    class Meta:

        model = Internacion
        fields = '__all__'

   


class JaulasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jaulas
        fields = '__all__'


