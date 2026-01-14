from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from datetime import datetime, timedelta
from .models import Turno
from veterinarios.models import Veterinario
from veterinarios.models import Horario
from veterinarios.serializers import VeterinarioSerializer
from .serializers import TurnoSerializer
from rest_framework.response import Response
from .pagination import TurnosPagination


# Create your views here.

class TurnoViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoSerializer
    pagination_class = TurnosPagination
    def get_queryset(self):
        queryset = Turno.objects.all()

        fecha = self.request.query_params.get("fecha")
        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset


    @action(detail=False, methods=['get'])
    def horarios_disponibles(self,request):
        veterinario_id = request.query_params.get("veterinario_id")
        fecha = request.query_params.get("fecha")
        
        #convertimos fecha

        fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

        #obtener horario del veterinario
        horario = Horario.objects.filter(veterinario_id=veterinario_id).first()

        #generar horario del veterinario cada 15m

        hora_actual = datetime.combine(fecha, horario.hora_inicio)
        hora_fin = datetime.combine(fecha, horario.hora_fin)

        
        horarios = []
        while hora_actual < hora_fin:
            horarios.append(hora_actual.time())
            hora_actual += timedelta(minutes=15)

        #horarios ocupados
        ocupados = Turno.objects.filter(
            veterinario_id=veterinario_id,
            fecha=fecha
        ).values_list("hora", flat=True)

        #sacar ocupados
        disponibles = [
            h.strftime("%H:%M")
            for h in horarios
            if h not in ocupados
        ]
        return Response(disponibles)

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
    def filtrar_turno_veterinario(self, request, pk=None):
        parametro = request.query_params.get('veterinario_id')
        if not parametro:
            return Response({"message": "Parametro no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        if parametro:
            veterinario = self.get_queryset().filter(veterinario_id=parametro)
            if veterinario.exists():
                serializer = self.serializer_class(veterinario, many=True)
                return Response(serializer.data)
            else:
                return Response({"message": "Veterinario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


    @action(methods=['POST'], detail=True)
    def cancelar_turno(self, request, pk=None):
        turno = self.get_object()
        if turno.estado == "Cancelado":
            return Response({"message": "Turno ya cancelado"}, status=status.HTTP_400_BAD_REQUEST)
        turno.estado = "Cancelado"
        turno.save()
        serializer = self.get_serializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @action(methods=['POST'], detail=True)
    def confirmar_turno(self, request, pk=None):
        turno = self.get_object()
        if turno.estado == "Confirmado":
            return Response({"message": "Turno ya confirmado"}, status=status.HTTP_400_BAD_REQUEST)
        turno.estado = "Confirmado"
        turno.save()
        serializer = self.get_serializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @action(methods=['GET'], detail=False)
    def veterinarios_disponibles(self, request):
        fecha = request.GET.get("fecha")
        if not fecha:
            return Response({"error": "Fecha requerida"}, status=400)

        dia_semana = datetime.strptime(fecha, "%Y-%m-%d").strftime("%A")

        traduccion = {
        "Monday": "Lunes",
        "Tuesday": "Martes",
        "Wednesday": "Miércoles",
        "Thursday": "Jueves",
        "Friday": "Viernes",
        "Saturday": "Sábado",
        "Sunday": "Domingo",
    }


        dia = traduccion[dia_semana]

        jornadas = Horario.objects.filter(dias__icontains=dia)
        veterinarios = Veterinario.objects.filter(
            id__in=jornadas.values_list("veterinario_id", flat=True)
        )

        serializer = VeterinarioSerializer(veterinarios, many=True)
        return Response(serializer.data)








