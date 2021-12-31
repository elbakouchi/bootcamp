from django.contrib import admin
from bootcamp.demand.models import Demand


@admin.register(Demand)
class DemandAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "status")
    list_filter = ("user", "status", "timestamp")
