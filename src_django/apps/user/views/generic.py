from django.contrib.auth import get_user_model
from seedwork.pagination import ListPagination
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import GenericViewSet

from apps.user.serializers.generic import UserMinimalSerializer

User = get_user_model()


class UserViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    permission_classes = (IsAdminUser,)
    queryset = User.objects.all()
    serializer_class = UserMinimalSerializer
    pagination_class = ListPagination
