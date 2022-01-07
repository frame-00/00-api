from unittest import mock

import pytest

from test_app.models import Example
from zerozero import api_views, registry


@pytest.fixture
def MOCK_REGISTERED_MODELS():
    backup = registry.REGISTERED_MODELS
    registry.REGISTERED_MODELS = {}
    yield
    registry.REGISTERED_MODELS = backup


def test_register(MOCK_REGISTERED_MODELS):
    model = Example
    options = None
    registry.register(model, options)
    assert {
        "test_app.example": {"model": model, "options": {}}
    } == registry.REGISTERED_MODELS
