from django.db.models import Count, F, Max
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView
from bootcamp.category.models import Category
from bootcamp.category.views import CategoriesListView
from bootcamp.demand.models import Demand


class HomePageView(ListView):
    model = Demand
    paginate_by = 5
    context_object_name = "demands"
    template_name = 'redico/homepage.html'
    queryset = Demand.objectz.homepage()


class HomePageListView(ListView):
    model = Demand
    paginate_by = 10
    context_object_name = "demands"
    template_name = 'redico/homepage3.html'
    queryset = Demand.objectz.homepage()

    def get_context_data(self, *args, **kwargs):
        context = super(HomePageListView, self).get_context_data(*args, **kwargs)
        context['unfulfilled'] = Demand.objectz.get_published_unverified_demands(self.paginate_by)
        # print(context['unfulfilled'])
        return context


class HomepageView(CategoriesListView):
    template_name = 'redico/homepage.html'

    def get_context_data(self, *args, **kwargs):
        context = super(HomepageView, self).get_context_data(*args, **kwargs)
        context['categories'] = super(HomepageView, self).get_queryset(**kwargs)
        return context


def paginate2(page):
    demands = \
        Demand.objectz.get_demands_with_category_and_page_views()

    paginator = Paginator(demands, 5)

    try:
        paginated_demands = paginator.page(page)
    except PageNotAnInteger:
        paginated_demands = paginator.page(1)
    except EmptyPage:
        paginated_demands = paginator.page(paginator.num_pages)

    return paginated_demands


def paginate(page):
    demands = \
        Demand.objectz.filter(verified=True).annotate(
            categoryName=F('category__name'), last_revision=Max('revision__id')).order_by("-pk", "-timestamp")

    paginator = Paginator(demands, 5)

    try:
        paginated_demands = paginator.page(page)
    except PageNotAnInteger:
        paginated_demands = paginator.page(1)
    except EmptyPage:
        paginated_demands = paginator.page(paginator.num_pages)

    return paginated_demands


# @csrf_exempt
def feed_pagination(request):
    if request.is_ajax and request.method == 'POST':
        page = request.POST.get('page', 5)
        paginated_demands = paginate(page)
        context = {"demands": paginated_demands.object_list}
        return HttpResponse(render_to_string("redico/snippets/demand-list-item.html", context))
    else:
        return JsonResponse({}, status=400)


def homepage(request):
    page = request.GET.get('page', 1)

    paginated_demands = paginate(page)

    categories = Category.objects.filter(activated=True).annotate(posts_count=Count('demand_category'))

    try:
        return render(request, 'redico/homepage.html', {'categories': categories, 'demands': paginated_demands})
    except EmptyPage:
        return render(request, 'redico/homepage.html', {'categories': [], 'demands': Paginator([], 1)})
    except ZeroDivisionError:
        return render(request, 'redico/homepage.html', {'categories': [], 'demands': Paginator([], 1)})
