from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter

# From Comments App
from comments.models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer

# From Posts App
from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly


# List View
class CommentListAPIView(ListAPIView):
    serializer_class = CommentSerializer

    # django filter
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content']
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        queryset_list = Comment.objects.filter_if_parent()
        query = self.request.GET.get('q')
        if query:
            queryset_list = queryset_list.filter(
                Q(content__icontains=query) |
                Q(user__username__icontaints=query)
            ).distinct()
        return queryset_list


class CommentDetailAPIView(RetrieveAPIView):
    queryset = Comment.objects.filter_if_parent()
    serializer_class = CommentDetailSerializer
    lookup_field = 'pk'


# # Delete View
# class PostDestroyAPIViewByPK(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#
#
# class PostDestroyAPIViewBySlug(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'slug'
#
#
# # Update View
# class PostUpdateAPIViewByPK(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
#
#     def perform_update(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class PostUpdateAPIViewBySlug(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]
#
#     # def perform_update(self, serializer):
#     #     serializer.save(user=self.request.user)
#
#
# # Create View
# class PostCreateAPIView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     permission_classes = [IsAuthenticated]
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
