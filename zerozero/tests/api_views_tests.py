import pytest
import json
import csv

from io import StringIO

from rest_framework.serializers import IntegerField, CharField

from django.forms.models import model_to_dict


from zerozero import api_views
from test_app import models

from rest_framework.test import APIClient
from django.urls import reverse
from django.forms.models import model_to_dict
from django.contrib.auth import models as auth_models
from zerozero.tests import factories


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_zerozero_viewset():
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


@pytest.mark.django_db
def test_zerozero_list_view(api_client):
    user = factories.User()
    expected_count = 10
    expected_columns = ["url", "char"]
    examples = factories.Example.create_batch(expected_count)
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse("test_app_example-list")
    response = api_client.get(url)
    assert 200 == response.status_code, response.content
    response_json = json.loads(response.content)
    assert expected_count == len(response_json["results"])
    assert set(expected_columns) == set(response_json["results"][0].keys())


@pytest.mark.django_db
def test_zerozero_list_view_as_csv(api_client):
    user = factories.User()
    expected_count = 10
    expected_columns = [
        "id",
        "char",
        "excluded_field",
    ]  # TODO: remove excluded field
    examples = factories.Example.create_batch(expected_count)
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse("test_app_example-list")
    response = api_client.get(url, {"format": "csv"})
    assert 200 == response.status_code, response.content
    response_csv = list(
        csv.reader(response.content.decode("utf-8").splitlines(), delimiter=",")
    )
    assert expected_count + 1 == len(response_csv)
    assert set(expected_columns) == set(response_csv[0])


@pytest.mark.django_db
def test_zerozero_list_view_with_parent(api_client):
    user = factories.User()
    expected_count = 10
    expected_columns = ["url", "parent"]
    examples = factories.ExamplesChild.create_batch(expected_count)
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_exampleschild", "test_app", "exampleschild"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse("test_app_exampleschild-list")
    response = api_client.get(url)
    assert 200 == response.status_code, response.content
    response_json = json.loads(response.content)
    assert expected_count == len(response_json["results"])
    assert set(expected_columns) == set(response_json["results"][0].keys())


@pytest.mark.django_db
def test_zerozero_list_view_with_order(api_client):
    user = factories.User()
    expected_count = 9
    parameters = {
        "query": json.dumps(
            {
                "order": [
                    "-char",
                ]
            }
        )
    }
    examples = factories.Example.create_batch(
        expected_count
    )  # all start char values startwith with char
    expected_count += 2  # to account for the next two
    first_example = model_to_dict(factories.Example.create(char="dhar 99"))
    last_example = model_to_dict(factories.Example.create(char="bhar 99"))
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse("test_app_example-list")
    response = api_client.get(url, parameters)
    response_json = json.loads(response.content)
    assert 200 == response.status_code, response.content
    assert expected_count == len(response_json["results"])
    # TODO: make this way less terrible
    first_result = response_json["results"][0]
    last_result = response_json["results"][-1]
    first_result["id"] = int(first_result["url"].split("/")[-2])
    last_result["id"] = int(last_result["url"].split("/")[-2])
    del first_result["url"]
    del last_result["url"]
    del first_example["excluded_field"]
    del last_example["excluded_field"]
    assert first_example == first_result
    assert last_example == last_result


@pytest.mark.django_db
def test_zerozero_create_view(api_client):
    expected_example = {"char": "test", "excluded_field": ""}
    user = factories.User()
    permission = auth_models.Permission.objects.get_by_natural_key(
        "add_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse("test_app_example-list")
    response = api_client.post(url, expected_example)
    assert 201 == response.status_code, response.content
    response_json = json.loads(response.content)
    examples = models.Example.objects.all()
    assert 1 == examples.count()
    create_values = examples.values()[0]
    del create_values["id"]
    assert expected_example == create_values


@pytest.mark.django_db
def test_zerozero_update_view(api_client):
    expected_example = {"char": "test"}
    example = factories.Example()
    user = factories.User()
    permission = auth_models.Permission.objects.get_by_natural_key(
        "change_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse(
        "test_app_example-detail",
        args=[
            example.pk,
        ],
    )
    response = api_client.put(url, expected_example)
    assert 200 == response.status_code, response.content
    response_json = json.loads(response.content)
    examples = models.Example.objects.all()
    assert 1 == examples.count()
    create_values = examples.values()[0]
    del create_values["id"]
    del create_values["excluded_field"]
    assert expected_example == create_values


@pytest.mark.django_db
def test_zerozero_partial_update_view(api_client):
    expected_example = {"char": "test"}
    example = factories.Example()
    user = factories.User()
    permission = auth_models.Permission.objects.get_by_natural_key(
        "change_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse(
        "test_app_example-detail",
        args=[
            example.pk,
        ],
    )
    response = api_client.patch(url, expected_example)
    assert 200 == response.status_code, response.content
    response_json = json.loads(response.content)
    examples = models.Example.objects.all()
    assert 1 == examples.count()
    create_values = examples.values()[0]
    del create_values["id"]
    del create_values["excluded_field"]
    assert expected_example == create_values


@pytest.mark.django_db
def test_zerozero_delete_view(api_client):
    example = factories.Example()
    user = factories.User()
    permission = auth_models.Permission.objects.get_by_natural_key(
        "delete_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    api_client.force_authenticate(user=user)
    url = reverse(
        "test_app_example-detail",
        args=[
            example.pk,
        ],
    )
    response = api_client.delete(url)
    assert 204 == response.status_code, response.content
    examples = models.Example.objects.all()
    assert 0 == examples.count()
