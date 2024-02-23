from django.db import models
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
from django.core.validators import MinValueValidator



class LifeStageChoices(models.IntegerChoices):
    INFANT = 0, _("Infant")
    CHILD = 1, _("Child")
    FEMALE = 2, _("Female")
    MALE = 3, _("Male")
    PREGNANCY = 4, _("Pregnancy")
    BREASTFEEDING = 5, _("Breastfeeding")


class DailyQuantity(models.Model):
    nutrient = models.ForeignKey('nutrient.Nutrient', verbose_name=_('nutrient'), on_delete=models.CASCADE,
                                related_name='nutrient_dailyquantity_set')
    life_stage = models.PositiveSmallIntegerField(_('life stage'), choices=LifeStageChoices.choices, null=True, blank=True, default=LifeStageChoices.INFANT)
    max_age_range = models.DecimalField(_('maximum age range'), null=True, blank=True, max_digits=14, decimal_places=2, validators=[MinValueValidator(0)],
                                    default=Decimal('0.0'))
    min_age_range = models.DecimalField(_('minimun age range'), null=True, blank=True, max_digits=14, decimal_places=2, validators=[MinValueValidator(0)],
                                    default=Decimal('0.0'))
    recommendable_quantity = models.DecimalField(_('recommendable quantity'), null=True, blank=True, max_digits=14, decimal_places=2, validators=[MinValueValidator(0)],
                                    default=Decimal('0.0'))
    bibliography = models.TextField(_('bibliography'), null=True, blank=True)
    unit = models.ForeignKey('unit.Unit', verbose_name=_('unit'), on_delete=models.CASCADE,
                                related_name='unit_dailyquantity_set')


    class Meta:
        verbose_name = _('Daily quantity')
        verbose_name_plural = _('Daily quantities')