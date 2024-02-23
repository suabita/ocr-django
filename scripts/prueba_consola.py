import os

import sys
sys.path.append('/home/karen/Documents/ocr-django_project/ocr-django')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocrdjproject.settings')
django.setup()

from authentication.user.models import User
from nutritional_table.models import NutritionalTable
from nutrient.models import Nutrient
from unit.models import Unit
from daily_quantity.models import DailyQuantity


u = User.objects.last()
print("user created",u.__dict__)

n = NutritionalTable.objects.count()
print("nutritional table", n)


nutrients_1 = [
    "Biotina",
    "Boro",
    "Calcio",
    "Carnitina",
    "Colina",
    "Cromo",
    "Cobre",
    "Fluoruro",
    "Folato",
    "Yodo",
    "Hierro",
    "Magnesio",
    "Manganeso",
    "Molibdeno",
    "Niacina",
    "Omega-3",
    "Fósforo",
    "Potasio",
    "Probióticos",
    "Riboflavina",
    "Selenio",
    "Tiamina",
    "Vitamina B12",
    "Vitamina B6",
    "Vitamina E",
    "Vitamina K",
    "Zinc"
]

nutrients = [
    "Proteína",
    "Grasa",
    "Grasa insaturada",
    "Grasa trans",
    "Grasa saturada",
    "Grasa poliinsaturada",
    "Grasa monoinsaturada",
    "Colesterol",
    "Lípido",
    "Carbohidratos",
    "Fibra dietaria",
    "Fibra soluble",
    "Fibra insoluble",
    "Azucares",
    "Azucares añadidos",
]

#for n in nutrients:
    #nutrient = Nutrient(name=n)
    #nutrient.save()



units = [
    "mcg/día"
]

daily = DailyQuantity.objects.all()
print("daily total", daily.count())
for d in daily:
    print("daily quantity", d.__dict__)


for n in ["Ácido pantoténico"]:
    nutrient = Nutrient(name=n)
    nutrient.save()