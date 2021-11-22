import pytest


from rest_framework.serializers import IntegerField, CharField


from zerozero import serializers
from test_app import models


@pytest.mark.django_db
def test_zerozero_serializer():
    field_names = {"id", "char"}
    ExampleSerializer = serializers.ZeroZeroSerializer(model=models.Example)
    fields = ExampleSerializer().fields
    assert set(fields.keys()) == field_names
    assert type(fields["id"]) == IntegerField
    assert type(fields["char"]) == CharField
