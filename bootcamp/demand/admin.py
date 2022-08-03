from django.contrib import admin
from bootcamp.demand.models import Demand
from bootcamp.articles.models import Article
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted


class RevisionInline(admin.TabularInline):
    exclude = ['user', 'slug', 'status']
    extra = 1
    model = Article
    can_delete = False
    show_change_link = True


@admin.register(Demand)
class DemandAdmin(SafeDeleteAdmin):
    inlines = [RevisionInline]
    list_display = (highlight_deleted, "highlight_deleted_field", "title", "user", "status", "verified", "has_revision") \
                   + SafeDeleteAdmin.list_display
    list_filter = ("user", "status", "timestamp", "verified", "has_revision", SafeDeleteAdminFilter,) \
                  + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"

    def queryset(self, request):
        return self.model.object


DemandAdmin.highlight_deleted_field.short_description = DemandAdmin.field_to_highlight
