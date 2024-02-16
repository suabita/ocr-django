from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from nutritional_table import utils


class NutritionalTable(models.Model):
    user = models.ForeignKey('authentication.User', verbose_name=_('user'), on_delete=models.CASCADE,
                                related_name='user_nutritionaltable_set')
    recommendations = models.JSONField(_('recommendations'), null=True, blank=True, default=dict)
    ocr_data = models.JSONField(_('ocr data'), null=True, blank=True, default=dict)    
    file_table = models.FileField(_('file table'), upload_to=utils.upload_user_file,
                                            null=True,
                                            blank=True,
                                            validators=[utils.validate_file])
    name = models.CharField(_('nutrient name'), max_length=100, unique=True)



    class Meta:
        verbose_name = _('Nutritional table')
        verbose_name_plural = _('Nutritional tables')