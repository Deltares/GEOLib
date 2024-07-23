"""This module contaiuns the logic to support both pydantic v1 and v2
"""
from pydantic import VERSION as PYDANTIC_VERSION

IS_PYDANTIC_V2 = PYDANTIC_VERSION.startswith("2.")
