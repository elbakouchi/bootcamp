from dal import autocomplete
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView

from taggit.models import Tag

from bootcamp.articles.models import Article
from bootcamp.demand.models import Demand
from bootcamp.news.models import News
from bootcamp.helpers import ajax_required
from bootcamp.qa.models import Question


class SearchListView(LoginRequiredMixin, ListView):
    """CBV to contain all the search results"""

    model = News
    template_name = "search/search_results.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        query = self.request.GET.get("query")
        context["active"] = "news"
        context["hide_search"] = True
        context["tags_list"] = Tag.objects.filter(name=query)
        context["news_list"] = News.objects.filter(
            content__icontains=query, reply=False
        ).distinct()
        context["articles_list"] = Article.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query),
            status="P",
        ).distinct()
        context["questions_list"] = Question.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        ).distinct()
        context["users_list"] = (
            get_user_model()
                .objects.filter(Q(username__icontains=query) | Q(name__icontains=query))
                .distinct()
        )
        context["news_count"] = context["news_list"].count()
        context["articles_count"] = context["articles_list"].count()
        context["questions_count"] = context["questions_list"].count()
        context["users_count"] = context["users_list"].count()
        context["tags_count"] = context["tags_list"].count()
        context["total_results"] = (
                context["news_count"]
                + context["articles_count"]
                + context["questions_count"]
                + context["users_count"]
                + context["tags_count"]
        )
        return context


# For autocomplete suggestions
@login_required
@ajax_required
def get_suggestions(request):
    # Convert users, articles, questions objects into list to be
    # represented as a single list.
    query = request.GET.get("term", "")
    users = list(
        get_user_model().objects.filter(
            Q(username__icontains=query) | Q(name__icontains=query)
        )
    )
    articles = list(
        Article.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query),
            status="P",
        )
    )
    questions = list(
        Question.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(tags__name__icontains=query)
        )
    )
    # Add all the retrieved users, articles, questions to data_retrieved
    # list.
    data_retrieved = users
    data_retrieved.extend(articles)
    data_retrieved.extend(questions)
    results = []
    for data in data_retrieved:
        data_json = {}
        if isinstance(data, get_user_model()):
            data_json["id"] = data.id
            data_json["label"] = data.username
            data_json["value"] = data.username

        if isinstance(data, Article):
            data_json["id"] = data.id
            data_json["label"] = data.title
            data_json["value"] = data.title

        if isinstance(data, Question):
            data_json["id"] = data.id
            data_json["label"] = data.title
            data_json["value"] = data.title

        results.append(data_json)

    return JsonResponse(results, safe=False)


class DemandAutocomplete(autocomplete.Select2ListView):
    '''
    def autocomplete_results(self, results):
        # print(results)
        """Return list of strings that match the autocomplete query."""
        if all(isinstance(el, list) for el in results) and len(results) > 0:
            return [[x, y] for [x, y] in results if self.q.lower() == y.lower()]
        if all(isinstance(el, tuple) for el in results) and len(results) > 0:
            return [[x, y] for (x, y) in results if self.q.lower() == y.lower()]
        else:
            return [x for x in results if self.q.lower() == x.lower()]

    def results(self, results):
        """Return the result dictionary."""
        if all(isinstance(el, list) for el in results) and len(results) > 0:
            return [dict(id=x, text=y) for [x, y] in results]
        elif all(isinstance(el, tuple) for el in results) and len(results) > 0:
            return [dict(id=x, text=y) for (x, y) in results]
        else:
            return [dict(id=x, text=x) for x in results]
    '''
    def get_list(self):
        self.q = self.request.GET.get('term', '')
        # print(self.q)
        _dump = []
        tokens = Demand.objectz.get_published().values_list('tokens')
        for words in tokens:
            try:
                _dump.extend([w.lower() for w in words[0].split(',') if len(w) > 2])
            except Exception as e:
                print(e)
                continue
        return sorted(set(_dump))


class DemandAutocomplete2(autocomplete.Select2QuerySetView):
    template = 'demand/demand_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        if q:
            qs = Demand.objectz.get_published().filter(title__exact=q, content__exact=q)
            return qs
        return Demand.objectz.none()


class SearchDemands(ListView):
    model = Demand
    paginate_by = 5
    context_object_name = "demands"
    template_name = 'redico/search_demand_list.html'

    def get_queryset(self):
        q = self.request.GET.get('q', None)
        if q:
            qs = Demand.objectz.search(q)
            return qs
        return Demand.objectz.none()
