from django.contrib.admin import register
from django.contrib.auth import get_user_model

from seedwork.admin import BaseUserAdmin

User = get_user_model()


@register(User)
class CustomUserAdmin(BaseUserAdmin):
    ...
