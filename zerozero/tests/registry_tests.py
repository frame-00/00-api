from unittest import mock

import pytest

from test_app.models import Example
from zerozero import api_views, registry


@pytest.fixture
def MOCK_REGISTERED_MODELS():
    backup = registry.REGISTERED_MODELS
    registry.REGISTERED_MODELS = []
    yield
    registry.REGISTERED_MODELS = backup


def test_register(MOCK_REGISTERED_MODELS):
    model = Example
    options = None
    registry.register(model, options)
    assert 1 == len(registry.REGISTERED_MODELS)
    assert model == registry.REGISTERED_MODELS[0]["model"]
    assert {} == registry.REGISTERED_MODELS[0]["options"]
