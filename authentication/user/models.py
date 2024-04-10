from django.contrib.auth.models import AbstractUser
from django.core.validators import validate_email
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from decimal import Decimal

class GenderChoices(models.IntegerChoices):
    FEMALE = 0, _("Femenino")
    MALE = 1, _("Masculino")


class PhysiologicalChoices(models.IntegerChoices):
    PREGNANCY = 0, _("Embarazo")
    BREASTFEEDING = 1, _("Lactancia")
    NOTAPPLY = 2, _("No aplica")


class PhysicalActivityChoices(models.IntegerChoices):
    SEDENTARY = 0, _("Sedentario (poco o nada de ejercicio + trabajo de escritorio)")
    LIGHTLY_ACTIVE = 1, _("Ligeramente activo (ejercicio ligero 1-3 días / semana)")
    MODERATELY_ACTIVE = 2, _("Moderadamente activo (ejercicio moderado 3-5 días / semana)")
    VERY_ACTIVE = 3, _("Muy activo (ejercicio pesado 6-7 días / semana)")
    EXTREMELY_ACTIVE = 4, _("Extremadamente activo (entrenamiento extenuante 2x / día)")

class ObjectiveChoices(models.IntegerChoices):
    KEEP = 0, _("Mantener el peso")
    LOSE = 1, _("Perder peso")
    GAIN = 2, _("Ganar peso")


class User(AbstractUser):

    height = models.PositiveIntegerField(_('altura cm'), null=True, blank=True, validators=[MinValueValidator(0)])
    weight = models.DecimalField(_('peso kg'), max_digits=14, decimal_places=2, validators=[MinValueValidator(0)],
                                    default=Decimal('0.0'))
    sex = models.PositiveSmallIntegerField(_('genero'), choices=GenderChoices.choices, null=True, blank=True, default=GenderChoices.FEMALE)
    age = models.DecimalField(_('edad'), null=True, blank=True, max_digits=14, decimal_places=2, validators=[MinValueValidator(0)],
                                    default=Decimal('0.0'))
    physiological_state = models.PositiveSmallIntegerField(_('estado'), choices=PhysiologicalChoices.choices, null=True, blank=True, default=PhysiologicalChoices.NOTAPPLY)
    physical_activity = models.PositiveSmallIntegerField(_('nivel de actividad física'), choices=PhysicalActivityChoices.choices, null=True, blank=True, default=PhysicalActivityChoices.SEDENTARY)
    objective = models.PositiveSmallIntegerField(_('objetivo'), choices=ObjectiveChoices.choices, null=True, blank=True, default=ObjectiveChoices.KEEP)


    def __str__(self):
        return str(self.email)


    def get_bucket_path(self):
        return 'media/users/%s/' % self.id

    def get_truncated_name(self):
        """Return the short name for the user."""
        full_name = '%s %s' % (self.first_name.split()[0], self.last_name.split()[0])
        return full_name.strip()