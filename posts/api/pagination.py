from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination


# TODO set correct values
class PostLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2
    max_limit = 10


class PostPageNumberPagination(PageNumberPagination):
    page_size = 2