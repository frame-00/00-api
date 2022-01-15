import json
import yaml
import operator

from django import forms
from django.db.models import Q


class QueryForm(forms.Form):
    order = forms.JSONField(
        required=False
    )  # needs futher validation(list of django lookups
    fields = forms.JSONField(
        required=False
    )  # needs futher validation(list of django lookups
    where = forms.JSONField(required=False)

    def __init__(self, model, query, *args, **kwargs):
        query = yaml.safe_load(query)
        data = {}
        for key, value in query.items():
            data[key] = json.dumps(value)
        self.model = model
        super().__init__(data, *args, **kwargs)

    def clean_where(self):
        where = self.cleaned_data.get("where", None)
        if where:
            q_expression = where_to_q(where)
            return q_expression


STRING_TO_OPERATOR = {
    "AND": operator.and_,
    "OR": operator.or_,
}
OPERATOR_STRING = list(STRING_TO_OPERATOR.keys())


def where_to_q(where):
    where_left, where_right = list(where.items())[0]
    if where_left in OPERATOR_STRING[:2]:  # AND and OR have 2 arguments
        first, second = where_right
        first_q = where_to_q(first)
        second_q = where_to_q(second)
        operator = STRING_TO_OPERATOR[where_left]
        return operator(first_q, second_q)
    if where_left == "NOT":  # OR has just 1
        return ~where_to_q(where_right)
    return Q(**where)
