import os

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "litrevu.settings")
django.setup()

from django.contrib.auth import get_user_model


def create_users():
    User = get_user_model()

    users_data = [
        {"username": "user1", "email": "user1@example.com", "password": "password123"},
        {"username": "user2", "email": "user2@example.com", "password": "password123"},
        {"username": "user3", "email": "user3@example.com", "password": "password123"},
        {"username": "user4", "email": "user4@example.com", "password": "password123"},
    ]

    for user_data in users_data:
        if not User.objects.filter(username=user_data["username"]).exists():
            User.objects.create_user(
                username=user_data["username"], email=user_data["email"], password=user_data["password"]
            )
            print(f"Utilisateur {user_data['username']} créé.")
        else:
            print(f"Utilisateur {user_data['username']} existe déjà.")


if __name__ == "__main__":
    create_users()
