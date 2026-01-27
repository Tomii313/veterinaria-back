from rest_framework.pagination import PageNumberPagination

class InternacionPagination(PageNumberPagination):
    page_size = 10
