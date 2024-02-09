from django.contrib import admin
from .models import Nutrient
from django.utils.translation import gettext_lazy as _

@admin.register(Nutrient)
class NutrientAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('slug',)
