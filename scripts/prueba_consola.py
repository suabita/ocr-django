import os

import sys
sys.path.append('/home/karen/Documents/ocr-django_project/ocr-django')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocrdjproject.settings')
django.setup()

from authentication.user.models import User
from nutritional_table.models import NutritionalTable


u = User.objects.last()
print("user created",u.__dict__)

n = NutritionalTable.objects.last()
print("nutritional table", n.__dict__)
