from django.contrib import admin
from .models import Information
from django.utils.translation import gettext_lazy as _


@admin.register(Information)
class InformationAdmin(admin.ModelAdmin):
    list_display = ('id', 'nutrient', 'type_information', 'cause_illness')
    list_filter = ('type_information', 'cause_illness')
    search_fields = ('nutrient__name', 'information', 'bibliography')
    fieldsets = (
        (None, {
            'fields': ('nutrient', 'information')
        }),
        (_('Type and Cause'), {
            'fields': ('type_information', 'cause_illness')
        }),
        (_('Additional Information'), {
            'fields': ('bibliography',)
        }),
    )
    readonly_fields = ('id',)
