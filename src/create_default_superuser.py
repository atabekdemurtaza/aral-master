import os

from django.contrib.auth import get_user_model


User = get_user_model()
User.objects.create_superuser(
    os.environ.get('ENV_SUPERUSER_USERNAME', 'admin'),
    os.environ.get('ENV_SUPERUSER_EMAIL', 'admin@example.com'),
    os.environ.get('ENV_SUPERUSER_PASSWORD', 'qwe123!@#'),
    first_name=os.environ.get('ENV_SUPERUSER_FIRST_NAME', 'Super'),
    last_name=os.environ.get('ENV_SUPERUSER_LAST_NAME', 'User'),
)
