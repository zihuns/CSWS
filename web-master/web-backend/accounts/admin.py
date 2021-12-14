from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm

class UserAdmin(BaseUserAdmin):
    #add_form = UserChangeForm
    #form = UserCreationForm

    list_display = ('uos_id', 'name', 'student_id', 'is_staff', 'is_superuser')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('uos_id', 'password')}),
        ('Personal info', {'fields': ('name', 'student_id')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')})
    )
    add_fieldsets = (
    )
    search_fields = ('student_id',)
    ordering = ('student_id',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)