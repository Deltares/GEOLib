"""This is part of a compatibility module to accept both pydantic v1 and v2."""

from typing import List, Optional, Type, TypeVar

from . import PYDANTIC_V2, pydanticv1_loaded

if PYDANTIC_V2 and pydanticv1_loaded:
    from pydantic.v1.types import *
    from pydantic.v1.types import conlist as old_conlist
else:
    from pydantic.types import *
    from pydantic.types import conlist as old_conlist


if not PYDANTIC_V2 or pydanticv1_loaded:
    AnyItemType = TypeVar("AnyItemType")

    def conlist(
        item_type: Type[AnyItemType],
        *,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        unique_items: Optional[bool] = None,
    ) -> Type[List[AnyItemType]]:
        return old_conlist(
            item_type=item_type,
            min_items=min_length,
            max_items=max_length,
            unique_items=unique_items,
        )
