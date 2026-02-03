from rest_framework import serializers
from .models import Animal, Estudios
from duenios.serializers import DuenioSerializer
from duenios.models import Duenio
import cloudinary.uploader

class AnimalSerializer(serializers.ModelSerializer):
    duenio_id = serializers.PrimaryKeyRelatedField(
        queryset=Duenio.objects.all(),
        source="duenio",
        required=False,
        allow_null=True
    )

    duenio_nombre = serializers.CharField(source="duenio.nombre", read_only=True)
    duenio_apellido = serializers.CharField(source="duenio.apellido", read_only=True)
    duenio_dni = serializers.IntegerField(source="duenio.dni", read_only=True)
    duenio_telefono = serializers.CharField(source="duenio.telefono", read_only=True)

    class Meta:
        model = Animal
        fields = "__all__"



class AnimalDuenioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ("nombre",)

class EstudiosSerializer(serializers.ModelSerializer):
    animal_nombre = serializers.CharField(source="animal.nombre", read_only=True)
    animal_dueño = serializers.CharField(source="animal.duenio.nombre", read_only=True)
    duenio_apellido = serializers.CharField(source="animal.duenio.apellido", read_only=True)
<<<<<<< HEAD
    archivo = serializers.FileField(required=False, allow_null=True)
=======
    archivo = serializers.FileField(write_only=True, required=False)
>>>>>>> 0b8380f11761bb307685700c8f19b65ad3ea96fa
    class Meta:
        model = Estudios
        fields = '__all__'

    def create(self, validated_data):
        archivo = validated_data.pop("archivo", None)
        estudio = Estudios.objects.create(**validated_data)

        if archivo:
            result = cloudinary.uploader.upload(
                archivo,
                resource_type="raw",    # PDFs son raw
                access_mode="public"    # 🔥 público
            )
            estudio.archivo = result["secure_url"]
            estudio.save()

        return estudio

   