"""
Settings for `manage.py test`: SQLite in-memory, no PostgreSQL or `.env` required.

Usage:

    uv run python manage.py test --settings=pet_shelter.settings_test
"""

from __future__ import annotations

import os

# Required before importing `settings` (which validates SECRET_KEY).
os.environ.setdefault("SECRET_KEY", "django-test-secret-not-for-production")

from pet_shelter.settings import *  # noqa: E402, F403

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    },
}

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]
