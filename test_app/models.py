from django.db import models

from zerozero.registry import register


class Example(models.Model):
    char = models.CharField(max_length=10)


register(Example)


class ExamplesChild(models.Model):
    parent = models.ForeignKey(Example, on_delete=models.CASCADE)


class ExampleM2M(models.Model):
    has_many = models.ManyToManyField(Example)
