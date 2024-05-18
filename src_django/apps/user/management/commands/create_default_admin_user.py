from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Create default Admin user'

    def handle(self, *args, **kwargs):
        default_admin_user, created = User.objects.get_or_create(
            username="admin",
            is_superuser=True,
            is_staff=True,
        )
        if created:
            default_admin_user.set_password('asdfqwer')
            default_admin_user.save()
            print(f'Default system user with username: {default_admin_user.username} created')
        else:
            print(f'Default system user with username: {default_admin_user.username} existed')
