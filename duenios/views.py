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
# Create your views here.

class DuenioViewSet(viewsets.ModelViewSet):
    queryset = Duenio.objects.all()
    serializer_class = DuenioSerializer
    pagination_class = DueniosPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre', 'apellido', 'dni']
    def get_queryset(self):
        return Duenio.objects.all()

    @action(detail=False, methods=['get'])
    def filtrar_dni(self, request):
        dni = request.query_params.get("dni")
        if not dni:
            return Response([], status=200)

        duenio = Duenio.objects.filter(dni=dni)
        serializer = self.get_serializer(duenio, many=True)
        return Response(serializer.data)


  
    @action(detail=True, methods=['POST'])
    def eliminar_duenio(self,request,pk=None):
        duenio = self.get_object()
        duenio.delete()
        return Response(status=204)

    