import json
import yaml

from django import forms


class QueryForm(forms.Form):
    order = forms.JSONField()  # needs futher validation(list of django lookups

    def __init__(self, model, query, *args, **kwargs):
        query = yaml.safe_load(query)
        data = {}
        for key, value in query.items():
            data[key] = json.dumps(value)
        self.model = model
        super().__init__(data, *args, **kwargs)
