from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


# custom admin panel (altered)
class CustomAdminPanel(UserAdmin):
    # list of fields on admin
    list_display = ("email","username", "student_id", "first_name", "is_hostel_manager", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "middle_name" 
                                         ,"last_name", "username",
                                         "campus","student_id",
                                         "phone",   
                                         "college",
                                         "gender")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_hostel_manager",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    # custom filter list
    list_filter = ("is_staff", "is_superuser", "is_active", "groups",'is_hostel_manager',)

    # custom search_fields
    search_fields = ("username", "first_name", "last_name", "email",'student_id',)

## custom add fieldset for custom admin
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("first_name", "middle_name",
                           "last_name", "email", "password1",
                             "password2", "campus",
                             "student_id", "gender",
                             "is_active", "is_staff",
                            "is_superuser","groups",
                            "user_permissions",
                            "is_hostel_manager"
                             ),
            },
        ),
    )

admin.site.register(CustomUser, CustomAdminPanel)