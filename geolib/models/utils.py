# FROM https://github.com/python/cpython/blob/6292be7adf247589bbf03524f8883cb4cb61f3e9/Lib/typing.py
from typing import _GenericAlias, _SpecialForm
import collections


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


def is_union(tp):
    return isinstance(tp, _GenericAlias) and tp._name is None


def is_list(tp):
    return isinstance(tp, _GenericAlias) and tp._name == "List"

