from rest_framework import serializers

from rest_framework.utils.field_mapping import (
    get_nested_relation_kwargs,
)

from rest_framework.utils.field_mapping import (
    ClassLookupDict,
    get_field_kwargs,
    get_nested_relation_kwargs,
    get_url_kwargs,
    needs_label,
)
from rest_framework.relations import (
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ManyRelatedField,
    PrimaryKeyRelatedField,
    RelatedField,
    SlugRelatedField,
    StringRelatedField,
)


def get_detail_view_name(model):
    """
    Given a model class, return the view name to use for URL relationships
    that refer to instances of the model.
    """
    return f"{model._meta.app_label.lower()}_{model._meta.model_name.lower()}-detail"


def get_relation_kwargs(field_name, relation_info):
    """
    Creates a default instance of a flat relational field.
    """
    (
        model_field,
        related_model,
        to_many,
        to_field,
        has_through_model,
        reverse,
    ) = relation_info
    kwargs = {
        "queryset": related_model._default_manager,
        "view_name": get_detail_view_name(related_model),
    }

    if to_many:
        kwargs["many"] = True

    if to_field:
        kwargs["to_field"] = to_field

    limit_choices_to = model_field and model_field.get_limit_choices_to()
    if limit_choices_to:
        if not isinstance(limit_choices_to, models.Q):
            limit_choices_to = models.Q(**limit_choices_to)
        kwargs["queryset"] = kwargs["queryset"].filter(limit_choices_to)

    if has_through_model:
        kwargs["read_only"] = True
        kwargs.pop("queryset", None)

    if model_field:
        if model_field.verbose_name and needs_label(model_field, field_name):
            kwargs["label"] = capfirst(model_field.verbose_name)
        help_text = model_field.help_text
        if help_text:
            kwargs["help_text"] = help_text
        if not model_field.editable:
            kwargs["read_only"] = True
            kwargs.pop("queryset", None)
        if kwargs.get("read_only", False):
            # If this field is read-only, then return early.
            # No further keyword arguments are valid.
            return kwargs

        if model_field.has_default() or model_field.blank or model_field.null:
            kwargs["required"] = False
        if model_field.null:
            kwargs["allow_null"] = True
        if model_field.validators:
            kwargs["validators"] = model_field.validators
        if getattr(model_field, "unique", False):
            validator = UniqueValidator(
                queryset=model_field.model._default_manager
            )
            kwargs["validators"] = kwargs.get("validators", []) + [validator]
        if to_many and not model_field.blank:
            kwargs["allow_empty"] = False

    return kwargs


def get_url_kwargs(model_field):
    return {"view_name": get_detail_view_name(model_field)}


class _ZeroZeroSerializer(serializers.HyperlinkedModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def build_field(self, field_name, info, model_class, nested_depth):
        """
        Return a two tuple of (cls, kwargs) to build a serializer field with.
        """
        if field_name in info.fields_and_pk:
            model_field = info.fields_and_pk[field_name]
            return self.build_standard_field(field_name, model_field)

        elif field_name in info.relations:
            relation_info = info.relations[field_name]
            if not nested_depth:
                return self.build_relational_field(field_name, relation_info)
            else:
                return self.build_nested_field(
                    field_name, relation_info, nested_depth
                )

        elif hasattr(model_class, field_name):
            return self.build_property_field(field_name, model_class)

        elif field_name == self.url_field_name:
            return self.build_url_field(field_name, model_class)

        return self.build_unknown_field(field_name, model_class)

    def build_relational_field(self, field_name, relation_info):
        """
        Create fields for forward and reverse relationships.
        """
        field_class = self.serializer_related_field
        field_kwargs = get_relation_kwargs(field_name, relation_info)
        to_field = field_kwargs.pop("to_field", None)
        if (
            to_field
            and not relation_info.reverse
            and not relation_info.related_model._meta.get_field(
                to_field
            ).primary_key
        ):
            field_kwargs["slug_field"] = to_field
            field_class = self.serializer_related_to_field

        # `view_name` is only valid for hyperlinked relationships.
        if not issubclass(field_class, HyperlinkedRelatedField):
            field_kwargs.pop("view_name", None)
        return field_class, field_kwargs

    def build_url_field(self, field_name, model_class):
        """
        Create a field representing the object's own URL.
        """
        field_class = self.serializer_url_field
        field_kwargs = get_url_kwargs(model_class)
        return field_class, field_kwargs

    def build_nested_field(self, field_name, relation_info, nested_depth):
        class NestedSerializer(ZeroZeroSerializer):
            class Meta:
                model = relation_info.related_model
                depth = nested_depth - 1
                fields = "__all__"

        field_class = NestedSerializer
        field_kwargs = get_nested_relation_kwargs(relation_info)

        return field_class, field_kwargs


class ZeroZeroSerializer:
    def __new__(cls, *args, **kwargs):
        Model = kwargs.pop("model")
        exclude_value = kwargs.pop("exclude", [])

        class ModelSerializer(_ZeroZeroSerializer):
            class Meta:
                model = Model
                exclude = exclude_value
                ref_name = "{}.{}".format(
                    Model._meta.app_label, Model._meta.model_name
                )

        return ModelSerializer
