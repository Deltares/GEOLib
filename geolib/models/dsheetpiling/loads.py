from pydantic import BaseModel as DataModel


class UniformLoad(DataModel):
    right_load: float
    left_load: float


class Moment(DataModel):
    """Non Uniform Load."""


class SurchargeLoad(DataModel):
    """Non Uniform Load."""


class HorizontalLineLoad(DataModel):
    """Non Uniform Load."""


class NormalForce(DataModel):
    """Non Uniform Load."""


class SoilDisplacement(DataModel):
    """Non Uniform Load."""


class Earthquake(DataModel):
    """Non Uniform Load."""

    force: float  # g
