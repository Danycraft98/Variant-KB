import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'variant_db.settings')

import django

django.setup()


from api.models import PathItem, ITEMS

for key, value in ITEMS.items():
    PathItem.objects.get_or_create(key=key, value=value)
