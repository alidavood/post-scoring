# In your test code
from django.test import TestCase
from .factories import UserFactory


class UserTestCase(TestCase):
    def setUp(self):
        self.user_1 = UserFactory()

    def test_username_must_not_be_none(self):
        self.assertIsNotNone(self.user_1.username,)

    def test_first_name_must_not_be_none(self):
        self.assertIsNotNone(self.user_1.first_name,)

    def test_last_name_must_not_be_none(self):
        self.assertIsNotNone(self.user_1.last_name,)

    ...  # and so on
