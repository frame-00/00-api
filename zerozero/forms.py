import json
import yaml

from django import forms

from zerozero import models
from zerozero.query import load_yaml, where_to_q
from zerozero.registry import REGISTERED_MODELS

MODEL_CHOICES = [(key, key) for key in REGISTERED_MODELS.keys()]


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


class QueryReportForm(forms.ModelForm):
    model = forms.ChoiceField(choices=MODEL_CHOICES, required=True)

    # needs futher validation (list of django lookups)
    fields = forms.CharField(required=False, widget=forms.Textarea)
    order = forms.CharField(required=False, widget=forms.Textarea)
    where = forms.CharField(required=False, widget=forms.Textarea)

    def clean_where(self):
        where = self.cleaned_data.get("where", None)
        if where != None:
            where = load_yaml(where)
            return where

    def clean_fields(self):
        fields = self.cleaned_data.get("fields", None)
        if fields != None:
            fields = load_yaml(fields)
            return fields

    def clean_order(self):
        order = self.cleaned_data.get("order", None)
        if order != None:
            order = load_yaml(order)
            return order

    class Meta:
        model = models.QueryReport
        fields = "__all__"
