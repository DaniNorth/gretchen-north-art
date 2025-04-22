# create_superuser.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gretchen_north_art.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="DaniNorth",
        email="danielle.b.north@gmail.com",
        password="Secured11!"
    )
    print("Superuser created ✅")
else:
    print("Superuser already exists 🚫")
