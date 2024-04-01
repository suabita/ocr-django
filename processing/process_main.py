from processing.ocr_processing import OcrProcessing
from processing.user_response import UserResponse
from processing.image_preprocessing import ImagePreprocessing
import json
from nutritional_table.models import StatusChoices


class ProcessingMain:
    #
    #ocr
    #ocr devuelve un diccinario
    #iterar el diccionario de la tabla leida
    #por cada uno traer el cached_recomendation
    #si no hay entonces consultar a la ia y de paso guardar en cached_recomendation
    #
    user = None
    nutritional_table = None
    new_response = False

    def __init__(self, user, nutritional_table, new_response):
        self.user = user
        self.nutritional_table = nutritional_table
        self.new_response = new_response

    def run(self):
        print("iniciando analisis")
        if self.nutritional_table:
            image_procesed_path = ImagePreprocessing(self.nutritional_table).run()
            table_ocr_info = OcrProcessing(image_procesed_path).run()
            self.nutritional_table.ocr_data = json.loads(table_ocr_info)
            print("OCR tabla", table_ocr_info)
            user_response = UserResponse(self.nutritional_table.ocr_data , self.user, self.new_response).run()
            print("user_response", ascii(user_response))
            self.nutritional_table.recommendations = user_response
            self.nutritional_table.status = StatusChoices.SUCCESS
            self.nutritional_table.save()