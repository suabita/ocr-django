from django.contrib import admin
from .models import NutritionalTable
from django.utils.translation import gettext_lazy as _


@admin.register(NutritionalTable)
class NutritionalTableAdmin(admin.ModelAdmin):
    list_display = ('name', 'user')
    list_filter = ('name',)
    search_fields = ('nutrient__name',)
    
    readonly_fields = ('id',)
