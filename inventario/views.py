from django.shortcuts import render
from rest_framework import viewsets
from .models import Producto, Categoria
from .serializers import ProductoSerializer, CategoriaSerializer
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.decorators import action
from .pagination import InventarioPagination
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from drf_spectacular.utils import extend_schema_view, extend_schema
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter

# Create your views here.

@extend_schema_view(
    list=extend_schema(summary="Listar productos"),
    retrieve=extend_schema(summary="Detalle de producto"),
    create=extend_schema(summary="Crear producto"),
    update=extend_schema(summary="Actualizar producto"),
    destroy=extend_schema(summary="Eliminar producto"),
)
class ProductoViewSet(viewsets.ModelViewSet):
    serializer_class = ProductoSerializer
    pagination_class = InventarioPagination
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    def get_queryset(self):
        return Producto.objects.all()


    @extend_schema(
        summary="Filtrar producto por categoría",
        description="Filtrar producto por categoría",
        parameters=[
            OpenApiParameter(
                name="categoria",
                description="ID de la categoría",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: ProductoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=False)
    def filtrar_producto(self, request):
        categoria_id = request.query_params.get('categoria')
        if categoria_id:
            filtrar = self.get_queryset().filter(categoria__id=categoria_id)
           
        else:
            filtrar = self.get_queryset()
        serializer = self.get_serializer(filtrar, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Buscar producto por nombre",
        description="Buscar producto por nombre",
        parameters=[
            OpenApiParameter(
                name="nombre",
                description="Nombre del producto",
                required=True,
                type=OpenApiTypes.STR,
            ),
        ], responses={200: ProductoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=False)
    def buscar_producto(self, request):
        nombre = request.query_params.get('nombre')
        if nombre:
            buscar = self.get_queryset().filter(nombre__icontains=nombre)
        else:
            buscar = self.get_queryset()
        serializer = self.get_serializer(buscar, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Ordenar productos por stock",
        description="Ordenar productos por stock",
        parameters=[
            OpenApiParameter(
                name="stock",
                description="Stock del producto",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: ProductoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=False)
    def ordenar_productos(self, request):
        productos = self.get_queryset().order_by("-stock")
        if not productos:
            return Response([])
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)


    @extend_schema(
        summary="Ordenar productos por stock",
        description="Ordenar productos por stock",
        parameters=[
            OpenApiParameter(
                name="stock",
                description="Stock del producto",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: ProductoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=False)
    def ordenar_productos_desc(self, request):
        productos = self.get_queryset().order_by("stock")
        if not productos:
            return Response([])
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Stock crítico",
        description="Se encarga de mostrar aquellos productos que tengan menos de 50 unidades.",
        parameters=[
            OpenApiParameter(
                name="stock",
                description="Stock del producto",
                required=True,
                type=OpenApiTypes.INT,
            ),
        ], responses={200: ProductoSerializer(many=True)}
    )
    @action(methods=['GET'], detail=False)
    def stock_critico(self,request):
        stock_critico = self.get_queryset().filter(stock__lte=50).count()
        return Response(stock_critico)

    
@extend_schema_view(
    list=extend_schema(summary="Listar categorias"),
    retrieve=extend_schema(summary="Detalle de categoria"),
    create=extend_schema(summary="Crear categoria"),
    update=extend_schema(summary="Actualizar categoria"),
    destroy=extend_schema(summary="Eliminar categoria"),
)
class CategoriaViewSet(viewsets.ModelViewSet):
    serializer_class = CategoriaSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    filter_backends = [filters.SearchFilter]
    search_fields = ['nombre']
    def get_queryset(self):
        return Categoria.objects.all()

