from django.contrib import admin
from .models import CustomUser, Student
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, OtpCodeData


# custom admin panels (altered)
class CustomStudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'student_id_number', 'campus')
class CustomAdminPanel(UserAdmin):
    # list of fields on admin
    list_display = ("email","username", "first_name", "is_hostel_manager", "is_staff")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "middle_name" 
                                         ,"last_name", "username",
                                         "phone",   
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
        (('Extra Permissions'), {'fields':(
            "is_student",
            "is_guest_house_manager",
            "is_hostel_manager",
            "is_hostel_worker",
            "is_bookmie_agent",
        )}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    # custom filter list
    list_filter = ("is_staff", "is_superuser", "is_active", "groups",'is_hostel_manager','is_hostel_worker', 'is_guest_house_manager', 'is_bookmie_agent',)

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
admin.site.register(Student, CustomStudentAdmin)
admin.site.register(OtpCodeData)

