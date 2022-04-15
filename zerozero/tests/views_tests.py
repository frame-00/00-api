import pytest

from django.urls import reverse, reverse_lazy
from rest_framework.authtoken.models import Token

from zerozero import models
from zerozero.tests.factories import User, Example


@pytest.fixture
def example():
    examples = []
    examples.append(Example(char="char 000"))
    examples.append(Example(char="char 001"))
    examples.append(Example(char="char 002"))
    return examples


@pytest.fixture
def example_post_payload():
    return {
        "name": "test",
        "slug": "test",
        "model": "test_app.Example",
        "where": "char: char 001\n",
        "fields": "",
        "order": "",
        "interval": 240,
    }


@pytest.fixture
def client_with_user(client):
    user = User()
    client.force_login(user)
    return client, user


@pytest.mark.django_db
def test_token(client_with_user):
    client, user = client_with_user
    response = client.get(reverse_lazy("token-generator"))
    assert 200 == response.status_code, response.content


def test_token_without_access(client):
    response = client.get(reverse_lazy("token-generator"))
    assert 302 == response.status_code, response.content


@pytest.mark.django_db
def test_token_post(client_with_user):
    client, user = client_with_user
    response = client.post(reverse_lazy("token-generator"), follow=True)
    assert 200 == response.status_code
    tokens = Token.objects.filter(user=user)
    assert 1 == len(tokens)
    token = tokens[0]
    assert token.key in response.content.decode("utf-8")


@pytest.mark.django_db
def test_token_post_with_existing_token(client_with_user):
    client, user = client_with_user
    token = Token.objects.create(user=user)
    response = client.get(reverse_lazy("token-generator"))
    assert token.key not in response.content.decode("utf-8")
    response = client.post(reverse_lazy("token-generator"), follow=True)
    new_token = Token.objects.filter(user=user)[0]
    assert new_token.key in response.content.decode("utf-8")
    assert token.key not in response.content.decode("utf-8")
    assert token.key != new_token


@pytest.mark.django_db
def test_query_report(client_with_user):
    client, user = client_with_user
    response = client.get(reverse_lazy("create-query-report"))
    assert 200 == response.status_code


@pytest.mark.django_db
def test_query_report_post(example, example_post_payload, client_with_user):
    expected_payload = {
        "name": "test",
        "slug": "test",
        "model": "test_app.Example",
        "where": '{"char": "char 001"}',
        "interval": 240,
    }

    client, user = client_with_user
    response = client.post(
        reverse_lazy("create-query-report"),
        example_post_payload,
        follow=True,
    )

    assert 200 == response.status_code
    model_objects = models.QueryReport.objects.all()
    assert 1 == len(model_objects)
    assert (
        expected_payload.items()
        <= models.QueryReport.objects.values()[0].items()
    )

    response = client.get(
        reverse(
            "slug-query-report",
            kwargs={"slug": "test"},
        ),
    )
    # TODO: check slug, check data output, check if saved (should not be)
    assert (
        example_post_payload.items()
        <= vars(response.context_data["object"]).items()
    )
