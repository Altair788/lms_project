from rest_framework.pagination import PageNumberPagination


class LmsPaginator(PageNumberPagination):
    page_size = 1

