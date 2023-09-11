from django.contrib import admin
from rest_framework.authtoken.models import Token
from .models import StoreUser


@admin.register(StoreUser)
class StoreUser(admin.ModelAdmin):
    list_display = ["email", "is_active", "is_email_confirmed", "is_staff", "created"]
    exclude = [
        "password",
    ]
    list_filter = ["is_staff", "is_email_confirmed"]
    search_fields = ["email"]
