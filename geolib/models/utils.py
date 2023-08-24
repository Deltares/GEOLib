# FROM https://github.com/python/cpython/blob/6292be7adf247589bbf03524f8883cb4cb61f3e9/Lib/typing.py
import collections
import sys
from typing import Dict, List, Tuple, Type, _GenericAlias, _SpecialForm, get_type_hints

if sys.version_info < (3, 9):
    # Python 3.9 does not include `_special`, so use the function from typing instead

    def get_args(tp):
        """Get type arguments with all substitutions performed.
        For unions, basic simplifications used by Union constructor are performed.
        Examples::
            get_args(Dict[str, int]) == (str, int)
            get_args(int) == ()
            get_args(Union[int, Union[T, int], str][int]) == (int, str)
            get_args(Union[int, Tuple[T, int]][str]) == (int, Tuple[str, int])
            get_args(Callable[[], T][int]) == ([], int)
        """
        if isinstance(tp, (_GenericAlias, _SpecialForm)) and not tp._special:
            res = tp.__args__
            if tp.__origin__ is collections.abc.Callable and res[0] is not Ellipsis:
                res = (list(res[:-1]), res[-1])
            return res
        return ()

else:
    from typing import get_args as get_args  # NOQA


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
    return [
        (field_name, field)
        for field_name, field in class_type.__fields__.items()
        if field.required and not field_name.startswith("__")
    ]
