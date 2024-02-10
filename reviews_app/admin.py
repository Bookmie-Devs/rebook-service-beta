from django.contrib import (admin,)
from .models import (FeedBackMessage, 
                     CustomerCare, 
                     HostelLike,
                     RoomLike,
                     RecomendationFeedBacks,
                     RecomendationFeedBacks,
                     NewsletterEmails,
                     GeneralNewsLetter,
                     NewsLetterMessage,)
# Register your models here.


class FeedBackAdmin(admin.ModelAdmin):

    list_display = ('name','phone','date_sent','issue_resolved',)

    search_fields = ('name','phone','email',)

    list_filter = ('date_sent',)

# custom admin for feedback
admin.site.register(FeedBackMessage, FeedBackAdmin)


class CustomerCareAdmin(admin.ModelAdmin):
    list_display = ('name','phone','date_sent','issue_resolved',)

    search_fields = ('name','phone','email',)

    list_filter = ('date_sent','issue_resolved',)

# cutom admin for customer issues
admin.site.register(CustomerCare, CustomerCareAdmin)

class ReccomendationAdmin(admin.ModelAdmin):

    list_display = ('name','image')

admin.site.register(RecomendationFeedBacks, ReccomendationAdmin)
admin.site.register(HostelLike)
admin.site.register(RoomLike)
# MESSAGES
admin.site.register(NewsletterEmails)
admin.site.register(NewsLetterMessage)
admin.site.register(GeneralNewsLetter)
