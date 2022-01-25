import pytest

from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient

from zerozero.tests import factories


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_client_with_user(django_db_blocker, api_client):
    user = factories.User()
    api_client.force_authenticate(user=user)
    return api_client, user


@pytest.fixture
def api_client_with_example_access(api_client_with_user):
    api_client, user = api_client_with_user
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_example", "test_app", "example"
    )
    user.user_permissions.add(permission)
    user.save()
    return api_client, user


@pytest.fixture
def api_client_with_examples_child_access(api_client_with_user):
    api_client, user = api_client_with_user
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_exampleschild", "test_app", "exampleschild"
    )
    user.user_permissions.add(permission)
    user.save()
    return api_client, user
