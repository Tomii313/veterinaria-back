from django.shortcuts import render
from .serializers import VeterinarioSerializer, HorarioSerializer
from rest_framework import viewsets
from .models import Veterinario, Horario
from rest_framework.response import Response
from rest_framework.decorators import action
from .pagination import VeterinarioPagination
# Create your views here.


class VeterinarioViewSet(viewsets.ModelViewSet):
    serializer_class = VeterinarioSerializer
    pagination_class = VeterinarioPagination
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

    


class HorarioViewSet(viewsets.ModelViewSet):
    serializer_class = HorarioSerializer
    def get_queryset(self):
        queryset = Horario.objects.all()
        veterinario_id = self.request.query_params.get('veterinario')

        if veterinario_id:
            queryset = queryset.filter(veterinario_id=veterinario_id)

        return queryset




