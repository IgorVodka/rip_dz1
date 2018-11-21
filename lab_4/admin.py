from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from lab_4.forms import CustomUserChangeForm
from lab_4.models import User, Department, Subject, Teacher, Like


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('avatar',)}),
    )


class TeacherAdmin(admin.ModelAdmin):
    ordering = ['id']
    search_fields = ['last_name', 'first_name', 'patronymic']


admin.site.register(User, CustomUserAdmin)
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Like)
