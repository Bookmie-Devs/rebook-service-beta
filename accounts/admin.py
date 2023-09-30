from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


# custom admin panel (altered)
class CustomAdminPanel(UserAdmin):
    # list of fields on admin
    list_display = ("email","username", "student_id", "first_name", "is_staff")

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
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

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
                             ),
            },
        ),
    )

admin.site.register(CustomUser, CustomAdminPanel)