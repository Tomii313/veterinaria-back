from django.shortcuts import render
from .models import Internacion, Jaulas, Observaciones
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework import status
from rest_framework.response import Response
from .serializers import InternacionSerializer, JaulasSerializer, ObservacionesSerializer
from datetime import date
from .pagination import InternacionPagination
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


# Create your views here.

class InternacionViewSet(viewsets.ModelViewSet):
    serializer_class = InternacionSerializer
    pagination_class = InternacionPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    def get_queryset(self):
        return Internacion.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            animal = serializer.validated_data['animal']
            jaula = serializer.validated_data['jaula']

            internacion_activa = Internacion.objects.filter(
                animal=animal,
                fecha_salida__isnull=True
            ).exists()

            if internacion_activa:
                return Response(
                    {'error': 'Este animal ya tiene una internación activa'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if not jaula.disponible:
                return Response(
                    {'error': 'La jaula no está disponible'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            jaula.disponible = False
            jaula.save()

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['POST'])
    def dar_alta(self,request,pk=None):
       internado = self.get_queryset().filter(pk=pk).first()
       if not internado:
           return Response(
               {'error': 'Internacion no encontrada'},
               status=status.HTTP_404_NOT_FOUND
           )
       if internado.fecha_salida is not None:
           return Response(
               {'error': 'El internado ya ha sido dado de alta.'},
               status=status.HTTP_400_BAD_REQUEST
           )
       internado.fecha_salida = date.today()
       internado.jaula.disponible = True
       internado.jaula.save()
       internado.save()
       return Response(
    {"message": "Alta realizada correctamente"},
    status=status.HTTP_200_OK
)

    @action(detail=True, methods=["GET"])
    def imprimir(self, request, pk=None):
        internacion = self.get_object()

        return render(
            request,
            "pdf/internacion.html",
            {
                "internacion": internacion
            }
        )
    

    @action(detail=False, methods=['GET'])
    def internaciones_activas(self,request):
        internaciones = Internacion.objects.filter(fecha_salida__isnull=True).count()
        return Response(internaciones)
       

class JaulasViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = JaulasSerializer
    def get_queryset(self):
        return Jaulas.objects.all()

    @action(detail=False, methods=['GET'])
    def jaulas_disponibles(self, request):
        jaulas_disponibles = Jaulas.objects.filter(disponible=True).count()
        return Response(jaulas_disponibles)

    @action(detail=False,methods=['GET'])
    def jaulas_ocupadas(self,request):
        jaulas_ocupadas = Jaulas.objects.filter(disponible=False).count()
        return Response(jaulas_ocupadas)

    @action(detail=False,methods=['GET'])
    def total_jaulas(self,request):
        total_jaulas = Jaulas.objects.count()
        return Response(total_jaulas)
 


class ObservacionesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    serializer_class = ObservacionesSerializer
    def get_queryset(self):
        return Observaciones.objects.all()