from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Animal, Estado
from .serializers import AnimalSerializer, EstadoSerializer
from .pagination import AnimalPagination



# Create your views here.

class AnimalViewSet(viewsets.ModelViewSet):
    serializer_class = AnimalSerializer
    pagination_class = AnimalPagination
    def get_queryset(self):
        return Animal.objects.all()

    @action(methods=['get'], detail=False)
    def buscar(self,request,pk=None):
        nombre = request.query_params.get('nombre')
        if nombre:
           mascota = self.get_queryset().filter(nombre=nombre)
           if mascota.exists():
               serializer_class = AnimalSerializer(mascota, many=True)
               return Response(serializer_class.data)
           else:
               return Response({"message": "Mascota no encontrada"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], detail=False)
    def especies(self,request, pk=None):
        parametro = request.query_params.get('especie')
        duenio = request.query_params.get('duenio')
        if parametro:
            animales = self.get_queryset().filter(especie=parametro)
            serializer = self.serializer_class(animales, many=True)
            return Response(serializer.data)
        else:
            animales = self.get_queryset().filter(duenio__apellido=duenio)
            serializer = self.serializer_class(animales, many=True)
            return Response(serializer.data)
        return Response({"message": "Parametro no encontrado"}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['GET'], detail=False)
    def filtrar_dni(self,request,pk=None):
        parametro = request.query_params.get('dni')
        if not parametro:
            return Response({"message": "Parametro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        if parametro:
            duenio = self.get_queryset().filter(duenio__dni=parametro)
            if duenio.exists():
                serializer = self.serializer_class(duenio, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Duenio no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "Parametro no encontrado"}, status=status.HTTP_404_NOT_FOUND)

class EstadoViewSet(viewsets.ModelViewSet):
    serializer_class = EstadoSerializer
    def get_queryset(self):
        return Estado.objects.all()

    @action(methods=['GET'], detail=False)
    def filtrar_estado(self,request,pk=None):
        parametro = request.query_params.get('estado')
        if parametro:
            estados = self.get_queryset().filter(estado=parametro)
            serializer = self.serializer_class(estados, many=True)
            return Response(serializer.data)
        return Response({"message": "Parametro no encontrado"}, status=status.HTTP_404_NOT_FOUND)