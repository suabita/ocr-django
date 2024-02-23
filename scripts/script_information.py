import os

import sys
sys.path.append('/home/karen/Documents/ocr-django_project/ocr-django')

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ocrdjproject.settings')
django.setup()

import pandas as pd

from information.models import Information
from nutrient.models import Nutrient


# Leer el archivo Excel y convertirlo en un DataFrame
try:
    df = pd.read_excel("/home/karen/Downloads/base_datos_script(1).xlsx")
    print("try")
except Exception as e:
    print("Error al leer el archivo Excel:", e)

# Iterar sobre las filas del DataFrame y crear objetos del modelo de Django
for index, row in df.iterrows():
    nutrientes = Nutrient.objects.filter(name=row['nutrientes']).last()
    print("nutrientes", nutrientes)
    tipo = 0 if row['tipo'] == "Concepto" else 1
    print("tipo", tipo)
    concepto = row['concepto']
    information = None
    if concepto:
        information = concepto
    else:
        information = row["implicaciones"]
    print("information", information)

    documentacion = row['documentacion']
    print("documentacion", documentacion)
    if nutrientes:
        objeto_nuevo = Information(
            nutrient=nutrientes,
            information=information,
            type_information=tipo,
            bibliography=documentacion,

            #Añade más campos según sea necesario
        )
        objeto_nuevo.save()