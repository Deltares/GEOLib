import sys
from typing import List, Optional, Type, TypeVar

from pydantic.version import VERSION

PYDANTIC_V2 = VERSION.startswith("2.")

pydanticv1_loaded = False
if PYDANTIC_V2:
    from pydantic.v1 import BaseModel, ValidationError, root_validator
    from pydantic.v1 import types as types
    from pydantic.v1 import validator
    from pydantic.v1.types import conlist

    pydanticv1_loaded = True
else:
    from pydantic import BaseModel, ValidationError, root_validator
    from pydantic import types as types
    from pydantic import validator
    from pydantic.types import conlist

if not PYDANTIC_V2 or pydanticv1_loaded:
    AnyItemType = TypeVar("AnyItemType")

    def patch_conlist(
        item_type: Type[AnyItemType],
        *,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        unique_items: Optional[bool] = None,
    ) -> Type[List[AnyItemType]]:
        return conlist(
            item_type=item_type,
            min_items=min_length,
            max_items=max_length,
            unique_items=unique_items,
        )

    types.conlist = patch_conlist

sys.modules["geolib.pydantic.types"] = types
