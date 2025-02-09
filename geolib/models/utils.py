# FROM https://github.com/python/cpython/blob/6292be7adf247589bbf03524f8883cb4cb61f3e9/Lib/typing.py
from typing import get_args, get_origin, get_type_hints


def unpack_if_union(tp):
    return get_args(tp)[0] if is_union(tp) else tp


def is_union(tp):
    return len(get_args(tp)) > 1


def is_list(tp):
    return tp is list or get_origin(tp) is list


def get_filtered_type_hints(class_type: type) -> list[tuple[str, type]]:
    """Gets all the (valid) type hints for a given class.

    Args:
        class_type (type): Class to extract property fields.

    Returns:
        list[tuple[str, type]]: Filtered list of tuples representing field name and type.
    """
    return [
        (field_name, field)
        for field_name, field in get_type_hints(class_type).items()
        if not field_name.startswith("__")
    ]


def get_required_class_field(class_type: type) -> list[tuple[str, type]]:
    """Gets all the (valid) class fields which are mandatory.

    Args:
        class_type (type): [description]

    Returns:
        list[tuple[str, type]]: [description]
    """
    return [
        (field_name, field)
        for field_name, field in class_type.model_fields.items()
        if field.is_required() and not field_name.startswith("__")
    ]
