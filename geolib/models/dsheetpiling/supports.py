from pydantic import BaseModel as DataModel


class Anchor(DataModel):
    """Anchor."""


class Strut(DataModel):
    """Strut."""


class SpringSupport(DataModel):
    """Spring support."""


class RigidSupport(DataModel):
    """Rigid support."""
