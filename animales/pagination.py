from rest_framework.pagination import PageNumberPagination

class AnimalPagination(PageNumberPagination):
    page_size = 10

class EstudiosPagination(PageNumberPagination):
    page_size = 15
