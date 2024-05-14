# FROM https://github.com/python/cpython/blob/6292be7adf247589bbf03524f8883cb4cb61f3e9/Lib/typing.py
from typing import List, Tuple, Type, _GenericAlias
from typing import get_args as get_args
from typing import get_type_hints

from geolib._compat import IS_PYDANTIC_V2


def unpack_if_union(tp):
    if is_union(tp):
        return get_args(tp)[0]
    else:
        return tp


def is_union(tp):
    return isinstance(tp, _GenericAlias) and tp._name in (None, "Optional")


def is_list(tp):
    return isinstance(tp, _GenericAlias) and tp._name == "List"


def get_filtered_type_hints(class_type: Type) -> List[Tuple[str, Type]]:
    """Gets all the (valid) type hints for a given class.

    Args:
        class_type (Type): Class to extract property fields.

    Returns:
        List[Tuple[str, Type]]: Filtered list of tuples representing field name and type.
    """
    return [
        (field_name, field)
        for field_name, field in get_type_hints(class_type).items()
        if not field_name.startswith("__")
    ]


def get_required_class_field(class_type: Type) -> List[Tuple[str, Type]]:
    """Gets all the (valid) class fields which are mandatory.

    Args:
        class_type (Type): [description]

    Returns:
        List[Tuple[str, Type]]: [description]
    """
    if IS_PYDANTIC_V2:
        return [
            (field_name, field)
            for field_name, field in class_type.model_fields.items()
            if field.is_required() and not field_name.startswith("__")
        ]
    else:
        return [
            (field_name, field)
            for field_name, field in class_type.__fields__.items()
            if field.required and not field_name.startswith("__")
        ]
