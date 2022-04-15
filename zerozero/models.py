from django.db import models
from zerozero.registry import register


class QueryReport(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)
    model = models.CharField(max_length=255)
    fields = models.TextField(blank=True, null=True)
    order = models.TextField(blank=True, null=True)
    where = models.TextField(blank=True, null=True)
    interval = models.IntegerField(blank=True, null=True)


register(QueryReport)


class QueryReportLog(models.Model):
    report = models.ForeignKey(
        QueryReport,
        on_delete=models.SET_NULL,
        related_name="logs",
        related_query_name="logs",
        null=True,
    )
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)
    success = models.BooleanField(null=True)
    error = models.TextField(blank=True, null=True)


register(QueryReportLog)
