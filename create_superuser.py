#!/usr/bin/env python
import os
import django
from datetime import date

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'softdesk_api.settings')
django.setup()

from accounts.models import User

# Créer un superutilisateur avec les champs requis
if not User.objects.filter(username='admin').exists():
    user = User.objects.create_superuser(
        username='admin',
        email='admin@softdesk.com',
        password='admin123',
        birth_date=date(1990, 1, 1),
        can_be_contacted=True,
        can_data_be_shared=False
    )
    print(f"Superutilisateur créé: {user.username}")
else:
    print("Le superutilisateur existe déjà.")
