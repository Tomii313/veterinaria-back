from rest_framework.pagination import PageNumberPagination

class DueniosPagination(PageNumberPagination):
    page_size = 10