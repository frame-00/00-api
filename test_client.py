import json
import os
import sys
from unittest import mock

import pytest
from requests.models import Response

from client import Model, ModelObject, build_client

expected_root_url = "http://localhost:8000/zerozero/api/"
expected_example_list = "http://localhost:8000/zerozero/api/test_app/example/"
expected_example_child_list = (
    "http://localhost:8000/zerozero/api/test_app/exampleschild/"
)
expected_detail_url = "http://localhost:8000/zerozero/api/test_app/example/1/"
expected_detail_data = {
    "url": "http://localhost:8000/zerozero/api/test_app/example/1/",
    "char": "bar",
}
pk = 1


def mock_response_json(content, status):
    mock_response = Response()
    mock_response.status_code = 200
    mock_response._content = str.encode(json.dumps(content))
    return mock_response


@pytest.fixture
def set_token():
    client_module = sys.modules["client"]
    client_module.TOKEN = "test-token"
    yield client_module.TOKEN
    client_module.TOKEN = None


def test_model_object_with_url_only(set_token):
    mock_response = mock_response_json(
        {
            "url": expected_detail_url,
            "char": "bar",
        },
        200,
    )

    with mock.patch("client.authenticated_request") as ar:
        ar.return_value = mock_response
        example = ModelObject(url=expected_detail_url)
        ar.assert_called_with("GET", expected_detail_url)
    assert expected_detail_url == example.url
    assert expected_detail_data == example.data


def test_model_get(set_token):
    mock_response = mock_response_json(
        {
            "url": expected_detail_url,
            "char": "bar",
        },
        200,
    )
    with mock.patch("client.authenticated_request") as ar:
        ar.return_value = mock_response
        Example = Model(url=expected_example_list)
        ar.assert_called_with("OPTIONS", expected_example_list)

    with mock.patch("client.authenticated_request") as ar:
        ar.return_value = mock_response
        example = Example.get(pk)
        ar.assert_called_with("GET", expected_detail_url)
    assert isinstance(example, ModelObject)
    assert expected_detail_url == example.url
    assert expected_detail_data == example.data


def test_model_object_with_data(set_token):
    """Test if ModelObject has dataset does not call the server"""
    example = ModelObject(**expected_detail_data)
    assert expected_detail_url == example.url
    assert expected_detail_data == example.data


def test_model(set_token):
    mock_response = mock_response_json(
        {
            "url": expected_detail_url,
            "char": "bar",
        },
        200,
    )

    with mock.patch("client.authenticated_request") as ar:
        ar.return_value = mock_response
        Example = Model(url=expected_example_list)
        ar.assert_called_with("OPTIONS", expected_example_list)

    assert expected_example_list == Example.url


def test_model_list(set_token):
    mock_response = mock_response_json(
        [
            {
                "url": "http://localhost:8000/zerozero/api/test_app/example/1/",
                "char": "bar",
            },
            {
                "url": "http://localhost:8000/zerozero/api/test_app/example/2/",
                "char": "baz",
            },
        ],
        200,
    )

    with mock.patch("client.authenticated_request") as ar:
        ar.return_value = mock_response
        Example = Model(url=expected_example_list)
        ar.assert_called_with("OPTIONS", expected_example_list)

    with mock.patch.object(ModelObject, "__init__") as init:
        init.return_value = None
        with mock.patch("client.authenticated_request") as ar:
            ar.return_value = mock_response
            examples = list(Example.list(page=1, page_size=2))
        init.assert_has_calls(
            [
                mock.call(
                    {
                        "url": "http://localhost:8000/zerozero/api/test_app/example/1/",
                        "char": "bar",
                    }
                ),
                mock.call(
                    {
                        "url": "http://localhost:8000/zerozero/api/test_app/example/2/",
                        "char": "baz",
                    }
                ),
            ],
            any_order=True,
        )
    assert len(examples) == 2


def test_build_client():
    TOKEN = "test-token"

    mock_response = mock_response_json(
        {
            "test_app/example": expected_example_list,
            "test_app/exampleschild": expected_example_child_list,
        },
        200,
    )

    with mock.patch("client.authenticated_request") as ar:
        ar.return_value = mock_response
        build_client(expected_root_url, TOKEN, __name__)
        ar.assert_called_with("OPTIONS", expected_example_child_list)

    assert expected_example_list == test_app.example.url
