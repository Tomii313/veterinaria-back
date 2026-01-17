from rest_framework import serializers
from .models import Internacion


class InternacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Internacion
        fields = '__all__'