from rest_framework import serializers
from .models import Animal


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

  