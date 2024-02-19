from django.contrib import admin
from .models import HostelAgent
# Register your models here.


class HostelAgentAdmin(admin.ModelAdmin):
    list_display = ('user', 'campus_affiliation', 'agent_code' ,'is_verified','is_active',)




admin.site.register(HostelAgent, HostelAgentAdmin)