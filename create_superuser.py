#!/usr/bin/env python
import os
import django
from django.conf import settings

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from accounts.models import CustomUser

# Create superuser if it doesn't exist
if not CustomUser.objects.filter(username='sysadmin').exists():
    user = CustomUser.objects.create_superuser(
        username='sysadmin',
        email='admin@example.com',
        password='admin123',
        first_name='System',
        last_name='Administrator'
    )
    print(f"Superuser 'sysadmin' created successfully")
else:
    print("Superuser 'sysadmin' already exists")