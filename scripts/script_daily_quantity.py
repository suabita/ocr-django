import os

import sys
sys.path.append('/home/karen/Documents/ocr-django_project/ocr-django')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocrdjproject.settings')
django.setup()

import pandas as pd

from nutrient.models import Nutrient
from daily_quantity.models import DailyQuantity
from unit.models import Unit



# Leer el archivo Excel y convertirlo en un DataFrame
try:
    df = pd.read_excel("/home/karen/Downloads/base_datos_cantidades_script(2).xlsx")
    print("try")
except Exception as e:
    print("Error al leer el archivo Excel:", e)

life_stage = {
    "infante": 0,
    "niño": 1,
    "mujer": 2,
    "hombre": 3,
    "embarazo": 4,
    "lactancia": 5
}

# Iterar sobre las filas del DataFrame y crear objetos del modelo de Django
for index, row in df.iterrows():
    nutriente = Nutrient.objects.filter(name=row['nutriente']).last()
    print("nutriente", nutriente)
    etapa = life_stage[row['etapa'].lower()]
    print("etapa", etapa)
    edad_minima = row['edad_minima']
    edad_maxima = row['edad_maxima']
    cantidad = row['cantidad']
    unidad = Unit.objects.filter(name=row['unidad']).last()
    documentacion = row['documentacion']
    print("edad_minima", edad_minima)
    print("edad_maxima", edad_maxima)
    print("documentacion", documentacion)
    if nutriente:
        objeto_nuevo = DailyQuantity(
            nutrient=nutriente,
            life_stage=etapa,
            max_age_range=edad_maxima,
            min_age_range=edad_minima,
            recommendable_quantity=cantidad,
            unit=unidad,
            bibliography=documentacion,

            #Añade más campos según sea necesario
        )
        objeto_nuevo.save()