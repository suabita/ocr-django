import cv2
import numpy as np
import os
from django.core.files import File
import boto3
import uuid

from ocrdjproject.settings import AWS_STORAGE_BUCKET_NAME

class ImagePreprocessing:
    #recorte del rectangulo
    #
    #limpieza
    #recorte cuadro a cuadro
    #lectura de cada cuadro
    #nutritional_table es una instancia de modelo
    #original_image es un path de donde esta guardada localmente la imagen original
    original_image = None
    nutritional_table = None

    def __init__(self, nutritional_table):
        self.nutritional_table = nutritional_table
        s3_client = boto3.client("s3")
        # file_s3 = s3_client.get_object(bucket_name=AWS_STORAGE_BUCKET_NAME,
        #                                key=self.nutritional_table.file_table.name)

        file_extension = os.path.splitext(self.nutritional_table.file_table.name)[1]
        file_path = "./temp_files_ocr/original_image.{}".format(file_extension)
        print("ruta de la tabla", self.nutritional_table.file_table.name)
        s3_client.download_file(AWS_STORAGE_BUCKET_NAME,
                                "media/{}".format(self.nutritional_table.file_table.name),
                                "./temp_files_ocr/original_image.{}".format(file_extension))
        self.original_image = cv2.imread(file_path)
        self.original_image = cv2.resize(self.original_image, (1280, 720))


    def run(self):
        seleccion = self.rectangle_cut()
        puntos_ordenados = self.ordenar_puntos(seleccion)
        imagen_nueva = self.get_table_image(puntos_ordenados)
        self.table_processing(imagen_nueva)
        return self.upload_processed_image("./temp_files_ocr/imagen sin ruido.jpg")


    def rectangle_cut(self):
        
        gray = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2GRAY)
        # Binarizacion (blanco y negro)
        thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 3, 2)
        # Buscar contornos rectangulares para aislar la tabla
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # Encontrar el contorno más grande, que debería ser la tabla
        max_area = 0
        largest_contour = None
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour
            Seleccion = []
        # Dibujar un rectángulo alrededor de la tabla
        new_image = self.original_image.copy()
        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            x1, y1 = x, y  # Vértice superior izquierdo
            x2, y2 = x + w, y  # Vértice superior derecho
            x3, y3 = x, y + h  # Vértice inferior izquierdo
            x4, y4 = x + w, y + h  # Vértice inferior derecho

            Seleccion.append((x1, y1))
            Seleccion.append((x2, y2))
            Seleccion.append((x4, y4))
            Seleccion.append((x3, y3))

            cv2.rectangle(new_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return Seleccion
    

    def ordenar_puntos(self, pts):
        # una lista de coordenadas que se ordenarán
        # tal que la primera entrada de la lista es la parte superior izquierda,
        # la segunda entrada es la parte superior derecha, la tercera es la
        # abajo a la derecha, y el cuarto es el abajo a la izquierd
        # Convertir la lista de puntos en una matriz NumPy
        pts = np.array(pts)
        pts = pts.reshape(4, 2)
        recta = np.zeros((4, 2), dtype="float32")

        # el punto superior izquierdo tendrá la suma más pequeña, mientras que
        # el punto inferior derecho tendrá la suma más grande
        s = pts.sum(axis=1)
        recta[0] = pts[np.argmin(s)]
        recta[2] = pts[np.argmax(s)]

        # Ahora, calcula la diferencia entre los puntos, el
        # el punto superior derecho tendrá la diferencia más pequeña,
        # mientras que la parte inferior izquierda tendrá la mayor diferencia
        diff = np.diff(pts, axis=1)
        recta[1] = pts[np.argmin(diff)]
        recta[3] = pts[np.argmax(diff)]

        # Devuelve las coordenadas ordenadas
        return recta
    


    def DistanciaEntreDosPuntos(self, p1, p2):
        dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        return dis


    def get_table_image(self, puntos_ordenados):
        Ancho_imagen_original = self.original_image.shape[1]
        Ancho_reducido_60 = int(Ancho_imagen_original * 0.8)

        # Medicion de distancias
        # 1. Mide la distancias , superior izquierda a inferior derecha
        # 2. Mide la distancia, superior izquierda a inferior izquierda

        Distancia_SI_ID = self.DistanciaEntreDosPuntos(puntos_ordenados[0], puntos_ordenados[2])
        Distancia_SI_II = self.DistanciaEntreDosPuntos(puntos_ordenados[0], puntos_ordenados[3])

        # Obtenidas las distancias la realacion de ancho y altura necesaria para la nueva imagen

        Rango_aspecto = Distancia_SI_ID / Distancia_SI_II
        # Composicion de la imagen nueva
        Ancho_nuevo = Ancho_reducido_60
        Altura_nueva = int(Ancho_nuevo * Rango_aspecto)

        pts1 = np.float32(puntos_ordenados)
        pts2 = np.float32([[0, 0], [Ancho_nuevo, 0], [Ancho_nuevo, Altura_nueva], [0, Altura_nueva]])
        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        tabla = cv2.warpPerspective(self.original_image, matrix, (Ancho_nuevo, Altura_nueva), cv2.INTER_CUBIC)
        Altura_imagen = self.original_image.shape[0]
        padding = int(Altura_imagen * 0.04)
        imagen_nueva = cv2.copyMakeBorder(tabla, padding, padding, padding, padding, cv2.BORDER_CONSTANT,
                                            value=[255, 255, 255])
        return imagen_nueva
    
    def table_processing(self, tabla):
        #Tratamiento de la tabla
        # Convertir la imagen a escala de grises
        gris = cv2.cvtColor(tabla, cv2.COLOR_BGR2GRAY)

        # Binarizar la imagen usando umbral adaptativo
        binarizado = cv2.adaptiveThreshold(gris, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 13, 11)

        # Detección y eliminación de líneas verticales
        kernel_verticales = np.ones((1, 60), np.uint8)
        lineas_verticales = cv2.morphologyEx(binarizado, cv2.MORPH_OPEN, kernel_verticales)

        # Detección y eliminación de líneas horizontales
        kernel_horizontales = np.ones((60, 1), np.uint8)
        lineas_horizontales = cv2.morphologyEx(binarizado, cv2.MORPH_OPEN, kernel_horizontales)

        # Combinar resultados para eliminar líneas
        lineas_combinadas = cv2.add(lineas_verticales, lineas_horizontales)

        # Dilatar para detectar ruido
        kernel_dilatacion = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        lineas_dilatadas = cv2.dilate(lineas_combinadas, kernel_dilatacion, iterations=2)

        # Eliminar líneas de la imagen binarizada
        imagen_sin_lineas = cv2.subtract(binarizado, lineas_dilatadas)

        # Eliminar ruido adicional
        kernel_ruido = np.ones((2, 2), np.uint8)
        imagen_sin_ruido = cv2.morphologyEx(imagen_sin_lineas, cv2.MORPH_OPEN, kernel_ruido)

        cv2.imwrite("./temp_files_ocr/imagen sin ruido.jpg",imagen_sin_ruido)

        # cv2.imshow("tabla", imagen_sin_ruido)
        

        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


    def limpiar_directorio(self, directorio):
        for archivo in os.listdir(directorio):
            ruta_completa = os.path.join(directorio, archivo)
            if os.path.isfile(ruta_completa):
                os.remove(ruta_completa)
            

    def upload_processed_image(self, local_file_path):
        ext = os.path.splitext(local_file_path)[1]

        object_name='media/user/{id_user}/nutritional_table_processed{u_id}{ext}'.format(id_user=self.nutritional_table.user.id, u_id=uuid.uuid4(), ext=ext)

        s3_client = boto3.client('s3')
        s3_client.upload_file(local_file_path, AWS_STORAGE_BUCKET_NAME, object_name)

        return object_name
        # with open(local_file_path, 'rb') as f:
        #     # Crea un objeto File desde el archivo local
        #     django_file = File(f)
            
        #     # Asigna el archivo al campo file_field
        #     self.nutritional_table.file_table_processed.save("images_processed", django_file)
            
        #     # Guarda el objeto del modelo
        #     self.nutritional_table.save()