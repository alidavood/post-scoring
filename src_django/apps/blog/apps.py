from django.apps import AppConfig

from django.utils.translation import gettext_lazy as _


class WalletConfig(AppConfig):
    name = 'apps.blog'
    verbose_name = _('Blog')
    default_auto_field = 'django.db.models.BigAutoField'
