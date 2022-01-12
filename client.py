import os
import sys
from typing import Any
from urllib.parse import urljoin

import requests


def authenticated_request(*args, **kwargs):
    if not TOKEN:
        raise Exception("No token exception")
    headers = {"Authorization": "Token {}".format(TOKEN)}
    kwargs["headers"] = headers
    return requests.request(*args, **kwargs)


class Model:
    def __init__(self, url: str):
        self.url = url
        response = authenticated_request("OPTIONS", self.url)
        self.metadata = response.json()

    def list(self, page: int, page_size: int = 1000):
        response = authenticated_request(
            "GET", self.url, params={"page": page, "page_size": page_size}
        )

        for data in response.json():
            yield ModelObject(data)

    def get(self, pk: Any):
        built_url = urljoin(self.url, "{}/".format(pk))
        return ModelObject(url=built_url)


class ModelObject:
    def __init__(self, **kwargs):
        self.url = kwargs["url"]
        if len(kwargs.keys()) == 1:
            response = authenticated_request("GET", self.url)
            self.data = response.json()
        else:
            self.data = kwargs


def build_client(api_root_url, token, module_name):
    client_module = sys.modules[__name__]
    client_module.TOKEN = token
    module = sys.modules[module_name]
    response = authenticated_request("GET", api_root_url)
    if response.status_code != 200:
        raise Exception(response.content)
    models = response.json()
    app_classes = {}

    class Dummy:
        pass

    for path, url in models.items():
        app_name, model_name = path.split("/")
        app = app_classes.get(app_name)
        if not app:
            app = Dummy()
            app_classes[app_name] = app
        app.__dict__[model_name] = Model(url=url)
    for app_name, app in app_classes.items():
        setattr(module, app_name, app)
