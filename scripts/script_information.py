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
    df = pd.read_excel("/home/karen/Downloads/base_datos_script(3).xlsx")
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
    implicaciones = row["impli"]
    print("concepto", concepto)
    print("implicaciones", implicaciones)
    information = None
    if tipo == 0:
        information = concepto
    else:
        information = implicaciones
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
        print("objeto_nuevo", objeto_nuevo)
        try:
            nuevo = objeto_nuevo.save()
            print("nuevo", nuevo)
            print("Objeto guardado correctamente.")
        except Exception as e:
            print("Error al guardar el objeto:", e)
        # nuevo =objeto_nuevo.save()
        