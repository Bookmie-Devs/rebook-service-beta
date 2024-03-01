from django.contrib import admin
from .models import SalesStatistics

class SalesStatModalAdmin(admin.ModelAdmin):
    list_display = ('hostel','amount_made','year')
    list_filter = ('year','hostel',)


admin.site.register(SalesStatistics, SalesStatModalAdmin)
