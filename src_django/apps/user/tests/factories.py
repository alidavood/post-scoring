import factory
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('uuid4')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = make_password('password_test')
