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

from information.models import Information
from daily_quantity.models import DailyQuantity


import pandas as pd

from information.models import Information
from nutrient.models import Nutrient

# nutrient = Nutrient.objects.filter(name="Sodio").last()
# print(nutrient)
# nutrient.name= "Sodio"
# nutrient.save()





nutrients = [
    "Biotina",
    "Calcio",
    "Colina",
    "Cromo",
    "Cobre",
    "Folato",
    "Yodo",
    "Cloruro",
    "Hierro",
    "Magnesio",
    "Manganeso",
    "Niacina",
    "Fósforo",
    "Potasio",
    "Riboflavina",
    "Selenio",
    "Tiamina",
    "Vitamina B12",
    "Vitamina B6",
    "Vitamina E",
    "Vitamina K",
    "Vitamina C",
    "Vitamina A",
    "Vitamina D",
    "Ácido pantoténico",
    "Zinc",
    "sodio",
    "Proteína",
    "Grasa",
    "Fluoruro",
    "Carbohidratos",
    "Fibra dietaria",
    "Fibra soluble",
    "Fibra insoluble",
    "Azúcares",
    "Azúcares añadidos",
    "Azúcares totales",
    "Molibdeno",
    "Lípido",
    "Ácido linoleico",
    "Ácido alfa-linolénico",
    "Grasa insaturada",
    "Grasa trans",
    "Grasa saturada",
    "Grasa poliinsaturada",
    "Grasa monoinsaturada",
    "Colesterol"
]


# concept = Information.objects.filter(nutrient__name="Lípido", type_information=0)
# print(concept.id, concept.nutrient.name, concept.information)
# concept.delete()
# for con in concept:
#     print(con.nutrient.name, con.id, con.information)


# print(len(nutrients))
nutrient_qs = Nutrient.objects.filter(name="Calorías").last()

# print(ascii(nutrient_qs.name), ascii(nutrient_qs.cached_recommendations))
# nutrient_qs.cached_recommendations = {}
# nutrient_qs.save()
# print(ascii(nutrient_qs.name), ascii(nutrient_qs.cached_recommendations))

# for nutrient in nutrient_qs:
#     daily = DailyQuantity.objects.filter(nutrient__name=nutrient.name).count()
#     print(nutrient, daily)
#     concept = Information.objects.filter(nutrient__name=nutrient.name, type_information=0).count()
#     impli = Information.objects.filter(nutrient__name=nutrient.name, type_information=1).count()
#     print(nutrient, concept, impli)
# print(Information.objects.count())





# for i in information:
#     i.delete()
# for n in ["Calorías"]:
#     nutrient = Nutrient(name=n)
#     nutrient.save()





# units = [
#     "mcg/día",
#     "mg/día",
#     "g/día"
# ]

# for u in units:
#     unitt= Unit(name=u)
#     unitt.save()
# daily = DailyQuantity.objects.filter(nutrient__name="Fibra dietaria", recommendable_quantity=5).last()
# print("daily total", daily.nutrient, daily.recommendable_quantity)
# daily.nutrient = Nutrient.objects.filter(name="Azúcares añadidos").last()
# print("daily total", daily.nutrient, daily.recommendable_quantity)
# daily.save()


# nutrient= Nutrient.objects.filter(name="Biotina").last()
# daily = DailyQuantity.objects.filter(nutrient=nutrient)
# info = Information.objects.filter(nutrient=nutrient)
# references = []
# for d in daily:
#     references.append(d.bibliography)
# for i in info:
#     references.append(i.bibliography)
# print(nutrient.name, set(references))

""" 
daily = DailyQuantity.objects.all()
print("daily total", daily.count())
for d in daily:
    print("daily quantity", d.__dict__)


for n in ["Ácido pantoténico"]:
    nutrient = Nutrient(name=n)
    nutrient.save() """


# quantity = DailyQuantity.objects.filter(nutrient__name="Grasa total",
#                                                     max_age_range__gte=26,
#                                                     min_age_range__lte=26,
#                                                     life_stage=2).first()
# print(quantity.__dict__)


n = Nutrient.objects.filter(name="Grasa total").last()
# n.name = "Carbohidratos totales"
# n.save()
print(n.name,n.id)
# # n.delete()

table = NutritionalTable.objects.filter(id=120).last()
# table.recommendations["Calorías"]["recommended_quantity"] = "1567.1626 Kcal"
# table.save()
print(ascii(table.file_table_processed))

nutrient = Nutrient.objects.filter(name__icontains="Proteína").last()
print(nutrient.name, nutrient.cached_recommendations)

