from django.contrib import admin
from bootcamp.demand.models import Demand
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted


@admin.register(Demand)
class DemandAdmin(SafeDeleteAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "title", "user", "status", "verified", "has_revision") \
                   + SafeDeleteAdmin.list_display
    list_filter = ("user", "status", "timestamp", "verified", "has_revision", SafeDeleteAdminFilter,) \
                  + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"


DemandAdmin.highlight_deleted_field.short_description = DemandAdmin.field_to_highlight
