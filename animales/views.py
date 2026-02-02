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
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
from rest_framework.parsers import MultiPartParser, FormParser


# Create your views here.

@extend_schema_view(
    list=extend_schema(summary="Listar animales"),
    retrieve=extend_schema(summary="Detalle de animal"),
    create=extend_schema(summary="Crear animal"),
    update=extend_schema(summary="Actualizar animal"),
    destroy=extend_schema(summary="Eliminar animal"),
)
class AnimalViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = AnimalSerializer
    pagination_class = AnimalPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'especie', 'duenio__apellido', 'duenio__dni', 'duenio__nombre']

    def get_queryset(self):
        return Animal.objects.all()

    @extend_schema(
        summary="Filtrar animales por especie",
        description="Se inserta la especie del animal y se va a mostrar la información de los animales cuya especie coincida.",
        parameters=[
            OpenApiParameter(
                name="especie",
                description="Especie del animal",
                required=True,
                
            ),
        
        OpenApiParameter(
            name="duenio",
            description="Duenio del animal",
            required=True,
            type=OpenApiTypes.INT,
            
        ),
        ], responses={200: AnimalSerializer(many=True)}

    )

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


    @extend_schema(
        summary="Filtrar animales por dni del dueño",
        description="Se inserta el dni del dueño y se va a mostrar los animales que este tiene.",
        parameters=[
            OpenApiParameter(
                name="dni",
                description="Dni del dueño",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: AnimalSerializer(many=True)}
    )
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


    @extend_schema(
        summary="Seleccionar estados",
        description="Se va a mostrar los estados de los animales.",
    )
    @action(methods=['GET'], detail=False)
    def select_estado(self, request):
        return Response([{'value': k, 'label': v} for k,v in Animal.estados])


    @extend_schema(
        summary="Filtrar animales por estado",
        description="Se inserta el estado del animal y se va a mostrar la información de los animales cuyo estado coincida.",
        parameters=[
            OpenApiParameter(
                name="estado",
                description="Estado del animal",
                required=True,
                
            ),
        ], responses={200: AnimalSerializer(many=True)}
    )
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


    @extend_schema(
        summary="Contar animales internados",
        description="Se va a mostrar la cantidad de animales internados.",
    )
    @action(methods=['GET'], detail=False)
    def internados(self,request):
        internados = self.get_queryset().filter(estado="INTERNACION").count()
        return Response(internados)


    @extend_schema(
        summary="Mostrar animales internados",
        description="Se va a mostrar la información de los animales internados.",
    )
    @action(methods=['GET'], detail=False)
    def solo_internados(self, request):
        animales = self.get_queryset().filter(estado="INTERNACION")
        serializer = self.serializer_class(animales, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="Listar estudios"),
    retrieve=extend_schema(summary="Detalle de estudio"),
    create=extend_schema(summary="Crear estudio"),
    update=extend_schema(summary="Actualizar estudio"),
    destroy=extend_schema(summary="Eliminar estudio"),
)
class EstudiosViewSet(viewsets.ModelViewSet):
    serializer_class = EstudiosSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend]
    pagination_class = EstudiosPagination
    filterset_fields = {"tipo" : ["exact"], "animal__nombre" : ["exact", "icontains"], "fecha" : ["exact","gte", "lte"],}
    parser_classes = (MultiPartParser, FormParser)

   
    def get_queryset(self):
        return Estudios.objects.all()


    @extend_schema(
        summary="Mostrar tipos de estudios",
        description="Se va a mostrar la información de los tipos de estudios.",
    )
    @action(detail=False, methods=["get"])
    def tipos(self, request):
        return Response([
            {"value": k, "label": v}
            for k, v in Estudios.TIPO
        ])

    