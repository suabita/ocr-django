from django.contrib import admin
from .models import DailyQuantity
from django.utils.translation import gettext_lazy as _


@admin.register(DailyQuantity)
class DailyQuantityAdmin(admin.ModelAdmin):
    list_display = ('nutrient', 'life_stage', 'min_age_range', 'max_age_range', 'recommendable_quantity', 'unit')
    list_filter = ('life_stage',)
    search_fields = ('nutrient__name', 'information', 'bibliography')
    fieldsets = (
        (None, {
            'fields': ('nutrient', 'information')
        }),
        (_('Age Range'), {
            'fields': ('min_age_range', 'max_age_range')
        }),
        (_('Recommendable Quantity'), {
            'fields': ('recommendable_quantity',)
        }),
        (_('Additional Information'), {
            'fields': ('life_stage', 'bibliography', 'unit')
        }),
    )
    readonly_fields = ('id',)
