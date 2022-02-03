from collections import OrderedDict

from django.utils.encoding import force_str

from rest_framework import exceptions, serializers
from rest_framework.reverse import reverse
from rest_framework.metadata import SimpleMetadata


class ZeroZeroMetadata(SimpleMetadata):
    def determine_metadata(self, request, view):
        try:
            metadata = super().determine_metadata(request, view)
        except NotImplementedError:
            metadata = {}
        except AttributeError:
            metadata = {}

        root_view_names = ["APIRootView", "APIRoot"]
        if (
            view.__class__.__name__ in root_view_names
            or view in root_view_names
        ):
            return self.root_metadata(metadata, view)

        serializer = view.get_serializer_class()
        serializer_instance = view.get_serializer()

        fields_metadata = {}

        for field in serializer_instance.fields.keys():
            instance_field = serializer_instance.fields[field]
            field_metadata = get_field_dict(field, serializer_instance, request)

            fields_metadata[field] = field_metadata
        metadata["fields"] = fields_metadata
        metadata["url"] = request.build_absolute_uri(request.path_info)
        return metadata


FIELD_TO_TYPE = {
    "BooleanField": ("boolean", "checkbox"),
    "NullBooleanField": ("boolean", "null-boolean"),
    "IntegerField": ("number", "number"),
    "FloatField": ("number", "number"),
    "DecimalField": ("number", "number"),
    "ForeignKey": ("string", "relation"),
    "OneToOneField": ("string", "relation"),
    "OneToOneRel": ("string", "relation"),
    "HyperlinkedIdentityField": ("string", "relation"),
    "HyperlinkedRelatedField": ("string", "relation"),
    "PrimaryKeyRelatedField": ("string", "relation"),
    "ManyToOneRel": ("string", "relation"),
    "GenericRelation": ("object", "tomany-relation"),
    "text": ("string", "textarea"),
    "choice": ("string", "select"),
    "DateField": ("string", "date"),
    "TimeField": ("string", "time"),
    "DateTimeField": ("string", "datetime"),
    "CharField": ("string", "text"),
    "ChoiceField": ("string", "select"),
    "EmailField": ("string", "email"),
    "URLField": ("string", "url"),
    "ManyToManyField": ("object", "tomany-relation"),
    "ManyToManyRel": ("object", "manytomany-lists"),
    "GenericRelatedField": ("string", "generic-relation"),
    "DurationField": ("string", "duration"),
}


def get_field_dict(field, serializer, request):
    form_field = serializer.fields[field]
    field_meta = {}
    field_meta["name"] = field
    field_meta["type"] = FIELD_TO_TYPE[type(form_field).__name__][1]
    field_meta["json_type"] = FIELD_TO_TYPE[type(form_field).__name__][0]
    field_meta["required"] = form_field.required
    field_meta["read_only"] = form_field.read_only
    if hasattr(form_field, "view_name"):
        field_meta["related_url"] = form_field.reverse(
            form_field.view_name.replace("detail", "list"), request=request
        )
        field_meta["related_name"] = form_field.view_name.replace("-detail", "")
    return field_meta
