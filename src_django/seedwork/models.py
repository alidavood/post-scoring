import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    create_time = models.DateTimeField(verbose_name=_('Create Time'), auto_now_add=True)
    modify_time = models.DateTimeField(verbose_name=_('Modify Time'), auto_now=True)
    auto_cols = ['create_time', 'modify_time']

    class Meta:
        abstract = True
        ordering = ('-create_time',)
        get_latest_by = ('create_time',)


class BaseUserModel(AbstractUser):

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        abstract = True
        ordering = ('last_name', 'first_name')
        get_latest_by = 'date_joined'
        indexes = [models.Index(fields=['username']),]
        verbose_name = _('User')
        verbose_name_plural = _('Users')
