from django.shortcuts import render
from rest_framework import viewsets
from .models import Duenio
from animales.models import Animal
from turnos.models import Turno
from turnos.serializers import TurnoSerializer
from animales.serializers import AnimalSerializer
from .serializers import DuenioSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import DueniosPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import filters
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter
# Create your views here.


@extend_schema_view(
    list=extend_schema(summary="Listar dueños"),
    retrieve=extend_schema(summary="Detalle de dueño"),
    create=extend_schema(summary="Crear dueño"),
    update=extend_schema(summary="Actualizar dueño"),
    destroy=extend_schema(summary="Eliminar dueño"),
)
class DuenioViewSet(viewsets.ModelViewSet):
    queryset = Duenio.objects.all()
    serializer_class = DuenioSerializer
    pagination_class = DueniosPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'apellido', 'dni']
    def get_queryset(self):
        return Duenio.objects.all()

    @extend_schema(
        summary="Filtrar dueños por DNI",
        description="Se inserta el DNI del dueño y se va a mostrar la información de este si coincide con uno existente.",
        parameters=[
            OpenApiParameter(
                name="dni",
                description="DNI del dueño",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: DuenioSerializer(many=True)}
    )
    @action(detail=False, methods=['get'])
    def filtrar_dni(self, request):
        dni = request.query_params.get("dni")
        if not dni:
            return Response([], status=200)

        duenio = Duenio.objects.filter(dni=dni)
        serializer = self.get_serializer(duenio, many=True)
        return Response(serializer.data)


    @extend_schema(
        summary="Eliminar dueño",
        description="Eliminar un dueño.",
        parameters=[
            OpenApiParameter(
                name="pk",
                description="ID del dueño",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ],
    )
    @action(detail=True, methods=['POST'])
    def eliminar_duenio(self,request,pk=None):
        duenio = self.get_object()
        duenio.delete()
        return Response(status=204)

    