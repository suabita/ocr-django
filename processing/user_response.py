from nutrient.models import Nutrient
from processing.ai_recommendations import AIRecommendations
from daily_quantity.models import DailyQuantity, LifeStageChoices
from authentication.user.models import PhysiologicalChoices, GenderChoices, PhysicalActivityChoices, ObjectiveChoices
from ocrdjproject.settings import ID_FAT, ID_SUGAR, ID_CALORIES


class UserResponse:
    table_ocr_info = {}
    user = None
    new_response = False

    def __init__(self, table_info={}, user=None, new_response=False):
        self.table_ocr_info = table_info
        self.user = user
        self.new_response = new_response

    def run(self):
        print("UserResponse user", self.user)

        user_response = {}

        for nutrient_name, values in self.table_ocr_info.items():
            nutrient = Nutrient.objects.filter(name__icontains=nutrient_name).last()
            print("UserResponse nutrient qs", nutrient_name, nutrient)
            print("UserResponse nutrient values", nutrient_name, values)
            if nutrient:
                # if not self.new_response:
                if  not self.new_response and nutrient.cached_recommendations:
                    print("Se encontro cache para el nutriente...")
                    recommendations = nutrient.cached_recommendations
                else:
                    print("Consultando ChatGPT sobre el nutriente...")
                    recommendations = AIRecommendations(nutrient).run()
                    nutrient.cached_recommendations = recommendations
                    nutrient.save()
                # else:
                #     print("Consultando nuevamente ChatGPT sobre el nutriente...")
                #     recommendations = AIRecommendations(nutrient).run()


                # print("Consultando ChatGPT sobre el nutriente...")
                user_response[nutrient_name] = {
                    "concept": recommendations.get("concepto",""),
                    "implications": recommendations.get("implicaciones", ""),
                    "recommended_quantity": self.get_recommended_quantity(nutrient),
                    "ocr_quantity": values[1]
                }

                print("Output del nutriente", user_response[nutrient_name])

            else:
                print("no existe el nutriente", ascii(nutrient))


        return user_response


    def get_recommended_quantity(self, nutrient_qs):
        if self.user:
            

            if self.user.physiological_state == PhysiologicalChoices.PREGNANCY:
                life_stage_user = LifeStageChoices.PREGNANCY
            elif self.user.physiological_state == PhysiologicalChoices.BREASTFEEDING:
                life_stage_user = LifeStageChoices.BREASTFEEDING
            elif self.user.age <= 8 and self.user > 1:
                life_stage_user = LifeStageChoices.CHILD
            elif self.user.age <= 1:
                life_stage_user = LifeStageChoices.INFANT
            elif self.user.sex == GenderChoices.MALE:
                life_stage_user = LifeStageChoices.MALE
            else:
                life_stage_user = LifeStageChoices.FEMALE

            print("life_stage_user", life_stage_user)
            print("age", self.user.age)
            print("nutrient", nutrient_qs.name)

            quantity = DailyQuantity.objects.filter(nutrient_id=nutrient_qs.id,
                                                    max_age_range__gte=self.user.age,
                                                    min_age_range__lte=self.user.age,
                                                    life_stage=life_stage_user).first()
            
            if quantity:
                return "{} {}".format(quantity.recommendable_quantity,quantity.unit)
            else:
                print("nutriente id", nutrient_qs.id)
                print("settings calorias id", ID_CALORIES)
                if nutrient_qs.id == ID_CALORIES:
                    if self.user.objective == ObjectiveChoices.KEEP:
                        return str(self.get_calories()) + " Kcal"
                    elif self.user.objective == ObjectiveChoices.LOSE:
                        return str(self.get_calories() - 500) + " Kcal"
                    elif self.user.objective == ObjectiveChoices.GAIN:
                        return str(self.get_calories() + 250) + " Kcal"
                else:
                    return ""
                    
        else:
            print("no hay usuario")
            return

    def get_tmb(self):
        if self.user.sex == GenderChoices.MALE:
            tmb = 88.362 + (13.397 * float(self.user.weight)) + (4.799 * float(self.user.height)) - (5.677 * float(self.user.age))
        
        if self.user.sex == GenderChoices.FEMALE:   
            tmb = 447.593 + (9.247 * float(self.user.weight)) + (3.098 * float(self.user.height)) - (4.330 * float(self.user.age))
        
        return tmb
    
    def get_calories(self):
        tmb = self.get_tmb()

        if self.user.physical_activity == PhysicalActivityChoices.SEDENTARY:
            return tmb*1.2
        if self.user.physical_activity == PhysicalActivityChoices.LIGHTLY_ACTIVE:
            return tmb*1.375
        if self.user.physical_activity == PhysicalActivityChoices.MODERATELY_ACTIVE:
            return tmb*1.55
        if self.user.physical_activity == PhysicalActivityChoices.VERY_ACTIVE:
            return tmb*1.725
        if self.user.physical_activity == PhysicalActivityChoices.EXTREMELY_ACTIVE:
            return tmb*1.9
        
