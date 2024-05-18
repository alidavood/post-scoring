import random
import time

from django.conf import settings
from django.test.runner import DiscoverRunner
from rest_framework.throttling import UserRateThrottle

# ERROR_RATE = 0.2
ERROR_RATE = 0.5


def third_party_simulator():
    time.sleep(1)

    if random.random() < ERROR_RATE:
        return {'data': 'failed', 'status': 503}

    return {'data': 'success', 'status': 200}


def make_bold_string(text: str) -> str:
    return f"\033[1m {text}  \033[0m"


class CustomTestRunner(DiscoverRunner):
    def setup_test_environment(self, **kwargs):
        super().setup_test_environment(**kwargs)
        settings.TEST_MODE = True


class CustomThrottle(UserRateThrottle):
    rate = '100/day'  # Limit requests to 5 per day per user
