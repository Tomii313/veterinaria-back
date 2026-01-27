from django.shortcuts import render
from rest_framework import viewsets
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .pagination import InventarioPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

# Create your views here.


class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    pagination_class = InventarioPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    def get_queryset(self):
        return Producto.objects.all()

    @action(methods=['GET'], detail=False)
    def filtrar_producto(self, request):
        categoria_id = request.query_params.get('categoria')
        if categoria_id:
            filtrar = self.get_queryset().filter(categoria__id=categoria_id)
           
        else:
            filtrar = self.get_queryset()
        serializer = self.get_serializer(filtrar, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def buscar_producto(self, request):
        nombre = request.query_params.get('nombre')
        if nombre:
            buscar = self.get_queryset().filter(nombre__icontains=nombre)
        else:
            buscar = self.get_queryset()
        serializer = self.get_serializer(buscar, many=True)
        return Response(serializer.data)


    @action(methods=['GET'], detail=False)
    def ordenar_productos(self, request):
        productos = self.get_queryset().order_by("-stock")
        if not productos:
            return Response([])
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)


    @action(methods=['GET'], detail=False)
    def ordenar_productos_desc(self, request):
        productos = self.get_queryset().order_by("stock")
        if not productos:
            return Response([])
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def stock_critico(self,request):
        stock_critico = self.get_queryset().filter(stock__lte=50).count()
        return Response(stock_critico)

    

class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    def get_queryset(self):
        return Categoria.objects.all()

