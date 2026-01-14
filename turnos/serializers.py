from rest_framework import serializers
from .models import Turno


class TurnoSerializer(serializers.ModelSerializer):
    nombre_animal = serializers.CharField(source="animal.nombre", read_only=True)
    raza_animal = serializers.CharField(source="animal.raza", read_only=True)
    edad_animal = serializers.CharField(source="animal.edad", read_only=True)
    duenio_nombre = serializers.CharField(source="animal.duenio.nombre", read_only=True)
    duenio_apellido = serializers.CharField(source="animal.duenio.apellido", read_only=True)
    veterinario_nombre = serializers.CharField(source="veterinario.nombre", read_only=True)
    veterinario_apellido = serializers.CharField(source="veterinario.apellido", read_only=True)
  
    class Meta:
        model = Turno
        fields = '__all__'
    
    
       
        

    def validate(self, data):
        veterinario = data.get("veterinario")
        fecha = data.get("fecha")
        hora = data.get("hora")
        
        if Turno.objects.filter(veterinario=veterinario,fecha=fecha,hora=hora).exists():
            raise serializers.ValidationError("Ya existe un turno para este veterinario en esta fecha y hora.")
        return data
