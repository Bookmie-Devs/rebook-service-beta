from django.contrib import admin
from .models import Agent
# Register your models here.


class AgentAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                'user', 'phone', 'mobile_money', 'agent_profile_picture', 'ghana_card',
                    'is_verified','is_active',
            ),
        }),
    )
    
    list_display = ('user', 'agent_code' ,'is_verified','is_active','date_join',)




admin.site.register(Agent, AgentAdmin)