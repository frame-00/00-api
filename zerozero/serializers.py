from rest_framework import serializers

from rest_framework.utils.field_mapping import (
    get_nested_relation_kwargs,
)


class _ZeroZeroSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def is_valid(self, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

    def to_representation(self, instance):
        return serializers.ModelSerializer.to_representation(self, instance)


class ZeroZeroSerializer:
    def __new__(cls, *args, **kwargs):
        Model = kwargs.pop("model")
        exclude_value = kwargs.pop("exclude", [])

        class ModelSerializer(_ZeroZeroSerializer):
            class Meta:
                model = Model
                exclude = exclude_value
                ref_name = "{}.{}".format(Model._meta.app_label, Model._meta.model_name)

        return ModelSerializer
