from django.contrib import admin

from .models import StoreUser


@admin.register(StoreUser)
class StoreUser(admin.ModelAdmin):
        
        list_display = ['email', 'is_active', 'is_staff', 'created']
        exclude = ['password',]
        list_filter = ['is_staff', 'is_active']
        search_fields = ['email', 'username']
    