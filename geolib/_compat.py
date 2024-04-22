"""This module contaiuns the logic to support both pydantic v1 and v2
"""
from pydantic import VERSION as PYDANTIC_VERSION

IS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")

if IS_PYDANTIC_V2:
    try:
        from pydantic_extra_types.color import Color
        from pydantic_settings import BaseSettings
    except ImportError:
        raise ImportError(
            "Please install `pydantic-settings` and `pydantic-extra-types` to use geolib with "
            "pydantic v2 with `pip install pydantic-settings pydantic-extra-types`. Alternatively, "
            "you can install geolib with the extra required packages by running `pip install "
            "geolib[pydantic-v2]`."
        )
else:
    # Example of how to raise a DeprecationWarning. Should be enabled when it is decided to remove
    # support for pydantic v1 in a future release.
    # raise DeprecationWarning(
    #   "Support for pydantic v1 will be removed in the next major release. Please upgrade to pydantic v2."
    # )
    pass
