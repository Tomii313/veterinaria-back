from rest_framework.pagination import PageNumberPagination

class AnimalPagination(PageNumberPagination):
    page_size = 10