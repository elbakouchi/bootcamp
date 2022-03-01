import graphene

from graphene_django.types import DjangoObjectType

from bootcamp.articles.models import Article, ArticleQuerySet
from bootcamp.helpers import paginate_data


class ArticleType(DjangoObjectType):
    """DjangoObjectType to access the Article model."""

    count_thread = graphene.Int()
    count_likers = graphene.Int()

    class Meta:
        model = Article
    '''
    
    def resolve_count_thread(self, info, **kwargs):
        return self.get_thread().count()

    def resolve_count_likers(self, info, **kwargs):
        return self.get_likers().count()

    def resolve_get_thread(self, info, **kwargs):
        return self.get_thread()

    def resolve_get_likers(self, info, **kwargs):
        return self.get_likers()
    '''


class PaginatedArticlesType(graphene.ObjectType):
    """A paginated type generic object to provide pagination to the articles
    graph."""

    page = graphene.Int()
    pages = graphene.Int()
    has_next = graphene.Boolean()
    has_prev = graphene.Boolean()
    objects = graphene.List(ArticleType)


class ArticleQuery(object):
    all_articles = graphene.List(ArticleType)
    paginated_articles = graphene.Field(PaginatedArticlesType, page=graphene.Int())
    articles = graphene.Field(ArticleType, uuid_id=graphene.String())

    def resolve_all_articles(self, info, **kwargs):
        return Article.objects.get_published()

    def resolve_paginated_articles(self, info, page):
        """Resolver functions to query the objects and turn the queryset into
        the PaginatedType using the helper function"""
        page_size = 30
        qs = Article.objects.get_published()
        return paginate_data(qs, page_size, page, PaginatedArticlesType)

    def resolve_article(self, info, **kwargs):
        slug = kwargs.get("slug")

        if slug is not None:
            return Article.objects.get(slug=slug)

        return None


class ArticleMutation(graphene.Mutation):
    """Mutation to create article objects on an effective way."""

    class Arguments:
        content = graphene.String()
        user = graphene.ID()
        parent = graphene.ID()

    content = graphene.String()
    user = graphene.ID()
    parent = graphene.ID()
    article = graphene.Field(lambda: Article)

    def mutate(self, **kwargs):
        print(kwargs)
