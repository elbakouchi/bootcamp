from django.contrib import admin
from .models import Category, Service


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "activated")
    list_filter = ("user", "activated", "timestamp")

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "activated")
    list_filter = ("user", "activated", "timestamp")


