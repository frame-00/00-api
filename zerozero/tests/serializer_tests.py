import pytest


from rest_framework.serializers import (
    IntegerField,
    CharField,
    HyperlinkedIdentityField,
)


from zerozero import serializers
from test_app import models


@pytest.mark.django_db
def test_zerozero_serializer():
    expected_field_names = {"url", "char"}
    expected_view_name = "test_app_example-detail"
    ExampleSerializer = serializers.ZeroZeroSerializer(model=models.Example)
    fields = ExampleSerializer().fields
    assert expected_field_names == set(fields.keys())
    assert isinstance(fields["char"], CharField)
    assert isinstance(fields["url"], HyperlinkedIdentityField)
    assert expected_view_name == fields["url"].view_name
