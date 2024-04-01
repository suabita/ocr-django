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

from processing.process_main import ProcessingMain
from processing.image_preprocessing import ImagePreprocessing
from processing.ocr_processing import OcrProcessing


user = User.objects.filter(username="klacunas71").last()
nutritional = NutritionalTable.objects.last()

# ProcessingMain(user).run()
# ImagePreprocessing(nutritional).run()
OcrProcessing().run()