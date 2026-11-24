"""Benzersiz kısa kod üretimi."""
import secrets

from app import database

# Karıştırılabilen karakterler (0/O, 1/l/I) bilerek çıkarıldı.
CHARS = "abcdefghijkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789"
LENGTH = 6


def generate_code() -> str:
    # secrets modülü, tahmin edilemeyen (kriptografik) rastgelelik sağlar
    return "".join(secrets.choice(CHARS) for _ in range(LENGTH))


def generate_unique_code() -> str:
    while True:
        code = generate_code()
        if not database.code_exists(code):
            return code
