from django.shortcuts import render
from .serializers import VeterinarioSerializer, HorarioSerializer
from rest_framework import viewsets
from .models import Veterinario, Horario
from rest_framework.response import Response
from rest_framework.decorators import action
from .pagination import VeterinarioPagination
from rest_framework import status
from turnos.models import Turno
from datetime import date, datetime
from django.db.models import Q
from turnos.serializers import TurnoSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
# Create your views here.


class VeterinarioViewSet(viewsets.ModelViewSet):
    serializer_class = VeterinarioSerializer
    pagination_class = VeterinarioPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    def get_queryset(self):
        return Veterinario.objects.all()
   

    @action(detail=False, methods=['GET'])
    def buscar_por_nombre(self,request):
        nombre = request.query_params.get('nombre')
        if not nombre:
            return Response({'mensaje':'Debe ingresar un nombre'},status=400)
        veterinario = Veterinario.objects.filter(nombre__icontains=nombre)
        serializer = self.serializer_class(veterinario,many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'])
    def turnos_fecha(self, request):
        fecha_actual = date.today()
        turnos = Turno.objects.filter(fecha=fecha_actual).count()
        return Response(turnos)
    

    @action(detail=False, methods=['GET'])
    def citas_proximas(self, request):
        fecha_actual = date.today()
        hora_actual = datetime.now().time()

        turnos = Turno.objects.filter(Q(fecha__gt=fecha_actual) | Q(fecha=fecha_actual, hora__gte=hora_actual)).order_by('fecha', 'hora')[:2]
        serializer = TurnoSerializer(turnos, many=True)
        return Response(serializer.data)


class HorarioViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioSerializer
    def get_queryset(self):
        queryset = Horario.objects.all()
        veterinario_id = self.request.query_params.get('veterinario')

        if veterinario_id:
            queryset = queryset.filter(veterinario_id=veterinario_id)

        return queryset




