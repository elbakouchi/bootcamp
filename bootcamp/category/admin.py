from django.contrib import admin
from bootcamp.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "status")
    list_filter = ("user", "status", "timestamp")
