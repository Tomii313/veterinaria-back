from rest_framework import serializers
from .models import Veterinario, Horario


class VeterinarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veterinario
        fields = '__all__'

 

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'