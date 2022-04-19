from datetime import datetime
import json
import yaml
import operator

from functools import reduce
import yaml

from django.apps import apps
from django.db.models import Q

STRING_TO_OPERATOR = {
    "AND": operator.and_,
    "OR": operator.or_,
}
OPERATOR_STRING = list(STRING_TO_OPERATOR.keys())

# Patch to ignore dates: https://stackoverflow.com/questions/34667108/ignore-dates-and-times-while-parsing-yaml
yaml.SafeLoader.yaml_implicit_resolvers = {
    k: [r for r in v if r[0] != "tag:yaml.org,2002:timestamp"]
    for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()
}


def load_yaml(value):
    yaml_value = yaml.load(value, Loader=yaml.SafeLoader)
    return json.dumps(yaml_value)


def operation_reducer(clause1, clause2):
    first_q = where_to_q(clause1)
    second_q = where_to_q(clause2)
    return first_q, second_q


def where_to_q(where):
    where_left, where_right = list(where.items())[0]
    if where_left in OPERATOR_STRING[:2]:
        q_expressions = map(where_to_q, where_right)
        operator = STRING_TO_OPERATOR[where_left]
        return reduce(operator, q_expressions)
    # TODO add validation
    if where_left == "NOT":
        return ~where_to_q(where_right)
    return Q(**where)
