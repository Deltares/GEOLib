from abc import ABCMeta, abstractmethod
from typing import Optional

from pydantic import conlist, constr, validator

from geolib.geometry import Point
from geolib.models import BaseDataClass

from .internal import HorizontalLineLoad as HorizontalLineLoadInternal
from .internal import Moment as MomentInternal
from .internal import NormalForce as NormalForceInternal
from .internal import SurchargeLoad as InternalSurchargeLoad
from .internal import SurchargePoint as InternalSurchargePoint
from .internal import UniformLoad as InternalUniformLoad
from .settings import (
    DistributionType,
    LoadTypeFavourableUnfavourable,
    LoadTypeFavourableUnfavourableMoment,
    LoadTypePermanentVariable,
)


class VerificationLoadSettingsHorizontalLineLoad(BaseDataClass):
    """
    These options are available only if the Verification (EC7/CUR) option is selected in the Model window for the D-SheetPiling model.
    For GEOLIB the "verification" parameter should be set to True in the function DSheetPilingModel.set_model

    Args:
        duration_type: Select the duration of load application, Permanent or Variable.
        load_type: Select the type of load, Favorable, Unfavorable or leave it D-Sheet Piling determined.
    """

    load_type: LoadTypeFavourableUnfavourable = (
        LoadTypeFavourableUnfavourable.DSHEETPILING_DETERMINED
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class VerificationLoadSettingsLoads(BaseDataClass):
    """
    These options are available only if the Verification (EC7/CUR) option is selected in the Model window for the D-SheetPiling model.
    For GEOLIB the "verification" parameter should be set to True in the function DSheetPilingModel.set_model

    Args:
        duration_type: Select the duration of load application, Permanent or Variable.
        load_type: Select the type of load, Favorable, Unfavorable or leave it D-Sheet Piling determined.
    """

    load_type: LoadTypeFavourableUnfavourable = (
        LoadTypeFavourableUnfavourable.DSHEETPILING_DETERMINED
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class VerificationLoadSettings(BaseDataClass):
    """
    Load class for moment loads
    These options are available only if the Verification (EC7/CUR) option is selected in the Model window for the D-SheetPiling model.
    For GEOLIB the "verification" parameter should be set to True in the function DSheetPilingModel.set_model

    Args:
        duration_type: Select the duration of load application, Permanent or Variable.
        load_type: Select the type of load, Favorable or Unfavorable.
    """

    load_type: LoadTypeFavourableUnfavourableMoment = (
        LoadTypeFavourableUnfavourableMoment.FAVOURABLE
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class VerificationLoadSettingsMomentNormalForce(BaseDataClass):
    """
    Load class for moment loads
    These options are available only if the Verification (EC7/CUR) option is selected in the Model window for the D-SheetPiling model.
    For GEOLIB the "verification" parameter should be set to True in the function DSheetPilingModel.set_model

    Args:
        duration_type: Select the duration of load application, Permanent or Variable.
        load_type: Select the type of load, Favorable or Unfavorable.
    """

    load_type: LoadTypeFavourableUnfavourableMoment = (
        LoadTypeFavourableUnfavourableMoment.FAVOURABLE
    )
    duration_type: LoadTypePermanentVariable = LoadTypePermanentVariable.PERMANENT


class UniformLoad(BaseDataClass):
    """Uniform Load. This option is not available for SignlePileModelType.

    Args:
        name: Name of the SurchargeLoad.
        left_load: Value of the load on the left side.
        right_load: Value of the load on the right side.
        verification_load_settings: VerificationLoadSettings.
        standard_deviation_left: Standard deviation of the distribution type of the left side.
        standard_deviation_right: Standard deviation of the distribution type of the right side.
        distribution_type_left: Distribution type of the left side.
        distribution_type_right: Distribution type of the right side.
    """

    name: constr(min_length=1, max_length=50)
    left_load: float
    right_load: float
    verification_load_settings: VerificationLoadSettingsLoads = VerificationLoadSettingsLoads()
    standard_deviation_left: float = 0.0
    standard_deviation_right: float = 0.0
    distribution_type_left: DistributionType = DistributionType.NORMAL
    distribution_type_right: DistributionType = DistributionType.NORMAL

    def to_internal(self) -> InternalUniformLoad:
        uniformload = InternalUniformLoad(
            name=self.name,
            uniformloadleft=self.left_load,
            uniformloadright=self.right_load,
            uniformloadstandarddeviationleft=self.standard_deviation_left,
            uniformloadstandarddeviationright=self.standard_deviation_right,
        )
        uniformload.uniformloadpermanent = self.verification_load_settings.duration_type
        uniformload.uniformloadfavourable = self.verification_load_settings.load_type
        if self.distribution_type_left:
            uniformload.uniformloaddistleft = self.distribution_type_left
        if self.distribution_type_right:
            uniformload.uniformloaddistright = self.distribution_type_right
        return uniformload


class Moment(BaseDataClass):
    """Moment Load."""

    name: constr(min_length=1, max_length=50)
    level: float
    load: float
    verification_load_settings: VerificationLoadSettingsMomentNormalForce = VerificationLoadSettingsMomentNormalForce()

    def to_internal(self) -> MomentInternal:
        moment = MomentInternal(
            **self.dict(exclude_none=True, exclude={"verification_load_settings"})
        )
        moment.load_type = self.verification_load_settings.load_type
        moment.duration_type = self.verification_load_settings.duration_type
        return moment


class SurchargeLoad(BaseDataClass):
    """Surcharge Load.

    Args:
        name: Name of the SurchargeLoad.
        points: SurchargeLoad points. Points (X, Z) must be defined from the sheet outwards regarding x-coordinate.
        verification_load_settings: VerificationLoadSettings.
        standard_deviation: Standard deviation of the distribution type.
        distribution_type: Distribution type.
    """

    name: constr(min_length=1, max_length=50)
    points: conlist(Point, min_items=1)
    verification_load_settings: VerificationLoadSettingsLoads = VerificationLoadSettingsLoads()
    standard_deviation: float = 0.0
    distribution_type: DistributionType = DistributionType.NORMAL

    @validator("points")
    def points_must_be_increasing_and_greater_or_equal_to_zero(cls, v):
        x_coords = [p.x for p in v]
        if min(x_coords) < 0:
            raise ValueError(
                f"All x-coordinates must be greater than or equal to 0, found {min(x_coords)}"
            )
        if x_coords != sorted(x_coords):
            raise ValueError("x-coordinates must be strictly increasing")
        return v

    def to_internal(self) -> InternalSurchargeLoad:
        surchargeload = InternalSurchargeLoad(
            name=self.name,
            points=[
                InternalSurchargePoint(
                    surchargeloaddistance=point.x, surchargeloadvalue=point.z
                )
                for point in self.points
            ],
        )
        surchargeload.surchargeloadpermanent = (
            self.verification_load_settings.duration_type
        )
        surchargeload.surchargeloadfavourable = self.verification_load_settings.load_type
        if self.standard_deviation:
            surchargeload.surchargeloadstandarddeviation = self.standard_deviation
        if self.distribution_type:
            surchargeload.surchargeloaddistribution = self.distribution_type
        return surchargeload


class HorizontalLineLoad(BaseDataClass):
    """Horizontal Line Load."""

    name: constr(min_length=1, max_length=50)
    level: float
    load: float
    verification_load_settings: VerificationLoadSettingsLoads = VerificationLoadSettingsLoads()

    def to_internal(self) -> HorizontalLineLoadInternal:
        horizontallineload = HorizontalLineLoadInternal(
            **self.dict(exclude_none=True, exclude={"verification_load_settings"})
        )
        horizontallineload.load_type = self.verification_load_settings.load_type
        horizontallineload.duration_type = self.verification_load_settings.duration_type
        return horizontallineload


class NormalForce(BaseDataClass):
    """Normal Force Load."""

    name: constr(min_length=1, max_length=50)
    force_at_sheet_pile_top: float
    force_at_surface_level_left_side: float
    force_at_surface_level_right_side: float
    force_at_sheet_pile_toe: float
    verification_load_settings: VerificationLoadSettingsMomentNormalForce = VerificationLoadSettingsMomentNormalForce()

    def to_internal(self) -> NormalForceInternal:
        normalforce = NormalForceInternal(
            **self.dict(exclude_none=True, exclude={"verification_load_settings"})
        )
        normalforce.load_type = self.verification_load_settings.load_type
        normalforce.duration_type = self.verification_load_settings.duration_type
        return normalforce


class SoilDisplacement(BaseDataClass):
    """Non Uniform Load."""


class Earthquake(BaseDataClass):
    """Non Uniform Load."""

    force: float  # g
