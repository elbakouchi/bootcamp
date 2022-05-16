from django.db import models


class Keyword(models.Model):
    tokens = models.JSONField(blank=True)
