from django.urls import reverse
from django.shortcuts import redirect

from bootcamp.terms.models import Term


class TermAgreeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.user.is_authenticated:
            return response
        term_date = Term.objects.last().created_at
        user_term_date = request.user.termofservice_set.filter(created_at__gte=term_date).exists()
        if not user_term_date:
            return redirect(reverse('app:terms_of_service_view') + '?next=' + request.path)
        return response
