from django.db import models
from zerozero.registry import register

INTERVAL_CHOICES = [
    (None, "Never"),
    (60, "1 Hour"),
    (4 * 60, "4 Hours"),
    (12 * 60, "12 Hours"),
    (24 * 60, "1 Day"),
    (24 * 7 * 60, "1 Week"),
]


class QueryReport(models.Model):
    name = models.CharField(unique=True, max_length=255)
    slug = models.SlugField(unique=True)
    model = models.CharField(max_length=255)
    fields = models.JSONField(blank=True, null=True, default=[])
    order = models.JSONField(blank=True, null=True, default=[])
    where = models.JSONField(blank=True, null=True, default={})
    interval = models.IntegerField(
        blank=True, null=True, choices=INTERVAL_CHOICES
    )


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
