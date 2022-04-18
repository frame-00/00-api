import pytest
import sys

from django.conf import settings
from django.contrib.auth import models as auth_models
from rest_framework.test import APIClient

from zerozero.tests import factories


# Need to mock this before anything else loads
client_module = type(sys)("zerozero.client")
sys.modules["zerozero.client"] = client_module


@pytest.fixture
def mock_zerozero_client():
    from zerozero import client

    client.models = []
    settings.WAREHOUSE_DATABASE_URL = "postgres:///some_db"
    return client


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


@pytest.fixture
def api_client_with_example_better_access(api_client_with_user):
    api_client, user = api_client_with_user
    permission = auth_models.Permission.objects.get_by_natural_key(
        "view_examplebetter", "test_app", "examplebetter"
    )
    user.user_permissions.add(permission)
    user.save()
    return api_client, user
