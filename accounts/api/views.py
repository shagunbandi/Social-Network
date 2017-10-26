from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from django.db.models import Q
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin
from django.contrib.auth import get_user_model

# From Comments App
from comments.models import Comment
from .serializers import UserCreateSerializer


User = get_user_model()


# Create View
class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
