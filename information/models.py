from django.db import models
from django.utils.translation import gettext_lazy as _
from customized.mixin import SlugModelMixin

class TypeChoices(models.IntegerChoices):
    DEFINITION = 0, _("Definition")
    ILLNESS = 1, _("Illness")

class CauseIllnessChoices(models.IntegerChoices):
    EXCESS = 0, _("Excess")
    FAILURE = 1, _("Failure")

class Information(models.Model):
    nutrient = models.ForeignKey('nutrient.Nutrient', verbose_name=_('nutrient'), on_delete=models.CASCADE,
                                related_name='nutrient_information_set')
    information = models.TextField(_('information'), null=True, blank=True)
    type_information = models.PositiveSmallIntegerField(_('type information'), choices=TypeChoices.choices, null=True, blank=True, default=TypeChoices.DEFINITION)
    cause_illness = models.PositiveSmallIntegerField(_('cause illness'), choices=CauseIllnessChoices.choices, null=True, blank=True, default=CauseIllnessChoices.EXCESS)
    bibliography = models.TextField(_('bibliography'), null=True, blank=True)


    class Meta:
        verbose_name = _('Information')
        verbose_name_plural = _('Informations')