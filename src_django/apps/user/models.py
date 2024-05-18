from django.db import models
from django.utils.translation import gettext_lazy as _

from seedwork.models import BaseUserModel, BaseModel


class User(BaseUserModel):
    REQUIRED_FIELDS = []

    class Meta:
        indexes = [
            *BaseUserModel.Meta.indexes,
            models.Index(fields=['first_name']),
            models.Index(fields=['last_name']),
            models.Index(fields=['is_staff']),
            models.Index(fields=['is_active']),
        ]

