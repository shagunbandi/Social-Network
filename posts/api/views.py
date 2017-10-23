from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter


from posts.models import Post
from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .serializers import PostDetailSerializer, PostListSerializer, PostCreateUpdateSerializer
from .permissions import IsOwnerOrReadOnly


# List View
class PostListAPIView(ListAPIView):
    serializer_class = PostListSerializer

    # django filter
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'content']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Post.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(user__username__icontaints=query)
            ).distinct()
        return queryset_list


# Detail View
class PostDetailAPIViewByPK(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


# Delete View
class PostDestroyAPIViewByPK(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer


class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'


# Update View
class PostUpdateAPIViewByPK(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class PostUpdateAPIView(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]

    # def perform_update(self, serializer):
    #     serializer.save(user=self.request.user)


# Create View
class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

