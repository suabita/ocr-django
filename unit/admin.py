from django.contrib import admin
from .models import Unit
from django.utils.translation import gettext_lazy as _

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('slug',)
