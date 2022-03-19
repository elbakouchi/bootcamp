from django.contrib.postgres.aggregates import StringAgg
from django.conf import settings


def general_context(request):
    debug_flag = settings.DEBUG
    if request.path == "/":
        is_homepage = True
    else:
        is_homepage = False
    return {"debug_flag": debug_flag, "is_homepage": is_homepage}


def article_context(request):
    print(vars(request))
    return request
    # article.
    # article.annotate(categoryName=StringAgg('demand__category__name', delimiter=','))
    # return article
