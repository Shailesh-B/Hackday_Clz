from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import College, Department, Semester, Attendence, Routine, Assignment, Club, Event, Discussion
CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password','first_name','last_name','semester','is_teacher')}),
        ('Permissions', {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Dates', {'fields': ('last_login', 'date_joined')})
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_teacher',)}
         ),
    )
    list_display_links = ("email", "username",)
    list_display = ['email', 'username', ]


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register([College, Department, Semester,
                    Attendence, Routine, Assignment, Club, Event, Discussion])
