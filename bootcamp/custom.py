from django.http import JsonResponse
from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.http import Http404
from django.template.defaultfilters import striptags
from django.utils.encoding import smart_str
from django.utils.translation import ugettext as _
from django.views.generic.base import View
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectTemplateResponseMixin
from nltk.tokenize import RegexpTokenizer
from django.conf import settings

tokenizer = RegexpTokenizer(r'\w+')
threshold = getattr(settings, 'MAX_LENGTH_WORDS_COUNT', 350)


def word_counter_validator(text: str):
    tokens = tokenizer.tokenize(striptags(text))
    if len(tokens) > threshold:
        error: str = F'Assurez-vous que ce texte ne depasse pas {threshold} mots, le texte actuel contient {len(tokens)}.'
        raise ValidationError(error)


class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """

    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        try:
            response = super(AjaxableResponseMixin, self).form_valid(form)
            if self.request.is_ajax():
                data = {
                    'pk': self.object.pk,
                }
                return JsonResponse(data)
            else:
                return response

        except Exception as e:
            print(e)
            return JsonResponse(e.__dict__, safe=False)


PAGE_LABEL = "page"


class MultipleObjectMixin(object):
    allow_empty = True
    context_object_name = None
    model = None
    queryset = None

    def get_queryset(self):
        """Get the list of items for this view.
        This must be an interable, and may be a queryset
        (in which qs-specific behavior will be enabled).
        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, '_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            msg = '{0} must define ``queryset`` or ``model``'
            raise ImproperlyConfigured(msg.format(self.__class__.__name__))
        return queryset

    def get_allow_empty(self):
        """Returns True if the view should display empty lists.
        Return False if a 404 should be raised instead.
        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """Get the name of the item to be used in the context.
        See original in ``django.views.generic.list.MultipleObjectMixin``.
        """
        if self.context_object_name:
            return self.context_object_name
        elif hasattr(object_list, 'model'):
            object_name = object_list.model._meta.object_name.lower()
            return smart_str('{0}_list'.format(object_name))
        else:
            return None

    def get_context_data(self, **kwargs):
        """Get the context for this view.
        Also adds the *page_template* variable in the context.
        If the *page_template* is not given as a kwarg of the *as_view*
        method then it is generated using app label, model name
        (obviously if the list is a queryset), *self.template_name_suffix*
        and *self.page_template_suffix*.
        For instance, if the list is a queryset of *blog.Entry*,
        the template will be ``blog/entry_list_page.html``.
        """
        queryset = kwargs.pop('object_list')
        page_template = kwargs.pop('page_template', None)

        context_object_name = self.get_context_object_name(queryset)
        context = {'object_list': queryset, 'view': self}
        context.update(kwargs)
        if context_object_name is not None:
            context[context_object_name] = queryset

        if page_template is None:
            if hasattr(queryset, 'model'):
                page_template = self.get_page_template(**kwargs)
            else:
                raise ImproperlyConfigured(
                    'AjaxListView requires a page_template')
        context['page_template'] = self.page_template = page_template

        return context


class BaseListView(MultipleObjectMixin, View):

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty and len(self.object_list) == 0:
            msg = _('Empty list and ``%(class_name)s.allow_empty`` is False.')
            raise Http404(msg % {'class_name': self.__class__.__name__})
        context = self.get_context_data(
            object_list=self.object_list, page_template=self.page_template)
        return self.render_to_response(context)


class AjaxMultipleObjectTemplateResponseMixin(MultipleObjectTemplateResponseMixin):
    key = PAGE_LABEL
    page_template = None
    page_template_suffix = '_page'
    template_name_suffix = '_list'

    def get_page_template(self, **kwargs):
        """Return the template name used for this request.
        Only called if *page_template* is not given as a kwarg of
        *self.as_view*.
        """
        opts = self.object_list.model._meta
        return '{0}/{1}{2}{3}.html'.format(
            opts.app_label,
            opts.object_name.lower(),
            self.template_name_suffix,
            self.page_template_suffix,
        )

    def get_template_names(self):
        """Switch the templates for Ajax requests."""
        request = self.request
        querystring_key = request.GET.get('querystring_key', PAGE_LABEL)
        if request.is_ajax() and querystring_key == self.key:
            return [self.page_template]
        return super(
            AjaxMultipleObjectTemplateResponseMixin, self).get_template_names()


class AjaxListView(AjaxMultipleObjectTemplateResponseMixin, ListView):
    """Allows Ajax pagination of a list of objects.
    You can use this class-based view in place of *ListView* in order to
    recreate the behaviour of the *page_template* decorator.
    For instance, assume you have this code (taken from Django docs)::
        from django.conf.urls import patterns
        from django.views.generic import ListView
        from books.models import Publisher
        urlpatterns = patterns('',
            (r'^publishers/$', ListView.as_view(model=Publisher)),
        )
    You want to Ajax paginate publishers, so, as seen, you need to switch
    the template if the request is Ajax and put the page template
    into the context as a variable named *page_template*.
    This is straightforward, you only need to replace the view class, e.g.::
        from django.conf.urls import patterns
        from books.models import Publisher
        from endless_pagination.views import AjaxListView
        urlpatterns = patterns('',
            (r'^publishers/$', AjaxListView.as_view(model=Publisher)),
        )
    NOTE: Django >= 1.3 is required to use this view.
    """
