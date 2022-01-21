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
