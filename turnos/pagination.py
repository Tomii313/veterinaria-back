from rest_framework.pagination import PageNumberPagination


class TurnosPagination(PageNumberPagination):
    page_size = 10