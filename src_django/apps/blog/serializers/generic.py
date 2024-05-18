from django.utils.translation import gettext as _
from rest_framework import serializers

from ..models import *

User = get_user_model()


class GenericPostSerializer(serializers.ModelSerializer):
    total_score = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True, default="")
    user_score = serializers.CharField(read_only=True, default="")
    users_count = serializers.CharField(read_only=True, default="")

    class Meta:
        model = Post
        fields = ("id", "title", "context", "total_score", "user_score", "users_count")
        read_only_fields = ("id", "total_score", "user_score", "users_count")

    def to_representation(self, instance):
        data = super(GenericPostSerializer, self).to_representation(instance)

        if data['total_score'] is None:
            data['total_score'] = ""

        if data['user_score'] is None:
            data['user_score'] = ""

        return data


class GenericUserPostScoreSerializer(serializers.Serializer):
    user_score = serializers.IntegerField(
        default=None,
        source='score',
        validators=[
            MinValueValidator(1, message=_("Score must be at least 1")),
            MaxValueValidator(5, message=_("Score must be at most 5")),
        ])
