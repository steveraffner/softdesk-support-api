from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle User
    """
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Informations RGPD', {
            'fields': ('birth_date', 'can_be_contacted', 'can_data_be_shared')
        }),
        ('Métadonnées', {
            'fields': ('created_time', 'updated_time')
        }),
    )
    
    readonly_fields = ('created_time', 'updated_time')
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'age', 'is_staff')
    list_filter = BaseUserAdmin.list_filter + ('can_be_contacted', 'can_data_be_shared')
    
    def age(self, obj):
        return obj.age
    age.short_description = 'Âge'
