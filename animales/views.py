from animales.serializers import EstudiosSerializer
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Animal, Estudios
from .serializers import AnimalSerializer, EstudiosSerializer
from .pagination import AnimalPagination, EstudiosPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


# Create your views here.

class AnimalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = AnimalSerializer
    pagination_class = AnimalPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'especie', 'duenio__apellido', 'duenio__dni', 'duenio__nombre']

    def get_queryset(self):
        return Animal.objects.all()

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


    @action(methods=['GET'], detail=False)
    def select_estado(self, request):
        return Response([{'value': k, 'label': v} for k,v in Animal.estados])


    @action(methods=['GET'], detail=False)
    def filtrar_estado(self,request):
        parametro = request.query_params.get('estado')
        if not parametro:
            return Response({'message': 'Parametro no encontrado'}, status=status.HTTP_400_BAD_REQUEST)
        animales = self.get_queryset().filter(estado=parametro)
        if animales.exists():
            serializer = self.serializer_class(animales, many=True)
            return Response(serializer.data)
        else:
            return Response({'message': 'No se encontraron animales con ese estado'}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['GET'], detail=False)
    def internados(self,request):
        internados = self.get_queryset().filter(estado="INTERNACION").count()
        return Response(internados)


    @action(methods=['GET'], detail=False)
    def solo_internados(self, request):
        animales = self.get_queryset().filter(estado="INTERNACION")
        serializer = self.serializer_class(animales, many=True)
        return Response(serializer.data)


class EstudiosViewSet(viewsets.ModelViewSet):
    serializer_class = EstudiosSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    pagination_class = EstudiosPagination
    filterset_fields = {"tipo" : ["exact"], "animal__nombre" : ["exact", "icontains"], "fecha" : ["exact","gte", "lte"],}

   
    def get_queryset(self):
        return Estudios.objects.all()


    
    @action(detail=False, methods=["get"])
    def tipos(self, request):
        return Response([
            {"value": k, "label": v}
            for k, v in Estudios.TIPO
        ])

    