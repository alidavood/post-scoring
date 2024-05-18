from django.contrib.auth.models import AnonymousUser
from django.db.models import Avg, IntegerField, Subquery, OuterRef, Count
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from seedwork.pagination import ListPagination
from seedwork.utils import CustomThrottle
from ..serializers.generic import *
from ..services.post_score import PostService


class GenericPostViewSet(
    ListModelMixin,
    RetrieveModelMixin,
    GenericViewSet,
):
    """
    A viewset for handling generic post-related operations.
    """

    http_method_names = ('get', 'post')
    permission_classes = (AllowAny,)
    serializer_class = GenericPostSerializer
    pagination_class = ListPagination

    def get_queryset(self):
        user = self.request.user
        if isinstance(user, AnonymousUser):
            queryset = Post.objects.annotate(
                total_score=Avg('scores__score'),
                users_count=Count('user_scores'),
            )
        else:
            user_scores = UserPostScore.objects.filter(user=user, post=OuterRef('pk')).values('score')[:1]
            queryset = Post.objects.annotate(
                total_score=Avg('scores__score'),
                user_score=Subquery(user_scores, output_field=IntegerField()),
                users_count=Count('user_scores'),
            )
        return queryset

    @action(detail=True, methods=['post'], url_path='submit-score', throttle_classes=[CustomThrottle])
    @swagger_auto_schema(
        request_body=GenericUserPostScoreSerializer,
        responses={
            201: GenericUserPostScoreSerializer,
            429: "Too many requests",
        }
    )
    def submit_score(self, request, pk=None):
        """
        Endpoint to submit a score for a post.

        Args:
            request (Request): The incoming HTTP request.
            pk (str): The primary key of the post.

        Returns:
            Response: The HTTP response indicating success or failure.
        """
        serializer = GenericUserPostScoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        service = PostService(post=self.get_object())
        obj, err_msg = service.set_user_new_score_for_post(
            user=request.user, new_score=serializer.validated_data.get('score')
        )
        if not obj:
            return Response(data={"detail": err_msg}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        return Response(GenericUserPostScoreSerializer(obj).data, status=status.HTTP_201_CREATED)
