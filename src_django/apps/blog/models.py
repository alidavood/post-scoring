from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from seedwork.models import BaseModel

User = get_user_model()


class Post(BaseModel):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'),
    )
    context = models.TextField(
        null=True,
        blank=True,
        verbose_name=_('Context'),
    )
    user_scores = models.ManyToManyField(
        to=User,
        through='UserPostScore',
        through_fields=('post', 'user'),
        related_name='post_scores',
        verbose_name=_('User scores'),
    )

    def __repr__(self):
        return f'Post obj --> id:{self.id} -- title:{self.title}'

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class UserPostScore(BaseModel):
    post = models.ForeignKey(
        to=Post,
        related_name='scores',
        on_delete=models.CASCADE,
        verbose_name=_('Post'),
    )
    user = models.ForeignKey(
        to=User,
        related_name='scores',
        on_delete=models.CASCADE,
        verbose_name=_('User'),
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Score'),
    )

    @property
    def score_times(self):
        return self.summited_scores.count()

    def __repr__(self):
        return f'UserPostScore obj --> id:{self.id} -- post:{self.post.id} -- user:{self.user.id}'

    def __str__(self):
        return f'{self.id} -- {self.score}'

    class Meta:
        unique_together = ['post', 'user']
        verbose_name = _('User Post Score')
        verbose_name_plural = _('User Post Scores')


class UserPostScoreHistory(BaseModel):
    user_post_score = models.ForeignKey(
        to=UserPostScore,
        related_name='summited_scores',
        on_delete=models.CASCADE,
        verbose_name=_('User Post Score'),
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name=_('Score'),
    )

    def __repr__(self):
        return f'UserPostScoreHistory obj --> id:{self.id}'

    def __str__(self):
        return f'{self.id} -- {self.score}'

    class Meta:
        verbose_name = _('User Post Score History')
        verbose_name_plural = _('User Post Scores History')
