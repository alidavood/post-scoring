from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    name = 'apps.user'
    verbose_name = _('user')
    default_auto_field = 'django.db.models.BigAutoField'
