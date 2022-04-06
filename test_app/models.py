from django.db import models

from zerozero.registry import register


class Example(models.Model):
    char = models.CharField(max_length=10)
    excluded_field = models.CharField(max_length=10)


register(Example, {"exclude": ["excluded_field"]})


class ExamplesChild(models.Model):
    parent = models.ForeignKey(
        Example,
        on_delete=models.CASCADE,
        related_name="children",
        related_query_name="children",
    )


register(ExamplesChild)


class ExampleM2M(models.Model):
    has_many = models.ManyToManyField(
        Example, related_name="examplem2ms", related_query_name="examplem2ms"
    )


register(ExampleM2M)


# model for testing queryset filtering in reports page
class ExampleBetter(models.Model):
    char1 = models.CharField(max_length=10)
    char2 = models.CharField(max_length=10)
    char3 = models.CharField(max_length=10)
    char4 = models.CharField(max_length=10)


register(ExampleBetter)
