from rest_framework.pagination import PageNumberPagination

class InventarioPagination(PageNumberPagination):
    page_size = 10