from rest_framework import serializers
from .models import Animal, Estudios


class AnimalSerializer(serializers.ModelSerializer):
    """ estado = serializers.SerializerMethodField() """
    class Meta:
        model = Animal
        fields = '__all__'

    """  def get_estado(self,obj):
        estado = Estado.objects.filter(animal=obj).first()
        return estado.estado if estado else None """

    def to_representation(self,instance):
        data = super().to_representation(instance)
        data["duenio_id"] = instance.duenio.id
        data['duenio_nombre'] = instance.duenio.nombre
        data['duenio_apellido'] = instance.duenio.apellido
        data['duenio_dni'] = instance.duenio.dni
        data['duenio_telefono'] = instance.duenio.telefono
        return data



class AnimalDuenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ("nombre",)

class EstudiosSerializer(serializers.ModelSerializer):
    animal_nombre = serializers.CharField(source="animal.nombre", read_only=True)
    animal_dueño = serializers.CharField(source="animal.duenio.nombre", read_only=True)
    duenio_apellido = serializers.CharField(source="animal.duenio.apellido", read_only=True)
    class Meta:
        model = Estudios
        fields = '__all__'

  