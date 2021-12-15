from django.db import transaction

from rest_framework import viewsets
from rest_framework.permissions import BasePermission
from rest_framework_csv.renderers import CSVStreamingRenderer

from zerozero.forms import QueryForm
from zerozero import serializers
from zerozero import permissions


class _ZeroZeroViewSet(viewsets.ModelViewSet):
    Model = None

    def __init__(self, *args, **kwargs):
        self.app_label = self.Model._meta.app_label
        self.model_name = self.Model._meta.model_name
        return super().__init__(*args, **kwargs)

    @property
    def paginator(self):
        """Excludes csv from being paged"""

        self._paginator = super().paginator
        if isinstance(self.request.accepted_renderer, CSVStreamingRenderer):
            self._paginator = None
        return self._paginator

    @transaction.atomic()
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        queryset = self.Model.objects.all()
        if self.action == "list":
            query = self.request.GET.get("query")
            if query:
                form = QueryForm(self.Model, query)

                if not form.is_valid():
                    raise ValidationError({"detail": form.errors})

                order = form.cleaned_data.get("order", None)

                if order != None:
                    queryset = queryset.order_by(*order)
        return queryset

    def get_serializer_class(self):
        return serializers.ZeroZeroSerializer(self.request, model=self.Model)

    def get_permissions(self):

        return [permissions.APIDefaultPermission(action=self.action)]


class ZeroZeroViewSet(viewsets.ModelViewSet):
    def __new__(cls, *args, **kwargs):

        ModelValue = kwargs.pop("model")

        class ViewSet(_ZeroZeroViewSet):
            Model = ModelValue

        return ViewSet
