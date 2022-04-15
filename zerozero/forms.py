import json
import yaml

from django import forms

from zerozero import models
from zerozero.query import yaml_to_json, where_to_q
from zerozero.registry import REGISTERED_MODELS

MODEL_CHOICES = [(key, key) for key in REGISTERED_MODELS.keys()]
INTERVAL_CHOICES = [
    (None, "None"),
    (60, "1 Hour"),
    (4 * 60, "4 Hours"),
    (12 * 60, "12 Hours"),
    (24 * 60, "1 Day"),
    (24 * 7 * 60, "1 Week"),
]


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
    interval = forms.ChoiceField(choices=INTERVAL_CHOICES, required=False)

    def save(self, commit=True):
        instance = self.instance
        if instance.where:
            instance.where = yaml_to_json(instance.where)
        if instance.interval == "":
            instance.interval = None
        return super(QueryReportForm, self).save(commit=commit)

    class Meta:
        model = models.QueryReport
        fields = "__all__"
