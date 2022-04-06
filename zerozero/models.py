from django.db import models


class QueryReport(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)
    model = models.CharField(max_length=255)
    fields = models.TextField(blank=True, null=True)
    order = models.TextField(blank=True, null=True)
    where = models.TextField(blank=True, null=True)
