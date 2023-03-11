from django.contrib import admin
from bootcamp.articles.models import Article, ArticleAuthor
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted
from django.conf import settings
from django.utils.html import format_html

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

@admin.register(ArticleAuthor)
class ArticleAuthorAdmin(admin.ModelAdmin):
    list_display = ("auteur", "author_article_link")
    search_fields = ["name", "username", "email"]  
    list_display_links = None
   
    def get_queryset(self, request):
        return super().get_queryset(request).filter(author__gte=1).distinct()
    
    def has_delete_permission(self, request, obj=None):
        return False

    def auteur(self, obj):
        return f'{obj.username} ({obj.name}, {obj.email})'    

    def author_article_link(self,obj):
        return self.get_link(obj)

    author_article_link.allow_tags = True
    author_article_link.short_description = "Liste des révisions de l'auteur"

    def get_link(self, obj: ArticleAuthor) -> str:
        root = settings.ADMIN_URL.replace('^','')
        url = f'/{root}{obj._meta.app_label}/article/?user__id__exact={obj.id}'
        return format_html(f'<a href="{url}">📝</a>')  