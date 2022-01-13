from django.db import transaction
from rest_framework import renderers, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response
from rest_framework.utils import serializer_helpers
from rest_framework_csv.renderers import CSVStreamingRenderer

from zerozero import permissions, serializers, metadata
from zerozero.forms import QueryForm


class ZeroZeroPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "page_size"
    max_page_size = 10000


class _ZeroZeroViewSet(viewsets.ModelViewSet):
    Model = None
    renderer_classes = [
        renderers.JSONRenderer,
        renderers.BrowsableAPIRenderer,
        CSVStreamingRenderer,
    ]
    pagination_class = ZeroZeroPagination
    metadata_class = metadata.ZeroZeroMetadata

    def __init__(self, *args, **kwargs):
        self.app_label = self.Model._meta.app_label
        self.model_name = self.Model._meta.model_name
        self.name = ".".join([self.Model._meta.app_label, self.Model.__name__])

        return super().__init__(*args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        if isinstance(self.request.accepted_renderer, CSVStreamingRenderer):
            return_list = serializer_helpers.ReturnList(
                queryset.values(), serializer=None
            )  # here values are using default but be can be passed in
            return Response(return_list)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

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
