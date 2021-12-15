import json

from django import forms


class QueryForm(forms.Form):
    order = forms.JSONField()

    def __init__(self, model, query, *args, **kwargs):
        query = json.loads(query)
        data = {}
        for key, value in query.items():
            data[key] = json.dumps(value)
        self.model = model
        super().__init__(data, *args, **kwargs)
