from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.contrib.flatpages import views as flatpages

from graphene_django.views import GraphQLView

admin.site.site_header = 'Redico back-office'

urlpatterns = [
    url(r"^home/", include("bootcamp.home.urls", namespace="home")),
    url(r"^categories/", include("bootcamp.category.urls", namespace="categories")),
    url(r"^$", TemplateView.as_view(template_name="redico/home.html"), name="home"),
    url(r"^_categories", TemplateView.as_view(template_name="redico/categories.html"), name="_categories"),
    url(r"^apropos-de-redico", TemplateView.as_view(template_name="redico/about-redico.html"), name="about"),
    url(r"^article", TemplateView.as_view(template_name="redico/article-single.html"), name="article"),
    url(r"^articles", TemplateView.as_view(template_name="redico/liste-article.html"), name="articles"),
    url(r"^contactez-nous", TemplateView.as_view(template_name="redico/contact.html"), name="contact_us"),
    url(r"^gestion-des-cookies", TemplateView.as_view(template_name="redico/cookies.html"), name="cookies"),
    url(r"^index", TemplateView.as_view(template_name="redico/index.html"), name="index"),
    url(r"^nouveau-article", TemplateView.as_view(template_name="redico/new-article.html"), name="new_article"),
    url(r"^nos-partenaires", TemplateView.as_view(template_name="redico/partners.html"), name="partners"),
    url(r"^conditions-generales-utilisation", TemplateView.as_view(template_name="redico/privacy-policy.html"), name="privacy"),
    url(
        r"^about/$",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    # User management
    url(r"^users/", include("bootcamp.users.urls", namespace="users")),
    url(r"^accounts/", include("allauth.urls")),
    # Third party apps here
    url(r"^comments/", include("django_comments.urls")),
    url(r"^graphql", GraphQLView.as_view(graphiql=True)),
    url(r"^markdownx/", include("markdownx.urls")),
    # Local apps here
    url(
        r"^notifications/",
        include("bootcamp.notifications.urls", namespace="notifications"),
    ),
    url(r"^articles/", include("bootcamp.articles.urls", namespace="articles")),
    url(r"^news/", include("bootcamp.news.urls", namespace="news")),
    url(r"^messages/", include("bootcamp.messager.urls", namespace="messager")),
    url(r"^qa/", include("bootcamp.qa.urls", namespace="qa")),
    url(r"^search/", include("bootcamp.search.urls", namespace="search")),
    url(r'^(?P<url>.*/)$', flatpages.flatpage),

    #  url('summernote/', include('django_summernote.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development
    urlpatterns += [
        url(
            r"^400/$",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        url(
            r"^403/$",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        url(
            r"^404/$",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        url(r"^500/$", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [url(r"^__debug__/", include(debug_toolbar.urls))] + urlpatterns
