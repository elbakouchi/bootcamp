from django.contrib import admin
from django.urls import path, reverse
from django.utils.html import format_html
from bootcamp.demand.models import Demand, DemandAuthor
from bootcamp.articles.models import Article
from .views import AuthorDemandsListView
from safedelete.admin import SafeDeleteAdmin, SafeDeleteAdminFilter, highlight_deleted
import logging
from django.conf import settings

class RevisionInline(admin.TabularInline):
    exclude = ['user', 'slug', 'status']
    extra = 1
    model = Article
    can_delete = False
    show_change_link = True

#class UserDemandsFilter(admin.RelatedOnlyFieldListFilter):
#    template = "admin/user_filter.html"

@admin.register(Demand)
class DemandAdmin(SafeDeleteAdmin):
    inlines = [RevisionInline]
    list_display = (highlight_deleted, "highlight_deleted_field", "title", "user", "status", "verified", "has_revision","user_link") \
                   + SafeDeleteAdmin.list_display
    list_filter = (("user", admin.RelatedOnlyFieldListFilter), "status", "timestamp", "verified", "has_revision", SafeDeleteAdminFilter,) \
                  + SafeDeleteAdmin.list_filter

    field_to_highlight = "id"
    #user_link.short_description = "User"
    #user_link.allow_tags = True 

    def queryset(self, request):
        return self.model.object


@admin.register(DemandAuthor)
class DemandAuthorAdmin(admin.ModelAdmin):
    list_display = ("auteur", "author_demands_link")
    search_fields = ["name", "username", "email"]  
    list_display_links = None
   
    def get_queryset(self, request):
        return super().get_queryset(request).filter(client__gte=1).distinct()
    
    def has_delete_permission(self, request, obj=None):
        return False

    def auteur(self, obj):
        return f'{obj.username} ({obj.name}, {obj.email})'    

    def author_demands_link(self,obj):
        return self.get_link(obj)

    author_demands_link.allow_tags = True
    author_demands_link.short_description = "Liste des demandes de l'auteur"

    def get_link(self, obj: DemandAuthor) -> str:
        root = settings.ADMIN_URL.replace('^','')
        url = f'/{root}{obj._meta.app_label}/demand/?user__id__exact={obj.id}'
        return format_html(f'<a href="{url}">📝</a>')          


DemandAdmin.highlight_deleted_field.short_description = DemandAdmin.field_to_highlight

