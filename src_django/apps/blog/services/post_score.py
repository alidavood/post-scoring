from datetime import timedelta, datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext as _

from ..models import Post, UserPostScore, UserPostScoreHistory

User = get_user_model()


class PostService:
    """
    Service class for handling post-related operations.
    """

    DAILY_LIMIT = 5
    MONTHLY_LIMIT = 100
    POST_LIMIT = 3
    POST_MONTHLY_LIMIT_DAYS = 3

    def __init__(self, post: Post):
        """
        Initializes the PostService instance with a given post.

        Args:
            post (Post): The post object to be handled by the service.
        """
        self.post = post

    def set_user_new_score_for_post(
            self,
            user: User,
            new_score: int,
    ) -> tuple[UserPostScore | None, str | None]:
        """
        Sets a new score for a user on a post.

        Args:
            user (User): The user for whom the score is being set.
            new_score (int): The new score to be set for the user.

        Returns:
            tuple[UserPostScore | None, str | None]: A tuple containing the updated UserPostScore object (if successful)
            and an error message (if any).
        """

        rate_limited, err_msg = self._does_user_rate_limited_generally(user=user)
        if rate_limited:
            return None, err_msg

        already_submitted, last_score_obj = self._did_user_already_submit_score(user=user)
        if not already_submitted:
            obj = self._set_user_score(user=user, new_score=new_score)
            return obj, None

        rate_limited, err_msg = self._does_user_rate_limited_for_the_post(last_score_obj=last_score_obj)
        if rate_limited:
            return None, err_msg

        obj = self._set_user_score_and_save_score_history(new_score=new_score, last_score_obj=last_score_obj)
        return obj, None

    def _did_user_already_submit_score(self, user: User) -> tuple[bool, UserPostScore | None]:
        """
        Checks if a user has already submitted a score for the post.

        Args:
            user (User): The user to check for.

        Returns:
            tuple[bool, UserPostScore | None]: A tuple indicating whether the user has already submitted a score
            and the corresponding UserPostScore object (if found).
        """

        try:
            last_score = UserPostScore.objects.get(user=user, post=self.post)
            return True, last_score
        except UserPostScore.DoesNotExist:
            return False, None

    def _set_user_score(self, user: User, new_score: int) -> UserPostScore:
        """
        Creates a new UserPostScore object to record the user's score for the post.

        Args:
            user (User): The user for whom the score is being set.
            new_score (int): The new score to be set for the user.

        Returns:
            UserPostScore: The newly created UserPostScore object.
        """
        return UserPostScore.objects.create(post=self.post, user=user, score=new_score)

    @staticmethod
    def _update_user_score(last_score_obj: UserPostScore, score: int) -> UserPostScore:
        """
        Updates the score of a UserPostScore object.

        Args:
            last_score_obj (UserPostScore): The UserPostScore object to be updated.
            score (int): The new score to be set.

        Returns:
            UserPostScore: The updated UserPostScore object.
        """
        last_score_obj.score = score
        last_score_obj.save()
        return last_score_obj

    @staticmethod
    def _create_user_score_history(user_post_score: UserPostScore) -> UserPostScoreHistory:
        """
        Creates a new UserPostScoreHistory object to record the user's score history.

        Args:
            user_post_score (UserPostScore): The UserPostScore object for which the history is being recorded.

        Returns:
            UserPostScoreHistory: The newly created UserPostScoreHistory object.
        """
        return UserPostScoreHistory.objects.create(user_post_score=user_post_score, score=user_post_score.score)

    def _does_user_rate_limited_generally(self, user: User) -> tuple[bool, str | None]:
        """
        Checks if a user is rate-limited in submitting scores.

        Args:
            user (User): The user to check for.

        Returns:
            tuple[bool, str | None]: A tuple indicating whether the user is rate-limited and an error message (if any).
        """
        checks = [
            self._does_user_rate_limited_today_generally(user),
            self._does_user_rate_limited_this_month_generally(user),
        ]

        for rate_limited, err_msg in checks:
            if err_msg:
                return rate_limited, err_msg

        return False, None

    @classmethod
    def _does_user_rate_limited_today_generally(cls, user: User) -> tuple[bool, str | None]:
        """
        Checks if a user is rate-limited for today.

        Args:
            user (User): The user to check for.

        Returns:
            tuple[bool, str | None]: A tuple indicating whether the user is rate-limited and an error message (if any).
        """
        if UserPostScore.objects.filter(user=user, create_time__date=timezone.now().date()).count() >= cls.DAILY_LIMIT:
            return True, _('You have reached the maximum number of submissions allowed for today')
        return False, None

    @classmethod
    def _does_user_rate_limited_this_month_generally(cls, user: User) -> tuple[bool, str | None]:
        """
        Checks if a user is rate-limited for this month.

        Args:
            user (User): The user to check for.

        Returns:
            tuple[bool, str | None]: A tuple indicating whether the user is rate-limited and an error message (if any).
        """
        if UserPostScore.objects.filter(user=user,
                                        create_time__month=timezone.now().month).count() >= cls.MONTHLY_LIMIT:
            return True, _('You have reached the maximum number of submissions allowed for this month')
        return False, None

    @classmethod
    def _does_user_rate_limited_for_the_post(cls, last_score_obj: UserPostScore) -> tuple[bool, str | None]:
        """
        Checks if a user is rate-limited for the post.

        Args:
            last_score_obj (UserPostScore): The last score object submitted by the user for the post.

        Returns:
            tuple[bool, str | None]: A tuple indicating whether the user is rate-limited and an error message (if any).
        """
        if last_score_obj.summited_scores.count() >= cls.POST_LIMIT:
            return True, _('You have reached the maximum number of submissions allowed for this post')

        if last_score_obj.modify_time >= cls._calculate_some_days_ago(days=30):
            return True, _(
                'You have reached the maximum number of submissions allowed for this post in the last 30 days'
            )

        return False, None

    @staticmethod
    def _calculate_some_days_ago(days: int) -> datetime:
        """
        Calculates the datetime of a specified number of days ago.

        Args:
            days (int): The number of days.

        Returns:
            datetime: The calculated datetime.
        """
        return timezone.now() - timedelta(days=days)

    def _set_user_score_and_save_score_history(self, new_score: int, last_score_obj: UserPostScore) -> UserPostScore:
        """
        Sets the user's score for the post and saves the score history.

        Args:
            new_score (int): The new score to be set.
            last_score_obj (UserPostScore): The last score object submitted by the user for the post.

        Returns:
            UserPostScore: The updated UserPostScore object.
        """
        if self._check_does_new_score_equal_to_saved_score(last_score_obj, new_score=new_score):
            return last_score_obj
        with transaction.atomic():
            self._create_user_score_history(user_post_score=last_score_obj)
            return self._update_user_score(last_score_obj=last_score_obj, score=new_score)

    @staticmethod
    def _check_does_new_score_equal_to_saved_score(last_score_obj: UserPostScore, new_score: int) -> bool:
        """
        Checks if a new score is equal to the previously saved score.

        Args:
            last_score_obj (UserPostScore): The last score object submitted by the user for the post.
            new_score (int): The new score.

        Returns:
            bool: True if the new score is equal to the previously saved score, False otherwise.
        """
        return last_score_obj.score == new_score
