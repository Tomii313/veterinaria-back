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
from animales.models import Animal
from datetime import date,datetime
from internacion.models import Internacion
from internacion.serializers import InternacionSerializer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter


# Create your views here.

@extend_schema_view(
        list=extend_schema(summary="Listar turnos"),
        retrieve=extend_schema(summary="Detalle de turno"),
        create=extend_schema(summary="Crear turno"),
        update=extend_schema(summary="Actualizar turno"),
        destroy=extend_schema(summary="Eliminar turno"),
    )

class TurnoViewSet(viewsets.ModelViewSet):
    serializer_class = TurnoSerializer
    pagination_class = TurnosPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    def get_queryset(self):
        queryset = Turno.objects.all()

        fecha = self.request.query_params.get("fecha")
        if fecha:
            queryset = queryset.filter(fecha=fecha)

        return queryset


    @extend_schema(
        summary="Horarios disponibles según el veterinario y la fecha",
        parameters=[
            OpenApiParameter(
                name="veterinario_id",
                description="ID del veterinario",
                required=True,
                type=OpenApiTypes.INT,
            ),
            OpenApiParameter(
                name="fecha",
                description="Fecha del turno",
                required=True,
                type=OpenApiTypes.DATE,
            ),
        ], responses={200: TurnoSerializer(many=True)},
    )
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

    @extend_schema(
        summary="Filtrar turnos por DNI",
        parameters=[
            OpenApiParameter(
                name="dni",
                description="DNI del dueño",
                
                type=OpenApiTypes.INT,
            ),
        ], responses={200: TurnoSerializer(many=True)},
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
        summary="Filtrar turnos por veterinario",
        parameters=[
            OpenApiParameter(
                name="veterinario_id",
                description="ID del veterinario",
                
                type=OpenApiTypes.INT,
            ),
        ], responses={200: TurnoSerializer(many=True)},
    )
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



    @extend_schema(
        summary="Cancelar Turno",
        parameters=[
            OpenApiParameter(
                name="pk",
                description="ID del turno",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: TurnoSerializer(many=True)},
    )
    @action(methods=['POST'], detail=True)
    def cancelar_turno(self, request, pk=None):
        turno = self.get_object()
        if turno.estado == "Cancelado":
            return Response({"message": "Turno ya cancelado"}, status=status.HTTP_400_BAD_REQUEST)
        turno.estado = "Cancelado"
        turno.save()
        serializer = self.get_serializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)



    @extend_schema(
        summary="Confirmar Turno",
        parameters=[
            OpenApiParameter(
                name="pk",
                description="ID del turno",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: TurnoSerializer(many=True)},
    )
    @action(methods=['POST'], detail=True)
    def confirmar_turno(self, request, pk=None):
        turno = self.get_object()
        if turno.estado == "Confirmado":
            return Response({"message": "Turno ya confirmado"}, status=status.HTTP_400_BAD_REQUEST)
        turno.estado = "Confirmado"
        turno.save()
        serializer = self.get_serializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @extend_schema(
        summary="Veterinarios disponibles",
        parameters=[
            OpenApiParameter(
                name="fecha",
                description="Fecha del turno",
                required=True,
                type=OpenApiTypes.DATE,
            ),
        ], responses={200: VeterinarioSerializer(many=True)}
    )
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


    @extend_schema(
        summary="Historial médico",
        parameters=[
            OpenApiParameter(
                name="pk",
                description="ID del animal",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: TurnoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=True)
    def historial_medico(self,request, pk=None):
        animales = Animal.objects.get(id=pk)
        
        if not animales:
            return Response({"message": "Animal no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        turnos = Turno.objects.filter(animal=animales)
        if not turnos:
            return Response({"message": "Turnos no encontrados"}, status=status.HTTP_404_NOT_FOUND)
        internaciones = Internacion.objects.filter(animal=animales)
        if not internaciones:
            return Response({"message": "Internaciones no encontradas"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TurnoSerializer(turnos, many=True)
        serializer2 = InternacionSerializer(internaciones, many=True)
        return Response({
    "turnos": serializer.data,
    "internaciones": serializer2.data
})


    @extend_schema(
        summary="Turno en curso",
        parameters=[
            OpenApiParameter(
                name="fecha",
                description="Fecha del turno",
                required=True,
                type=OpenApiTypes.DATE,
            ),
            OpenApiParameter(
                name="hora",
                description="Hora del turno",
                required=True,
                type=OpenApiTypes.TIME,
            ),
        ], responses={200: TurnoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=False)
    def turno_en_curso(self,request):
        fecha_actual = date.today()
        hora_actual = datetime.now().time()
        turno = Turno.objects.filter(fecha=fecha_actual, hora=hora_actual, estado="Confirmado")
        if not turno:
            return Response({"message": "no hay turnos en curso"}, status=status.HTTP_200_OK)
        serializer = TurnoSerializer(turno, many=True)
        return Response(serializer.data)
        

    @extend_schema(
        summary="Cancelar Turno",
        parameters=[
            OpenApiParameter(
                name="pk",
                description="ID del turno",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: TurnoSerializer(many=True)},
    )
    @action(methods=['POST'], detail=True)
    def cancelacion_de_turno(self,request,pk=None):
        fecha_actual = date.today()
        hora_actual = datetime.now().time()
        turno = self.get_object()
        if turno.estado == "Pendiente" and turno.fecha < fecha_actual and turno.hora < hora_actual:
            turno.estado = "Cancelado"
            turno.save()
            return Response({"message": "Turno cancelado"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Turno no cancelable"}, status=status.HTTP_400_BAD_REQUEST)
        




