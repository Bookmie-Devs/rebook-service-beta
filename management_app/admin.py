from django.contrib import admin
from .models import SalesStatistics, Worker

class SalesStatModalAdmin(admin.ModelAdmin):
    list_display = ('hostel','amount_made','year')
    list_filter = ('year','hostel',)


class WorkersModalAdmin(admin.ModelAdmin):
    list_display = ('hostel','user','is_active')
    list_filter = ('is_active',)


admin.site.register(SalesStatistics, SalesStatModalAdmin)

admin.site.register(Worker, WorkersModalAdmin)