import graphene

from bootcamp.news.schema import NewsQuery
from bootcamp.users.schema import UserQuery
from bootcamp.articles.schema import ArticleQuery


class Query(NewsQuery, UserQuery, ArticleQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass


schema = graphene.Schema(query=Query)
