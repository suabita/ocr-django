from django.db import models
from django.utils.translation import gettext_lazy as _
from customized.mixin import SlugModelMixin


class Unit(SlugModelMixin, models.Model):
    slug = models.SlugField(unique=True, max_length=100)
    name = models.CharField(_('Unit name'), max_length=100, db_index=True, unique=True)

    def get_slug(self):
        return self.name

    def __str__(self):
        return self.name

    def clean(self):
        self.name = self.name.title()
    class Meta:
        verbose_name = _('Unit')
        verbose_name_plural = _('Units')