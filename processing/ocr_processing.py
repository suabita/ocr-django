import boto3
from openai import OpenAI
from ocrdjproject.settings import OPENAI_KEY

class OcrProcessing:

    image_procesed_path = None

    def __init__(self, image_procesed_path):
        self.image_procesed_path = image_procesed_path

    """100g / porcion"""
    def run(self):
        bucket = 'foodlensocr'
        # photo = 'media/user/7/nutritional_table_processedb4e36d12-bcaa-49a2-bb16-8f2df1d98d42.jpg'
        text_detections = self.detect_text(self.image_procesed_path, bucket)
        text_in_rows = self.organize_text_by_rows(text_detections)
        print(text_in_rows)


        client = OpenAI(
        # This is the default and can be omitted
            api_key=OPENAI_KEY,
        )
        promt = self.get_prompt(text_in_rows)
        print(promt)
        chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": promt,
                    }
                ],
                model="gpt-3.5-turbo",
            )
        print('chat_completion', chat_completion.choices[0].message.content)
        return chat_completion.choices[0].message.content



    def detect_text(self, photo, bucket):
        session = boto3.Session()
        client = session.client('rekognition')
        response = client.detect_text(Image={'S3Object': {'Bucket': bucket, 'Name': photo}})
        return response['TextDetections']


    def organize_text_by_rows(self, text_detections, tolerance=0.01):
        rows = {}
        current_top = 0
        for detection in text_detections:
            if detection['Type'] == 'LINE':
                top = detection['Geometry']['BoundingBox']['Top']
                print(top, detection['DetectedText'])
                if (top - current_top) >= tolerance:
                    current_top = top
                if current_top in rows:
                    rows[current_top].append(detection)
                else:
                    rows[current_top] = [detection]

        for top, texts in rows.items():
            texts.sort(key=lambda x: x['Geometry']['BoundingBox']['Left'])

        rows_strings = []
        for top, texts in rows.items():
            rows_strings.append(" / ".join([text['DetectedText'] for text in texts]))

        return '\n'.join(rows_strings)
    

    def get_prompt(self, ocr_output):

        prompt = f"""
        Eres el mecanismo de post procesamiento de mi algoritmo de OCR para lectura de etiquetas de información nutricional de paquetes de frituras, recibirás como entrada el output del procesamiento y deberás interpretar la información siguiendo las siguientes directrices:\n
        1. Lee el nombre del nutriente y las dos cantidades que corresponden a cada uno (100 gramos y por porción)\n
        2. Los nombres de los nutrientes pueden tener errores, por ejemplo "acicales" es realmente "azúcares" así que, interpreta esto de manera correcta.\n
        3. Si lees algo como Fibra dietética o Fibra cambialo por Fibra dietaria.\n
        4. Si lees algo como Carbohidratos Totales o Carb. Total. o Carbohidrato total cambialo por Carbohidratos totales.\n
        5. Si lees algo como Grasa sat. o Grasa Saturada cambialo por Grasa saturada. \n
        6. Si lees algo como Grasa Trans o Trans o Grasas Trans o Grasas trans cambialo por Grasa trans.\n
        7. Si lees algo como Az. añadidos o Azúcares Anadidos cambialo por Azúcares añadidos.\n
        8. Si lees algo como Grasa o Grasas o Grasa Total o Grasas totales cambialo por Grasa total. \n
        9. Si lees algo como Energía (kcal) o Energía (Kcal) o Energía (KCal) o Calorías (Kcal) o similar cambialo por Calorías (kcal).\n
        10. siempre lleva las unidades, ya sea g, o mg, a veces un 9 puede confundirse con la g, toma esto en cuenta para realizar la interpretación. También puede confundir letras por números, ejemplo B es un 8, una O por un 0, una i o l por un 1, etc. toma esto en cuenta\n
        11. si al final de la lectura del valor no encuentras un g o mg, toma el ultimo digito y cambialo por una g ya que el OCR hizo la lectura erroneamente\n 
        Tu respuesta debe ser UNICAMENTE un objeto json con claves y valores de la siguiente manera, con este ejemplo: {{"Azucares añadidos": ["100 mg", "45 mg"], "sodio": ["45 g", "12 g"]}} en la que des el nombre del nutriente como llave y como valor un array con dos cantidades, la de 100g y la de por porción, también agrega la cantidad de calorías.\n
        este es el input:\n
        {ocr_output}\n
        """
        return prompt
    
