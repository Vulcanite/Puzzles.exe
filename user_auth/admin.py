from django.contrib import admin

# Register your models here.
# from django.contrib import admin
from .models import customuser
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email','firstname','lastname','is_staff','is_active','date_joined','role',) # add fields as you want

admin.site.register(customuser, CustomUserAdmin)
