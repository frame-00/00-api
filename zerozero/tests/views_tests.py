import pytest
from django.urls import reverse_lazy
from rest_framework.authtoken.models import Token

from zerozero.tests.factories import User


@pytest.fixture
def client_with_user(client):
    user = User()
    client.force_login(user)
    return client, user


@pytest.mark.django_db
def test_token_view(client_with_user):
    client, user = client_with_user
    response = client.get(reverse_lazy("token-generator"))
    assert 200 == response.status_code, response.content


def test_token_view_without_access(client):
    response = client.get(reverse_lazy("token-generator"))
    assert 302 == response.status_code, response.content


@pytest.mark.django_db
def test_token_view_post(client_with_user):
    client, user = client_with_user
    response = client.post(reverse_lazy("token-generator"), follow=True)
    assert 200 == response.status_code
    tokens = Token.objects.filter(user=user)
    assert 1 == len(tokens)
    token = tokens[0]
    assert token.key in response.content.decode("utf-8")


@pytest.mark.django_db
def test_token_view_post_with_existing_token(client_with_user):
    client, user = client_with_user
    token = Token.objects.create(user=user)
    response = client.post(reverse_lazy("token-generator"), follow=True)
    assert token.key not in response.content.decode("utf-8")
    # test token changes after that
    new_token = Token.objects.filter(user=user)[0]
    assert token.key != new_token
    response = client.post(reverse_lazy("token-generator"), follow=True)
    assert new_token.key not in response.content.decode("utf-8")
