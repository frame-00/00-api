import pytest


from rest_framework.serializers import (
    IntegerField,
    CharField,
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ManyRelatedField,
    PrimaryKeyRelatedField,
    RelatedField,
    SlugRelatedField,
    StringRelatedField,
)


from zerozero import serializers
from test_app import models


@pytest.mark.django_db
def test_zerozero_serializer():
    expected_field_names = {"url", "char"}
    expected_view_name = "test_app.Example-detail"
    ExampleSerializer = serializers.ZeroZeroSerializer(model=models.Example)
    fields = ExampleSerializer().fields
    assert expected_field_names == set(fields.keys())
    assert isinstance(fields["char"], CharField)
    assert isinstance(fields["url"], HyperlinkedIdentityField)
    assert expected_view_name == fields["url"].view_name


@pytest.mark.django_db
def test_zerozero_serializer_with_relation():
    expected_field_names = {"url", "parent"}
    expected_view_name = "test_app.ExamplesChild-detail"
    expected_parent_view_name = "test_app.Example-detail"
    ExamplesChildSerializer = serializers.ZeroZeroSerializer(
        model=models.ExamplesChild
    )
    fields = ExamplesChildSerializer().fields
    assert expected_field_names == set(fields.keys())
    assert isinstance(fields["parent"], HyperlinkedRelatedField)
    assert isinstance(fields["url"], HyperlinkedIdentityField)
    assert expected_view_name == fields["url"].view_name
    assert expected_parent_view_name == fields["parent"].view_name


@pytest.mark.django_db
def test_zerozero_serializer_with_relation_and_depth():
    expected_field_names = {"url", "parent"}
    expected_view_name = "test_app.ExamplesChild-detail"
    ExamplesChildSerializer = serializers.ZeroZeroSerializer(
        model=models.ExamplesChild, depth=2
    )
    fields = ExamplesChildSerializer().fields
    assert expected_field_names == set(fields.keys())
    assert isinstance(fields["parent"], serializers.ZeroZeroSerializer)
    assert isinstance(fields["url"], HyperlinkedIdentityField)
    assert expected_view_name == fields["url"].view_name
