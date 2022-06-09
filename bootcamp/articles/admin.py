from django.contrib import admin
from bootcamp.articles.models import Article
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted


@admin.register(Article)
class ArticleAdmin(SafeDeleteAdmin):
    list_display = (highlight_deleted, "highlight_deleted_field", "title", "user", "status")\
                   + SafeDeleteAdmin.list_display
    list_filter = ("user", "status", "timestamp", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
    field_to_highlight = "id"


ArticleAdmin.highlight_deleted_field.short_description = ArticleAdmin.field_to_highlight

'''


 list_display = (highlight_deleted, "highlight_deleted_field", "first_name", "last_name", "email") + SafeDeleteAdmin.list_display
...    list_filter = ("last_name", SafeDeleteAdminFilter,) + SafeDeleteAdmin.list_filter
...
...    field_to_highlight = "id"
...
... ContactAdmin.highlight_deleted_field.short_description = ContactAdmin.field_to_highlight

'''