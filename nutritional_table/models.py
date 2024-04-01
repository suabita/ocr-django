from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from nutritional_table import utils



class StatusChoices(models.IntegerChoices):
    PENDING = 0, _("Pendiente")
    SUCCESS = 1, _("Actualizado")


class NutritionalTable(models.Model):
    user = models.ForeignKey('authentication.User', verbose_name=_('user'), on_delete=models.CASCADE,
                                related_name='user_nutritionaltable_set')
    recommendations = models.JSONField(_('user response'), null=True, blank=True, default=dict)
    ocr_data = models.JSONField(_('ocr data'), null=True, blank=True, default=dict)    
    file_table = models.FileField(_('file table'), upload_to=utils.upload_user_file,
                                            null=True,
                                            blank=True,
                                            validators=[utils.validate_file])
    file_table_processed = models.FileField(_('file table processed'), upload_to=utils.upload_user_file_processed,
                                            null=True,
                                            blank=True,
                                            validators=[utils.validate_file])
    name = models.CharField(_('nutrient name'), max_length=100, unique=True)
    status = models.PositiveSmallIntegerField(_('estado'), choices=StatusChoices.choices, null=True, blank=True, default=StatusChoices.PENDING)



    class Meta:
        verbose_name = _('Nutritional table')
        verbose_name_plural = _('Nutritional tables')