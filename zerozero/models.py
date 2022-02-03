from django.db import models
from zerozero.registry import REGISTERED_MODELS

MODEL_CHOICES = [(key, key) for key in REGISTERED_MODELS.keys()]


class QueryReport(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField()
    model = models.CharField(choices=MODEL_CHOICES, max_length=255)
    fields = models.JSONField(blank=True)
    order = models.JSONField(blank=True)
    where = models.JSONField(blank=True)
