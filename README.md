# OCR - Django

Este proyecto es el código fuente de un proyecto que implementa el reconocimiento optico de caracteres en una aplicación
hecha en Django que permite a los usuarios cargar una imagen de una tabla nutricional de una fritura y obtener información
relevante sobre su composición.

## Requisitos

- Python (versión 3.8.18)
- Django (versión 4.2.9)

## Servidor de desarrollo
### Utilizando Django:
* Clona este repositorio en tu maquina local:
  ```bash
    git clone https://github.com/suabita/ocr-django.git
    ```
* Asegúrate de tener un ambiente virtual de python con los paquetes definidos en el `requiremenst.txt` instalados.
* Activa el modo de desarrollo poniendo en `True` la variable `DEBUG` del archivo settings.
* En la carpeta raíz del proyecto ejecuta el comando `python manage.py runserver 127.0.0.1:8000`.
* El servidor se ejecutará en [localhost:8000](http://127.0.0.1:8000).
