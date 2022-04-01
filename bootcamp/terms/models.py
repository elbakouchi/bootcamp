from django.db import models

from bootcamp.users.models import User


class Term(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    # blah blah


class TermsOfService(models.Model):
    term = models.ForeignKey(Term, on_delete=models.DO_NOTHING)
    agreement = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
