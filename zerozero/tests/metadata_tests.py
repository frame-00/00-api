import pytest
import json

from django.urls import reverse


@pytest.mark.django_db
def test_metadata_example(api_client_with_examples_child_access):
    api_client, user = api_client_with_examples_child_access
    url = reverse("test_app.ExamplesChild-list")
    fields = {
        "url": {
            "name": "url",
            "type": "relation",
            "json_type": "string",
            "required": False,
            "read_only": True,
            "related_url": "http://testserver/zerozero/api/test_app.ExamplesChild/",
            "related_name": "test_app.ExamplesChild",
        },
        "parent": {
            "name": "parent",
            "type": "relation",
            "json_type": "string",
            "required": True,
            "read_only": False,
            "related_url": "http://testserver/zerozero/api/test_app.Example/",
            "related_name": "test_app.Example",
        },
    }
    response = api_client.options(url)
    assert 200 == response.status_code, response.content
    response_json = json.loads(response.content)
    assert "test_app.ExamplesChild" == response_json["name"]
    assert fields == response_json["fields"]


@pytest.mark.django_db
def test_metadata_example_better(api_client_with_example_better_access):
    api_client, user = api_client_with_example_better_access
    url = reverse("test_app.ExampleBetter-list")
    fields = {
        "url": {
            "name": "url",
            "type": "relation",
            "json_type": "string",
            "required": False,
            "read_only": True,
            "related_url": "http://testserver/zerozero/api/test_app.ExampleBetter/",
            "related_name": "test_app.ExampleBetter",
        },
        "char1": {
            "name": "char1",
            "type": "text",
            "json_type": "string",
            "required": True,
            "read_only": False,
        },
        "char2": {
            "name": "char2",
            "type": "text",
            "json_type": "string",
            "required": True,
            "read_only": False,
        },
        "char3": {
            "name": "char3",
            "type": "text",
            "json_type": "string",
            "required": True,
            "read_only": False,
        },
        "char4": {
            "name": "char4",
            "type": "text",
            "json_type": "string",
            "required": True,
            "read_only": False,
        },
        "json_blob": {
            "name": "json_blob",
            "type": "json",
            "json_type": "object",
            "required": False,
            "read_only": False,
        },
    }
    response = api_client.options(url)
    assert 200 == response.status_code, response.content
    response_json = json.loads(response.content)
    assert "test_app.ExampleBetter" == response_json["name"]
    assert fields == response_json["fields"]
