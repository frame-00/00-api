import pytest

from rest_framework.serializers import IntegerField, CharField


from zerozero import api_views
from test_app import models


@pytest.mark.django_db
def test_zerozero_viewset():
    field_names = {"id", "char"}
    ExampleViewSet = api_views.ZeroZeroViewSet(model=models.Example)
    list_view = ExampleViewSet.as_view({"get": "list", "post": "create"})
    detail_view = ExampleViewSet.as_view(
        {
            "get": "retrieve",
            "put": "update",
            "patch": "partial_update",
            "delete": "destroy",
        }
    )
