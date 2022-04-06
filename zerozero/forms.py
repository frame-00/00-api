import json
import yaml

from django import forms

from zerozero import models
from zerozero.query import where_to_q
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

    order = forms.CharField(
        required=False, widget=forms.Textarea
    )  # needs futher validation(list of django lookups
    fields = forms.CharField(
        required=False, widget=forms.Textarea
    )  # needs futher validation(list of django lookups
    where = forms.CharField(required=False, widget=forms.Textarea)

    def save(self, commit=True):
        instance = self.instance
        for field in ["where"]:
            value = getattr(instance, field)
            if value:
                temp_yaml = yaml.safe_load(value)
                setattr(instance, field, json.dumps(temp_yaml))
        return super(QueryReportForm, self).save(commit=commit)

    class Meta:
        model = models.QueryReport
        fields = "__all__"
