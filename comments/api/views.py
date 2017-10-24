from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter

# From Comments App
from comments.models import Comment
from .serializers import CommentSerializer, CommentDetailSerializer, create_comment_serializer

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


# Create View
class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get('type')
        slug = self.request.GET.get('slug')
        parent_id = self.request.GET.get('parent_id', None)

        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )


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