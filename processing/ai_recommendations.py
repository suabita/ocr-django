from openai import OpenAI
from information.models import Information, TypeChoices
from ocrdjproject.settings import OPENAI_KEY
import json

class AIRecommendations:
    nutrient = None

    def __init__(self, nutrient):
        self.nutrient = nutrient

    def run(self):
        client = OpenAI(
        # This is the default and can be omitted
        api_key=OPENAI_KEY,
        )
        promt = self.get_prompt()
        print("promt", promt)
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
        return json.loads(chat_completion.choices[0].message.content)

    def get_prompt(self):
        concepts_str = ''
        implications_str = ''

        concepts = Information.objects.filter(nutrient=self.nutrient, type_information=TypeChoices.DEFINITION)
        implications = Information.objects.filter(nutrient=self.nutrient, type_information=TypeChoices.ILLNESS)

        for concept in concepts:
            concepts_str += f"- {concept.information} \n"
        for implication in implications:
            implications_str += f"- {implication.information} \n"


        prompt = f"""
        Eres una API que da al usuario información nutricional útil sobre el nutriente {self.nutrient.name}, solo obtienes esa información del contexto almacenado en la base de datos, 
        así que por ningún motivo te salgas de ese contexto que te voy a dar. La respuesta que vas a entregar será un objeto json con dos llaves, la primera será "concepto" y como valor un resumen del concepto del nutriente
        y la segunda llave será "implicaciones" y como valor será un resumen de las implicaciones para la salud asociadas al exceso o a la deficiencia de ese nutriente, entonces entrega así: 

        {{"concepto":"resumen del concepto basado totalmente en el contexto que te daré, si no te doy contexto deja un string vacío",
        "implicaciones":"Un resumen de las implicaciones para la salud asociadas al exceso o a la deficiencia de ese nutriente, pero teniendo en cuenta únicamente el contexto que te daré, si no te doy contexto deja un string vacío"}}
        
        Como nota importante, solo usa el contexto que te daré a continuación y por ningún motivo te salgas de él o agregues información diferente. Por favor devuelve unicamente el objeto json
        Recuerda siempre siempre devolver la respuesta con el formato tipo json que te indiqué.
    
        CONTEXTO DEL CONCEPTO:\n
        {concepts_str}  \n
        
        CONTEXTO DE IMPLICACIONES:\n
        {implications_str}
        """
        return prompt

