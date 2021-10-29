import json
from collections import defaultdict
from datetime import date, datetime
from enum import Enum
from functools import partial
from itertools import chain
from math import isfinite
from typing import Dict, Generator, List, Optional, Set, Tuple, Union

from pydantic import ValidationError, confloat, conlist, root_validator, validator

from geolib import __version__ as version
from geolib.geometry import Point
from geolib.models.base_model_structure import BaseModelStructure
from geolib.soils import ShearStrengthModelTypePhreaticLevel, Soil
from geolib.utils import camel_to_snake, snake_to_camel

from .dstability_validator import DStabilityValidator
from .utils import children


class DStabilityBaseModelStructure(BaseModelStructure):
    def dict(_, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        return {
            k: "NaN" if isinstance(v, float) and not isfinite(v) else v
            for k, v in data.items()
        }


class AnalysisTypeEnum(Enum):
    BISHOP = "Bishop"
    BISHOP_BRUTE_FORCE = "BishopBruteForce"
    SPENCER = "Spencer"
    SPENCER_GENETIC = "SpencerGenetic"
    UPLIFT_VAN = "UpliftVan"
    UPLIFT_VAN_PARTICLE_SWARM = "UpliftVanParticleSwarm"


AnalysisType = AnalysisTypeEnum


class BishopSlipCircleResult(DStabilityBaseModelStructure):
    x: float
    z: float
    radius: float


class UpliftVanSlipCircleResult(DStabilityBaseModelStructure):
    x_left: float
    z_left: float
    x_right: float
    z_right: float
    z_tangent: float


class SpencerSlipPlaneResult(DStabilityBaseModelStructure):
    slipplane: List[Point]


class DStabilitySubStructure(DStabilityBaseModelStructure):
    @classmethod
    def structure_name(cls):
        class_name = cls.__name__
        return str.split(str.lower(class_name), ".")[-1]

    @classmethod
    def structure_group(cls):
        return cls.structure_name()


# waternet schema
class PersistablePoint(DStabilityBaseModelStructure):
    X: Optional[float] = "NaN"
    Z: Optional[float] = "NaN"


class PersistableHeadLine(DStabilityBaseModelStructure):
    Id: Optional[str]
    Label: Optional[str]
    Notes: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class PersistableReferenceLine(DStabilityBaseModelStructure):
    BottomHeadLineId: Optional[str]
    Id: Optional[str]
    Label: Optional[str]
    Notes: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]
    TopHeadLineId: Optional[str]


class Waternet(DStabilitySubStructure):
    """waternets/waternet_x.json."""

    @classmethod
    def structure_group(cls) -> str:
        return "waternets"

    @classmethod
    def structure_name(cls) -> str:
        return "waternets"

    Id: Optional[str]
    ContentVersion: Optional[str] = "1"
    PhreaticLineId: Optional[str]
    HeadLines: List[PersistableHeadLine] = []
    ReferenceLines: List[PersistableReferenceLine] = []
    UnitWeightWater: Optional[float] = 9.81

    def get_head_line(self, head_line_id: str) -> PersistableHeadLine:
        for head_line in self.HeadLines:
            if head_line.Id == head_line_id:
                return head_line

        raise ValueError(f"No headline with id {head_line_id} in model.")

    def get_reference_line(self, reference_line_id: str) -> PersistableReferenceLine:
        for reference_line in self.ReferenceLines:
            if reference_line.Id == reference_line_id:
                return reference_line

        raise ValueError(f"No referenceline with id {reference_line_id} in model.")

    def has_head_line_id(self, head_line_id: str) -> bool:
        return head_line_id in {head_line.Id for head_line in self.HeadLines}

    def add_head_line(
        self,
        head_line_id: str,
        label: str,
        notes: str,
        points: List[Point],
        is_phreatic_line: bool,
    ) -> PersistableHeadLine:
        head_line = PersistableHeadLine(Id=head_line_id, Label=label, Notes=notes)
        head_line.Points = [PersistablePoint(X=p.x, Z=p.z) for p in points]

        self.HeadLines.append(head_line)
        if is_phreatic_line:
            self.PhreaticLineId = head_line.Id

        return head_line

    def add_reference_line(
        self,
        reference_line_id: str,
        label: str,
        notes: str,
        points: List[Point],
        bottom_head_line_id: str,
        top_head_line_id: str,
    ) -> PersistableReferenceLine:
        reference_line = PersistableReferenceLine(
            Id=reference_line_id, Label=label, Notes=notes
        )
        reference_line.Points = [PersistablePoint(X=p.x, Z=p.z) for p in points]

        if not self.has_head_line_id(bottom_head_line_id):
            raise ValueError(
                f"Unknown headline id {bottom_head_line_id} for bottom_head_line_id"
            )

        if not self.has_head_line_id(top_head_line_id):
            raise ValueError(
                f"Unknown headline id {top_head_line_id} for top_head_line_id"
            )

        reference_line.BottomHeadLineId = bottom_head_line_id
        reference_line.TopHeadLineId = top_head_line_id

        self.ReferenceLines.append(reference_line)
        return reference_line


class PersistableDitchCharacteristics(DStabilityBaseModelStructure):
    DitchBottomEmbankmentSide: Optional[float] = "NaN"
    DitchBottomLandSide: Optional[float] = "NaN"
    DitchEmbankmentSide: Optional[float] = "NaN"
    DitchLandSide: Optional[float] = "NaN"


class PersistableEmbankmentCharacteristics(DStabilityBaseModelStructure):
    EmbankmentToeLandSide: Optional[float] = "NaN"
    EmbankmentToeWaterSide: Optional[float] = "NaN"
    EmbankmentTopLandSide: Optional[float] = "NaN"
    EmbankmentTopWaterSide: Optional[float] = "NaN"
    ShoulderBaseLandSide: Optional[float] = "NaN"


class EmbankmentSoilScenarioEnum(str, Enum):
    CLAY_EMBANKMENT_ON_CLAY = "ClayEmbankmentOnClay"
    CLAY_EMBANKMENT_ON_SAND = "ClayEmbankmentOnSand"
    SAND_EMBANKMENT_ON_CLAY = "SandEmbankmentOnClay"
    SAND_EMBANKMENT_ON_SAND = "SandEmbankmentOnSand"


class WaternetCreatorSettings(DStabilitySubStructure):
    """waternetcreatorsettings/waternetcreatorsettings_x.json"""

    AdjustForUplift: Optional[bool] = False
    AquiferInsideAquitardLayerId: Optional[str]
    AquiferLayerId: Optional[str]
    AquiferLayerInsideAquitardLeakageLengthInwards: Optional[float] = "NaN"
    AquiferLayerInsideAquitardLeakageLengthOutwards: Optional[float] = "NaN"
    AquitardHeadLandSide: Optional[float] = "NaN"
    AquitardHeadWaterSide: Optional[float] = "NaN"
    ContentVersion: Optional[str] = "1"
    DitchCharacteristics: Optional[
        PersistableDitchCharacteristics
    ] = PersistableDitchCharacteristics()
    DrainageConstruction: Optional[PersistablePoint] = PersistablePoint()
    EmbankmentCharacteristics: Optional[
        PersistableEmbankmentCharacteristics
    ] = PersistableEmbankmentCharacteristics()
    EmbankmentSoilScenario: EmbankmentSoilScenarioEnum = "ClayEmbankmentOnClay"
    Id: Optional[str]
    InitialLevelEmbankmentTopLandSide: Optional[float] = "NaN"
    InitialLevelEmbankmentTopWaterSide: Optional[float] = "NaN"
    IntrusionLength: Optional[float] = "NaN"
    IsAquiferLayerInsideAquitard: Optional[bool] = False
    IsDitchPresent: Optional[bool] = False
    IsDrainageConstructionPresent: Optional[bool] = False
    MeanWaterLevel: Optional[float] = "NaN"
    NormativeWaterLevel: Optional[float] = "NaN"
    OffsetEmbankmentToeLandSide: Optional[float] = "NaN"
    OffsetEmbankmentTopLandSide: Optional[float] = "NaN"
    OffsetEmbankmentTopWaterSide: Optional[float] = "NaN"
    OffsetShoulderBaseLandSide: Optional[float] = "NaN"
    PleistoceneLeakageLengthInwards: Optional[float] = "NaN"
    PleistoceneLeakageLengthOutwards: Optional[float] = "NaN"
    UseDefaultOffsets: Optional[bool] = True
    WaterLevelHinterland: Optional[float] = "NaN"

    @classmethod
    def structure_group(cls) -> str:
        return "waternetcreatorsettings"


class PersistableStochasticParameter(DStabilityBaseModelStructure):
    IsProbabilistic: bool = False
    Mean: float = 1.0
    StandardDeviation: float = 0.0


class StateType(Enum):
    OCR = "Ocr"
    POP = "Pop"
    YIELD_STRESS = "YieldStress"


class PersistableStress(DStabilityBaseModelStructure):
    Ocr: float = 1.0
    Pop: float = 0.0
    PopStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    StateType: Optional[StateType]
    YieldStress: float = 0.0


class PersistableStateLinePoint(DStabilityBaseModelStructure):
    Above: Optional[PersistableStress]
    Below: Optional[PersistableStress]
    Id: Optional[str]
    IsAboveAndBelowCorrelated: Optional[bool]
    IsProbabilistic: Optional[bool]
    Label: Optional[str]
    X: Optional[float]


class PersistableStateLine(DStabilityBaseModelStructure):
    Points: Optional[List[Optional[PersistablePoint]]]
    Values: Optional[List[Optional[PersistableStateLinePoint]]]


class PersistableStatePoint(DStabilityBaseModelStructure):
    Id: Optional[str]
    IsProbabilistic: Optional[bool]
    Label: Optional[str]
    LayerId: Optional[str]
    Point: Optional[PersistablePoint]
    Stress: Optional[PersistableStress]


class State(DStabilitySubStructure):
    """states/states_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "states"

    @classmethod
    def structure_group(cls) -> str:
        return "states"

    ContentVersion: Optional[str] = "1"
    Id: Optional[str]
    StateLines: List[PersistableStateLine] = []
    StatePoints: List[PersistableStatePoint] = []

    def add_state_point(self, state_point: PersistableStatePoint) -> None:
        self.StatePoints.append(state_point)

    def add_state_line(
        self,
        points: List[PersistablePoint],
        state_points: List[PersistableStateLinePoint],
    ):
        self.StateLines.append(PersistableStateLine(Points=points, Values=state_points))


# statecorrelation


class PersistableStateCorrelation(DStabilityBaseModelStructure):
    CorrelatedStateIds: Optional[List[Optional[str]]]
    IsFullyCorrelated: Optional[bool]


class StateCorrelation(DStabilitySubStructure):
    """statecorrelations/statecorrelations_1.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "statecorrelations"

    @classmethod
    def structure_group(cls) -> str:
        return "statecorrelations"

    ContentVersion: Optional[str] = "1"
    Id: Optional[str]
    StateCorrelations: Optional[List[Optional[PersistableStateCorrelation]]] = []


class Stage(DStabilitySubStructure):
    """stages/stage_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "stage"

    @classmethod
    def structure_group(cls) -> str:
        return "stages"

    AnalysisType: Optional[AnalysisTypeEnum] = AnalysisType.BISHOP_BRUTE_FORCE
    CalculationSettingsId: Optional[str]
    ContentVersion: Optional[str] = "1"
    DecorationsId: Optional[str]
    GeometryId: Optional[str]
    Id: Optional[str]
    Label: Optional[str]
    LoadsId: Optional[str]
    Notes: Optional[str]
    ReinforcementsId: Optional[str]
    ResultId: Optional[str] = None
    SoilLayersId: Optional[str]
    StateCorrelationsId: Optional[str]
    StateId: Optional[str]
    WaternetCreatorSettingsId: Optional[str]
    WaternetId: Optional[str]


class PersistableShadingType(Enum):
    DIAGONAL_A = "DiagonalA"
    DIAGONAL_B = "DiagonalB"
    DIAGONAL_C = "DiagonalC"
    DIAGONAL_D = "DiagonalD"
    DOT_A = "DotA"
    DOT_B = "DotB"
    DOT_C = "DotC"
    DOT_D = "DotD"
    HORIZONTAL_A = "HorizontalA"
    HORIZONTAL_B = "HorizontalB"
    NONE = "None"


class PersistableSoilVisualization(DStabilityBaseModelStructure):
    Color: Optional[str]
    PersistableShadingType: Optional[PersistableShadingType]
    SoilId: Optional[str]


class SoilVisualisation(DStabilityBaseModelStructure):
    ContentVersion: Optional[str] = "1"
    SoilVisualizations: Optional[List[Optional[PersistableSoilVisualization]]] = []

    @classmethod
    def structure_name(cls) -> str:
        return "soilvisualizations"


class PersistableSoilLayer(DStabilityBaseModelStructure):
    LayerId: Optional[str]
    SoilId: Optional[str]


class SoilLayerCollection(DStabilitySubStructure):
    """soillayers/soillayers_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "soillayers"

    @classmethod
    def structure_group(cls) -> str:
        return "soillayers"

    ContentVersion: Optional[str] = "1"
    Id: Optional[str]
    SoilLayers: List[PersistableSoilLayer] = []

    def add_soillayer(self, layer_id: str, soil_id: str) -> PersistableSoilLayer:
        psl = PersistableSoilLayer(LayerId=layer_id, SoilId=soil_id)
        self.SoilLayers.append(psl)
        return psl

    def get_ids(self, exclude_soil_layer_id: Optional[int]) -> Set[str]:
        if exclude_soil_layer_id is not None:
            exclude_soil_layer_id = str(exclude_soil_layer_id)
        return {
            layer.LayerId
            for layer in self.SoilLayers
            if layer.LayerId != exclude_soil_layer_id
        }


class PersistableSoilCorrelation(DStabilityBaseModelStructure):
    CorrelatedSoilIds: Optional[List[str]]


class SoilCorrelation(DStabilitySubStructure):
    """soilcorrelations.json"""

    ContentVersion: Optional[str] = "1"
    SoilCorrelations: Optional[List[Optional[PersistableSoilCorrelation]]] = []

    @classmethod
    def structure_name(cls) -> str:
        return "soilcorrelations"


class ShearStrengthModelTypePhreaticLevelInternal(Enum):
    """
    Shear Strength Model Type. These types represent the types that
    are internally defined in the json files of D-Stability.
    """

    C_PHI = "CPhi"
    NONE = "None"
    SU = "Su"
    SUTABLE = "SuTable"

    def to_global_shear_strength_model(self):
        transform_dictionary = {
            "CPhi": "Mohr_Coulomb",
            "None": "None",
            "Su": "SHANSEP",
            "SuTable": "SuTable",
        }
        return transform_dictionary[self.value]


class PersistableSuTablePoint(DStabilitySubStructure):
    EffectiveStress: float = 0.0
    Su: float = 0.0


class PersistableSuTable(DStabilityBaseModelStructure):
    StrengthIncreaseExponent: float = 1.0
    StrengthIncreaseExponentStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    SuTablePoints: List[PersistableSuTablePoint] = []
    IsSuTableProbabilistic: bool = False
    SuTableVariationCoefficient: float = 0.0

    def to_global_su_table(self):
        from geolib.soils import SuTablePoint

        su_table = []
        for su_table_point in self.SuTablePoints:
            su_table.append(
                SuTablePoint(su=su_table_point.Su, stress=su_table_point.EffectiveStress)
            )
        return su_table


class PersistableSoil(DStabilityBaseModelStructure):
    Code: str = ""
    Cohesion: confloat(ge=0) = 0.0
    CohesionAndFrictionAngleCorrelated: bool = False
    CohesionStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    Dilatancy: confloat(ge=0) = 0.0
    DilatancyStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    FrictionAngle: confloat(ge=0) = 0.0
    FrictionAngleStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    Id: str = ""
    IsProbabilistic: bool = False
    Name: str = ""
    ShearStrengthModelTypeAbovePhreaticLevel: ShearStrengthModelTypePhreaticLevelInternal = (
        ShearStrengthModelTypePhreaticLevelInternal.C_PHI
    )
    ShearStrengthModelTypeBelowPhreaticLevel: ShearStrengthModelTypePhreaticLevelInternal = (
        ShearStrengthModelTypePhreaticLevelInternal.SU
    )
    ShearStrengthRatio: confloat(ge=0) = 0.0
    ShearStrengthRatioAndShearStrengthExponentCorrelated: bool = False
    ShearStrengthRatioStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    StrengthIncreaseExponent: confloat(ge=0) = 1.0
    StrengthIncreaseExponentStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    VolumetricWeightAbovePhreaticLevel: confloat(ge=0) = 0.0
    VolumetricWeightBelowPhreaticLevel: confloat(ge=0) = 0.0
    SuTable: PersistableSuTable = PersistableSuTable()


class SoilCollection(DStabilitySubStructure):
    """soils.json"""

    ContentVersion: Optional[str] = "1"
    Soils: List[PersistableSoil] = [
        PersistableSoil(
            Id="2",
            Name="Embankment new",
            Code="H_Aa_ht_new",
            Cohesion=7.0,
            FrictionAngle=30.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.26,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=19.3,
            VolumetricWeightBelowPhreaticLevel=19.3,
        ),
        PersistableSoil(
            Id="3",
            Name="Embankment old",
            Code="H_Aa_ht_old",
            Cohesion=7.0,
            FrictionAngle=30.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.26,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="4",
            Name="Clay, shallow",
            Code="H_Rk_k_shallow",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.23,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=14.8,
            VolumetricWeightBelowPhreaticLevel=14.8,
        ),
        PersistableSoil(
            Id="5",
            Name="Clay, deep",
            Code="H_Rk_k_deep",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.23,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=15.6,
            VolumetricWeightBelowPhreaticLevel=15.6,
        ),
        PersistableSoil(
            Id="6",
            Name="Organic clay",
            Code="H_Rk_ko",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.24,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.85,
            VolumetricWeightAbovePhreaticLevel=13.9,
            VolumetricWeightBelowPhreaticLevel=13.9,
        ),
        PersistableSoil(
            Id="7",
            Name="Peat, shallow",
            Code="H_vhv_v",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.3,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=10.1,
            VolumetricWeightBelowPhreaticLevel=10.1,
        ),
        PersistableSoil(
            Id="8",
            Name="Peat, deep",
            Code="H_vbv_v",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.27,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=11.0,
            VolumetricWeightBelowPhreaticLevel=11.0,
        ),
        PersistableSoil(
            Id="9",
            Name="Sand",
            Code="Sand",
            Cohesion=0.0,
            FrictionAngle=30.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.0,
            ShearStrengthModelTypeBelowPhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.C_PHI,
            StrengthIncreaseExponent=0.0,
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=20.0,
        ),
        PersistableSoil(
            Id="10",
            Name="Clay with silt",
            Code="P_Rk_k&s",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.22,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="11",
            Name="Sand with clay",
            Code="H_Ro_z&k",
            Cohesion=0.0,
            FrictionAngle=0.0,
            Dilatancy=0.0,
            ShearStrengthRatio=0.22,
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            StrengthIncreaseExponent=0.9,
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
    ]

    @classmethod
    def structure_name(cls) -> str:
        return "soils"

    def has_soilcode(self, code: str) -> bool:
        """
        Checks if the soilcode is available in the current soil list.

        Args:
            code (str): code of the soil

        Returns:
            bool: True if found, False if not
        """
        return code in {s.Code for s in self.Soils}

    def add_soil(self, soil: Soil) -> PersistableSoil:
        """
        Add a new soil to the model.

        Args:
            soil (Soil): a new soil

        Returns:
            None
        """
        ps = soil._to_dstability()

        self.Soils.append(ps)
        return ps

    @staticmethod
    def __to_global_stochastic_parameter(
        persistable_stochastic_parameter: PersistableStochasticParameter,
    ):
        from geolib.soils import StochasticParameter

        return StochasticParameter(
            is_probabilistic=persistable_stochastic_parameter.IsProbabilistic,
            mean=persistable_stochastic_parameter.Mean,
            standard_deviation=persistable_stochastic_parameter.StandardDeviation,
        )

    def __determine_strength_increase_exponent(self, persistable_soil: PersistableSoil):
        # shear increase exponent taken from persistable_soil.SuTable or just from persistable_soil
        if (
            persistable_soil.ShearStrengthModelTypeAbovePhreaticLevel.value == "Su"
            or persistable_soil.ShearStrengthModelTypeAbovePhreaticLevel.value == "Su"
        ):
            # SHANSEP model is selected so the StrengthIncreaseExponentStochasticParameter from persistable_soil should be used
            return self.__to_global_stochastic_parameter(
                persistable_soil.StrengthIncreaseExponentStochasticParameter
            )
        elif (
            persistable_soil.ShearStrengthModelTypeAbovePhreaticLevel.value == "SuTable"
            or persistable_soil.ShearStrengthModelTypeAbovePhreaticLevel.value
            == "SuTable"
        ):
            # SU table is selected so the StrengthIncreaseExponentStochasticParameter from SuTable should be used
            return self.__to_global_stochastic_parameter(
                persistable_soil.SuTable.StrengthIncreaseExponentStochasticParameter
            )
        else:
            return None

    def __internal_soil_to_global_soil(self, persistable_soil: PersistableSoil):
        from geolib.soils import (
            MohrCoulombParameters,
            SoilWeightParameters,
            UndrainedParameters,
        )

        mohr_coulomb_parameters = MohrCoulombParameters(
            cohesion=self.__to_global_stochastic_parameter(
                persistable_soil.CohesionStochasticParameter
            ),
            friction_angle=self.__to_global_stochastic_parameter(
                persistable_soil.FrictionAngleStochasticParameter
            ),
            dilatancy_angle=self.__to_global_stochastic_parameter(
                persistable_soil.DilatancyStochasticParameter
            ),
            cohesion_and_friction_angle_correlated=persistable_soil.CohesionAndFrictionAngleCorrelated,
        )

        strength_increase_exponent = self.__determine_strength_increase_exponent(
            persistable_soil
        )
        undrained_parameters = UndrainedParameters(
            shear_strength_ratio=self.__to_global_stochastic_parameter(
                persistable_soil.ShearStrengthRatioStochasticParameter
            ),
            strength_increase_exponent=strength_increase_exponent,
            shear_strength_ratio_and_shear_strength_exponent_correlated=persistable_soil.ShearStrengthRatioAndShearStrengthExponentCorrelated,
            su_table=persistable_soil.SuTable.to_global_su_table(),
            probabilistic_su_table=persistable_soil.SuTable.IsSuTableProbabilistic,
            su_table_variation_coefficient=persistable_soil.SuTable.SuTableVariationCoefficient,
        )

        soil_weight_parameters = SoilWeightParameters()
        soil_weight_parameters.saturated_weight.mean = (
            persistable_soil.VolumetricWeightAbovePhreaticLevel
        )
        soil_weight_parameters.unsaturated_weight.mean = (
            persistable_soil.VolumetricWeightAbovePhreaticLevel
        )

        return Soil(
            id=persistable_soil.Id,
            name=persistable_soil.Name,
            code=persistable_soil.Code,
            is_probabilistic=persistable_soil.IsProbabilistic,
            shear_strength_model_above_phreatic_level=persistable_soil.ShearStrengthModelTypeAbovePhreaticLevel.to_global_shear_strength_model(),
            shear_strength_model_below_phreatic_level=persistable_soil.ShearStrengthModelTypeBelowPhreaticLevel.to_global_shear_strength_model(),
            mohr_coulomb_parameters=mohr_coulomb_parameters,
            soil_weight_parameters=soil_weight_parameters,
            undrained_parameters=undrained_parameters,
        )

    def get_soil(self, code: str) -> Soil:
        """
        Get soil by the given code.

        Args:
            code (str): code of the soil

        Returns:
            Soil: the soil object
        """
        for persistable_soil in self.Soils:
            if persistable_soil.Code == code:
                return self.__internal_soil_to_global_soil(persistable_soil)

        raise ValueError(f"Soil code '{code}' not found in the SoilCollection")

    def edit_soil(self, code: str, **kwargs: dict) -> PersistableSoil:
        """
        Update a soil.

        Args:
            code (str): code of the soil
            kwargs (dict): dictionary with agument names and values

        Returns:
            PersistableSoil: the edited soil
        """
        for persistable_soil in self.Soils:
            if persistable_soil.Code == code:
                for k, v in kwargs.items():
                    try:
                        setattr(persistable_soil, snake_to_camel(k), v)
                    except AttributeError:
                        raise ValueError(f"Unknown soil parameter {k}.")

                return persistable_soil

        raise ValueError(f"Soil code '{code}' not found in the SoilCollection")


# Reinforcements


class PersistableForbiddenLine(DStabilityBaseModelStructure):
    End: Optional[PersistablePoint]
    Label: Optional[str]
    Start: Optional[PersistablePoint]


class PersistableGeotextile(DStabilityBaseModelStructure):
    End: Optional[PersistablePoint]
    Label: Optional[str]
    ReductionArea: Optional[float]
    Start: Optional[PersistablePoint]
    TensileStrength: Optional[float]


class PersistableStressAtDistance(DStabilityBaseModelStructure):
    Distance: Optional[float]
    Stress: Optional[float]


class PersistableNail(DStabilityBaseModelStructure):
    BendingStiffness: Optional[float] = 0.0
    CriticalAngle: Optional[float] = 0.0
    Diameter: Optional[float]
    Direction: Optional[float] = 0.0
    GroutDiameter: Optional[float] = 0.0
    HorizontalSpacing: Optional[float] = 0.0
    Label: Optional[str]
    LateralStresses: Optional[List[Optional[PersistableStressAtDistance]]] = []
    Length: Optional[float]
    Location: Optional[PersistablePoint]
    MaxPullForce: Optional[float] = 0.0
    PlasticMoment: Optional[float] = 0.0
    ShearStresses: Optional[List[Optional[PersistableStressAtDistance]]] = []
    UseFacing: Optional[bool] = False
    UseLateralStress: Optional[bool] = False
    UseShearStress: Optional[bool] = False


class Reinforcements(DStabilitySubStructure):
    """reinforcements/reinforcements_x.json"""

    Id: Optional[str]
    ContentVersion: Optional[str] = "1"
    ForbiddenLines: List[PersistableForbiddenLine] = []
    Geotextiles: List[PersistableGeotextile] = []
    Nails: List[PersistableNail] = []

    def add_reinforcement(
        self, reinforcement: "DStabilityReinforcement"
    ) -> Union[PersistableForbiddenLine, PersistableGeotextile, PersistableNail]:
        internal_datastructure = reinforcement._to_internal_datastructure()
        plural_class_name = f"{reinforcement.__class__.__name__}s"
        getattr(self, plural_class_name).append(internal_datastructure)
        return internal_datastructure


class ProjectInfo(DStabilitySubStructure):
    """projectinfo.json."""

    Analyst: Optional[str] = ""
    ApplicationCreated: Optional[str] = ""
    ApplicationModified: Optional[str] = ""
    ContentVersion: Optional[str] = "1"
    Created: Optional[date] = datetime.now().date()
    CrossSection: Optional[str] = ""
    Date: Optional[date] = datetime.now().date()
    IsDataValidated: Optional[bool] = False
    LastModified: Optional[date] = datetime.now().date()
    LastModifier: Optional[str] = "GEOLib"
    Path: Optional[str] = ""
    Project: Optional[str] = ""
    Remarks: Optional[str] = f"Created with GEOLib {version}"

    @validator("Created", "Date", "LastModified", pre=True, allow_reuse=True)
    def nltime(cls, datestring):
        if isinstance(datestring, str):
            position = datestring.index(max(datestring.split("-"), key=len))
            if position > 0:
                date = datetime.strptime(datestring, "%d-%M-%Y").date()
            else:
                date = datetime.strptime(datestring, "%Y-%M-%d").date()
            return date


class PersistableBondStress(DStabilityBaseModelStructure):
    Sigma: Optional[float]
    Tau: Optional[float]


class PersistableNailPropertiesForSoil(DStabilityBaseModelStructure):
    BondStresses: Optional[List[Optional[PersistableBondStress]]] = []
    CompressionRatio: Optional[float]
    RheologicalCoefficient: Optional[float]
    SoilId: Optional[str]


class NailProperties(DStabilitySubStructure):
    """nailpropertiesforsoils.json"""

    ContentVersion: Optional[str] = "1"
    NailPropertiesForSoils: Optional[
        List[Optional[PersistableNailPropertiesForSoil]]
    ] = []

    @classmethod
    def structure_name(cls) -> str:
        return "nailpropertiesforsoils"


class PersistableConsolidation(DStabilityBaseModelStructure):
    Degree: Optional[float]
    LayerId: Optional[str]


class PersistableEarthquake(DStabilityBaseModelStructure):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]] = []
    FreeWaterFactor: Optional[float] = 0.0
    HorizontalFactor: Optional[float] = 0.0
    IsEnabled: Optional[bool] = False
    VerticalFactor: Optional[float] = 0.0


class PersistableLayerLoad(DStabilityBaseModelStructure):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]] = []
    LayerId: Optional[str]


class PersistableLineLoad(DStabilityBaseModelStructure):
    Angle: Optional[float]
    Consolidations: Optional[List[Optional[PersistableConsolidation]]] = []
    Label: Optional[str]
    Location: Optional[PersistablePoint]
    Magnitude: Optional[float]
    Spread: Optional[float]


class PersistableTree(DStabilityBaseModelStructure):
    Force: Optional[float]
    Label: Optional[str]
    Location: Optional[PersistablePoint]
    RootZoneWidth: Optional[float]
    Spread: Optional[float]


class PersistableUniformLoad(DStabilityBaseModelStructure):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]] = []
    End: Optional[float]
    Label: Optional[str]
    Magnitude: Optional[float]
    Spread: Optional[float]
    Start: Optional[float]


Load = Union[PersistableUniformLoad, PersistableLineLoad, PersistableLayerLoad]


class Loads(DStabilitySubStructure):
    """loads/loads_x.json"""

    Id: Optional[str]
    ContentVersion: Optional[str] = "1"
    Earthquake: Optional[PersistableEarthquake] = PersistableEarthquake()
    LayerLoads: Optional[List[Optional[PersistableLayerLoad]]] = []
    LineLoads: Optional[List[Optional[PersistableLineLoad]]] = []
    Trees: Optional[List[Optional[PersistableTree]]] = []
    UniformLoads: Optional[List[Optional[PersistableUniformLoad]]] = []

    def add_load(
        self, load: "DStabilityLoad", consolidations: List["Consolidation"]
    ) -> Union[PersistableUniformLoad, PersistableLineLoad, PersistableLayerLoad]:
        internal_datastructure = load.to_internal_datastructure()

        # Add consolidations if the load supports it
        if hasattr(internal_datastructure, "Consolidations"):
            internal_datastructure.Consolidations = [
                c.to_internal_datastructure() for c in consolidations
            ]

        target = load.__class__.__name__
        if target == "Earthquake":
            setattr(self, target, internal_datastructure)
        else:
            target += "s"
            getattr(self, target).append(internal_datastructure)

        return internal_datastructure

    def add_layer_load(
        self, soil_layer_id: int, consolidations: List["Consolidation"]
    ) -> PersistableLayerLoad:
        layer_load = PersistableLayerLoad(
            LayerId=str(soil_layer_id),
            Consolidations=[c.to_internal_datastructure() for c in consolidations],
        )
        self.LayerLoads.append(layer_load)
        return layer_load


class PersistableLayer(DStabilityBaseModelStructure):
    Id: Optional[str]
    Label: Optional[str]
    Notes: Optional[str]
    Points: conlist(PersistablePoint, min_items=3)

    @validator("Points", pre=True, allow_reuse=True)
    def polygon_checks(cls, points):
        """
        Todo:
            Find a way to check the validity of the given points
        """
        # implement some checks
        # 1. is this a simple polygon
        # 2. is it clockwise
        # 3. is it a non closed polygon
        # 4. does it intersect other polygons
        return points


class Geometry(DStabilitySubStructure):
    """geometries/geometry_x.json"""

    @classmethod
    def structure_group(cls) -> str:
        return "geometries"

    ContentVersion: Optional[str] = "1"
    Id: Optional[str]
    Layers: List[PersistableLayer] = []

    def contains_point(self, point: Point) -> bool:
        """
        Check if the given point is on one of the points of the layers

        Args:
            point (Point): A point type

        Returns:
            bool: True if this point is found on a layer, False otherwise

        Todo:
            Take x, z accuracy into account
        """
        for layer in self.Layers:
            for p in layer.Points:
                if point.x == p.X and point.z == p.Z:  # not nice
                    return True

        return False

    def get_layer(self, id: int) -> PersistableLayer:
        for layer in self.Layers:
            if layer.Id == str(id):
                return layer

        raise ValueError(f"Layer id {id} not found in this geometry")

    def add_layer(
        self, id: str, label: str, notes: str, points: List[Point]
    ) -> PersistableLayer:
        """
        Add a new layer to the model. Layers are expected;
        1. to contain at least 3 point (non closed polygons)
        2. the points need to be in clockwise order
        3. the polygon needs to be convex (no intersections with itsself)

        Args:
            id (str): id of the layer
            label (str): label of the layer
            notes (str): notes for the layers
            points (List[Points]): list of Point classes

        Returns:
            PersistableLayer: the layer as a persistable object
        """
        layer = PersistableLayer(
            Id=id,
            Label=label,
            Notes=notes,
            Points=[PersistablePoint(X=p.x, Z=p.z) for p in points],
        )

        self.Layers.append(layer)
        return layer


class PersistableBerm(DStabilityBaseModelStructure):
    AddedLayerId: Optional[str]
    Label: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class PersistableExcavation(DStabilityBaseModelStructure):
    Label: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class Decorations(DStabilitySubStructure):
    """decorations/decorations_x.json."""

    Berms: Optional[List[Optional[PersistableBerm]]] = []
    ContentVersion: Optional[str] = "1"
    Excavations: Optional[List[Optional[PersistableExcavation]]] = []
    Id: Optional[str]


# Calculation Settings


class PersistableCircle(DStabilityBaseModelStructure):
    Center: Optional[PersistablePoint] = PersistablePoint()
    Radius: Optional[float] = "NaN"


class PersistableBishopSettings(DStabilityBaseModelStructure):
    Circle: Optional[PersistableCircle] = PersistableCircle()


class PersistableGridEnhancements(DStabilityBaseModelStructure):
    ExtrapolateSearchSpace: Optional[bool] = True


class NullablePersistablePoint(DStabilityBaseModelStructure):
    X: Optional[float] = "NaN"
    Z: Optional[float] = "NaN"


class PersistableSearchGrid(DStabilityBaseModelStructure):
    BottomLeft: Optional[NullablePersistablePoint] = None
    NumberOfPointsInX: Optional[int] = 1
    NumberOfPointsInZ: Optional[int] = 1
    Space: Optional[float] = 1.0


class PersistableSlipPlaneConstraints(DStabilityBaseModelStructure):
    IsSizeConstraintsEnabled: Optional[bool] = False
    IsZoneAConstraintsEnabled: Optional[bool] = False
    IsZoneBConstraintsEnabled: Optional[bool] = False
    MinimumSlipPlaneDepth: Optional[float] = 0.0
    MinimumSlipPlaneLength: Optional[float] = 0.0
    WidthZoneA: Optional[float] = 0.0
    WidthZoneB: Optional[float] = 0.0
    XLeftZoneA: Optional[float] = 0.0
    XLeftZoneB: Optional[float] = 0.0


class PersistableTangentLines(DStabilityBaseModelStructure):
    BottomTangentLineZ: Optional[float] = "NaN"
    NumberOfTangentLines: Optional[int] = 1
    Space: Optional[float] = 0.5


class PersistableBishopBruteForceSettings(DStabilityBaseModelStructure):
    GridEnhancements: Optional[
        PersistableGridEnhancements
    ] = PersistableGridEnhancements()
    SearchGrid: Optional[PersistableSearchGrid] = PersistableSearchGrid()
    SlipPlaneConstraints: Optional[
        PersistableSlipPlaneConstraints
    ] = PersistableSlipPlaneConstraints()
    TangentLines: Optional[PersistableTangentLines] = PersistableTangentLines()


class CalculationTypeEnum(Enum):
    DESIGN = "Design"
    DETERMINISTIC = "Deterministic"
    MEAN = "Mean"
    PROBABILISTIC = "Probabilistic"


CalculationType = CalculationTypeEnum


class PersistableSpencerSettings(DStabilityBaseModelStructure):
    SlipPlane: Optional[List[Optional[PersistablePoint]]] = None


class OptionsTypeEnum(Enum):
    DEFAULT = "Default"
    THOROUGH = "Thorough"


OptionsType = OptionsTypeEnum


class PersistableGeneticSlipPlaneConstraints(DStabilityBaseModelStructure):
    IsEnabled: Optional[bool] = False
    MinimumAngleBetweenSlices: Optional[float] = 0.0
    MinimumThrustLinePercentageInsideSlices: Optional[float] = 0.0


class PersistableSpencerGeneticSettings(DStabilityBaseModelStructure):
    OptionsType: Optional[OptionsTypeEnum] = OptionsType.DEFAULT
    SlipPlaneA: Optional[List[Optional[PersistablePoint]]] = None
    SlipPlaneB: Optional[List[Optional[PersistablePoint]]] = None
    SlipPlaneConstraints: Optional[
        PersistableGeneticSlipPlaneConstraints
    ] = PersistableGeneticSlipPlaneConstraints()


class PersistableTwoCirclesOnTangentLine(DStabilityBaseModelStructure):
    FirstCircleCenter: Optional[NullablePersistablePoint] = NullablePersistablePoint()
    FirstCircleRadius: Optional[float] = "NaN"
    SecondCircleCenter: Optional[NullablePersistablePoint] = NullablePersistablePoint()


class PersistableUpliftVanSettings(DStabilityBaseModelStructure):
    SlipPlane: Optional[
        PersistableTwoCirclesOnTangentLine
    ] = PersistableTwoCirclesOnTangentLine()


class PersistableSearchArea(DStabilityBaseModelStructure):
    Height: Optional[float] = 0.0
    TopLeft: Optional[NullablePersistablePoint] = None
    Width: Optional[float] = 0.0


class PersistableTangentArea(DStabilityBaseModelStructure):
    Height: Optional[float] = 0.0
    TopZ: Optional[float] = None


class PersistableUpliftVanParticleSwarmSettings(DStabilityBaseModelStructure):
    OptionsType: Optional[OptionsTypeEnum] = OptionsType.DEFAULT
    SearchAreaA: Optional[PersistableSearchArea] = PersistableSearchArea()
    SearchAreaB: Optional[PersistableSearchArea] = PersistableSearchArea()
    SlipPlaneConstraints: Optional[
        PersistableSlipPlaneConstraints
    ] = PersistableSlipPlaneConstraints()
    TangentArea: Optional[PersistableTangentArea] = PersistableTangentArea()


class CalculationSettings(DStabilitySubStructure):
    """calculationsettings/calculationsettings_x.json"""

    AnalysisType: Optional[AnalysisTypeEnum]
    Bishop: Optional[PersistableBishopSettings] = PersistableBishopSettings()
    BishopBruteForce: Optional[
        PersistableBishopBruteForceSettings
    ] = PersistableBishopBruteForceSettings()
    CalculationType: Optional[CalculationTypeEnum] = CalculationTypeEnum.DETERMINISTIC
    ContentVersion: Optional[str] = "1"
    Id: Optional[str] = "19"
    ModelFactorMean: Optional[float] = 1.05
    ModelFactorStandardDeviation: Optional[float] = 0.033
    Spencer: Optional[PersistableSpencerSettings] = PersistableSpencerSettings()
    SpencerGenetic: Optional[
        PersistableSpencerGeneticSettings
    ] = PersistableSpencerGeneticSettings()
    UpliftVan: Optional[PersistableUpliftVanSettings] = PersistableUpliftVanSettings()
    UpliftVanParticleSwarm: Optional[
        PersistableUpliftVanParticleSwarmSettings
    ] = PersistableUpliftVanParticleSwarmSettings()

    def set_bishop(self, bishop_settings: PersistableBishopSettings) -> None:
        self.Bishop = bishop_settings
        self.AnalysisType = AnalysisType.BISHOP

    def set_bishop_brute_force(
        self, bishop_brute_force_settings: PersistableBishopBruteForceSettings
    ) -> None:
        self.BishopBruteForce = bishop_brute_force_settings
        self.AnalysisType = AnalysisType.BISHOP_BRUTE_FORCE

    def set_spencer(self, spencer_settings: PersistableSpencerSettings) -> None:
        self.Spencer = spencer_settings
        self.AnalysisType = AnalysisType.SPENCER

    def set_spencer_genetic(
        self, spencer_genetic_settings: PersistableSpencerGeneticSettings
    ) -> None:
        self.SpencerGenetic = spencer_genetic_settings
        self.AnalysisType = AnalysisType.SPENCER_GENETIC

    def set_uplift_van(self, uplift_van_settings: PersistableUpliftVanSettings) -> None:
        self.UpliftVan = uplift_van_settings
        self.AnalysisType = AnalysisType.UPLIFT_VAN

    def set_uplift_van_particle_swarm(
        self,
        uplift_van_particle_swarm_settings: PersistableUpliftVanParticleSwarmSettings,
    ) -> None:
        self.UpliftVanParticleSwarm = uplift_van_particle_swarm_settings
        self.AnalysisType = AnalysisType.UPLIFT_VAN_PARTICLE_SWARM


########
# OUTPUT
########


class PersistableSlice(DStabilityBaseModelStructure):
    ArcLength: Optional[float] = None
    BottomAngle: Optional[float] = None
    BottomLeft: Optional[PersistablePoint] = None
    BottomRight: Optional[PersistablePoint] = None
    CohesionInput: Optional[float] = None
    CohesionOutput: Optional[float] = None
    DegreeOfConsolidationLoadPorePressure: Optional[float] = None
    DegreeOfConsolidationPorePressure: Optional[float] = None
    DilatancyInput: Optional[float] = None
    DilatancyOutput: Optional[float] = None
    EffectiveStress: Optional[float] = None
    HorizontalPorePressure: Optional[float] = None
    HorizontalSoilQuakeStress: Optional[float] = None
    HydrostaticPorePressure: Optional[float] = None
    Label: Optional[str] = None
    LoadStress: Optional[float] = None
    MInput: Optional[float] = None
    NormalStress: Optional[float] = None
    Ocr: Optional[float] = None
    PhiInput: Optional[float] = None
    PhiOutput: Optional[float] = None
    PiezometricPorePressure: Optional[float] = None
    Pop: Optional[float] = None
    ShearStress: Optional[float] = None
    SInput: Optional[float] = None
    SuOutput: Optional[float] = None
    SurfacePorePressure: Optional[float] = None
    TopAngle: Optional[float] = None
    TopLeft: Optional[PersistablePoint] = None
    TopRight: Optional[PersistablePoint] = None
    TotalPorePressure: Optional[float] = None
    TotalStress: Optional[float] = None
    UpliftFactor: Optional[float] = None
    VerticalPorePressure: Optional[float] = None
    VerticalSoilQuakeStress: Optional[float] = None
    WaterQuakeStress: Optional[float] = None
    Weight: Optional[float] = None
    Width: Optional[float] = None
    YieldStress: Optional[float] = None
    ShearStrengthModelType: Optional[ShearStrengthModelTypePhreaticLevelInternal] = None


class BishopBruteForceResult(DStabilitySubStructure):
    Circle: Optional[PersistableCircle] = None
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSlice]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/bishopbruteforce/"

    def get_slipcircle_output(self) -> BishopSlipCircleResult:
        """Get condensed slipcircle data"""
        try:
            return BishopSlipCircleResult(
                x=self.Circle.Center.X, z=self.Circle.Center.Z, radius=self.Circle.Radius
            )
        except (ValidationError, AttributeError):
            raise ValueError(
                f"Slipcircle not available for {self.__class__.__name__} with id {self.Id}"
            )


class PersistableSoilContribution(DStabilityBaseModelStructure):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    SoilId: Optional[str] = None
    Value: Optional[float] = None


class PersistableStageContribution(DStabilityBaseModelStructure):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    StageId: Optional[str] = None
    Value: Optional[float] = None


class PersistableStateLinePointContribution(DStabilityBaseModelStructure):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    StateLinePointId: Optional[str] = None
    Value: Optional[float] = None


class PersistableStatePointContribution(DStabilityBaseModelStructure):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    StatePointId: Optional[str] = None
    Value: Optional[float] = None


class BishopReliabilityResult(DStabilitySubStructure):
    Circle: Optional[PersistableCircle] = None
    Converged: Optional[bool] = None
    FailureProbability: Optional[float] = None
    Id: Optional[str] = None
    ReliabilityIndex: Optional[float] = None
    SoilContributions: Optional[List[Optional[PersistableSoilContribution]]] = None
    StageContributions: Optional[List[Optional[PersistableStageContribution]]] = None
    StateLinePointContributions: Optional[
        List[Optional[PersistableStateLinePointContribution]]
    ] = None
    StatePointContributions: Optional[
        List[Optional[PersistableStatePointContribution]]
    ] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/bishopreliability/"

    def get_slipcircle_output(self) -> BishopSlipCircleResult:
        """Get condensed slipcircle data"""
        try:
            return BishopSlipCircleResult(
                x=self.Circle.Center.X, z=self.Circle.Center.Z, radius=self.Circle.Radius
            )
        except (ValidationError, AttributeError):
            raise ValueError(
                f"Slipcircle not available for {self.__class__.__name__} with id {self.Id}"
            )


class BishopResult(DStabilitySubStructure):
    Circle: Optional[PersistableCircle] = None
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSlice]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/bishop/"

    def get_slipcircle_output(self) -> BishopSlipCircleResult:
        """Get condensed slipcircle data"""
        try:
            return BishopSlipCircleResult(
                x=self.Circle.Center.X, z=self.Circle.Center.Z, radius=self.Circle.Radius
            )
        except (ValidationError, AttributeError):
            raise ValueError(
                f"Slipcircle not available for {self.__class__.__name__} with id {self.Id}"
            )


class PersistableSpencerSlice(DStabilityBaseModelStructure):
    ArcLength: Optional[float] = None
    BottomAngle: Optional[float] = None
    BottomLeft: Optional[PersistablePoint] = None
    BottomRight: Optional[PersistablePoint] = None
    CohesionInput: Optional[float] = None
    CohesionOutput: Optional[float] = None
    DegreeOfConsolidationLoadPorePressure: Optional[float] = None
    DegreeOfConsolidationPorePressure: Optional[float] = None
    DilatancyInput: Optional[float] = None
    DilatancyOutput: Optional[float] = None
    EffectiveStress: Optional[float] = None
    HorizontalPorePressure: Optional[float] = None
    HorizontalSoilQuakeStress: Optional[float] = None
    HydrostaticPorePressure: Optional[float] = None
    Label: Optional[str] = None
    LeftForce: Optional[float] = None
    LeftForceAngle: Optional[float] = None
    LeftForceY: Optional[float] = None
    LoadStress: Optional[float] = None
    MInput: Optional[float] = None
    NormalStress: Optional[float] = None
    Ocr: Optional[float] = None
    PhiInput: Optional[float] = None
    PhiOutput: Optional[float] = None
    PiezometricPorePressure: Optional[float] = None
    Pop: Optional[float] = None
    RightForce: Optional[float] = None
    RightForceAngle: Optional[float] = None
    RightForceY: Optional[float] = None
    ShearStress: Optional[float] = None
    SInput: Optional[float] = None
    SuOutput: Optional[float] = None
    SurfacePorePressure: Optional[float] = None
    TopAngle: Optional[float] = None
    TopLeft: Optional[PersistablePoint] = None
    TopRight: Optional[PersistablePoint] = None
    TotalPorePressure: Optional[float] = None
    TotalStress: Optional[float] = None
    UpliftFactor: Optional[float] = None
    VerticalPorePressure: Optional[float] = None
    VerticalSoilQuakeStress: Optional[float] = None
    WaterQuakeStress: Optional[float] = None
    Weight: Optional[float] = None
    Width: Optional[float] = None
    YieldStress: Optional[float] = None
    ShearStrengthModelType: Optional[ShearStrengthModelTypePhreaticLevelInternal] = None


class SpencerGeneticAlgorithmResult(DStabilitySubStructure):
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSpencerSlice]]] = None
    SlipPlane: Optional[List[Optional[PersistablePoint]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/spencergeneticalgorithm/"

    def get_slipplane_output(self) -> SpencerSlipPlaneResult:
        """Get condensed slipplane data"""
        try:
            return SpencerSlipPlaneResult(
                slipplane=[Point(x=p.X, z=p.Z) for p in self.SlipPlane]
            )
        except (ValidationError, TypeError):
            raise ValueError(
                f"Slip plane not available for {self.__class__.__name__} with id {self.Id}"
            )


class SpencerReliabilityResult(DStabilitySubStructure):
    Converged: Optional[bool] = None
    FailureProbability: Optional[float] = None
    Id: Optional[str] = None
    ReliabilityIndex: Optional[float] = None
    SlipPlane: Optional[List[Optional[PersistablePoint]]] = None
    SoilContributions: Optional[List[Optional[PersistableSoilContribution]]] = None
    StageContributions: Optional[List[Optional[PersistableStageContribution]]] = None
    StateLinePointContributions: Optional[
        List[Optional[PersistableStateLinePointContribution]]
    ] = None
    StatePointContributions: Optional[
        List[Optional[PersistableStatePointContribution]]
    ] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/spencerreliability/"

    def get_slipplane_output(self) -> SpencerSlipPlaneResult:
        """Get condensed slipplane data"""
        try:
            return SpencerSlipPlaneResult(
                slipplane=[Point(x=p.X, z=p.Z) for p in self.SlipPlane]
            )
        except (ValidationError, TypeError):
            raise ValueError(
                f"Slip plane not available for {self.__class__.__name__} with id {self.Id}"
            )


class SpencerResult(DStabilitySubStructure):
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSpencerSlice]]] = None
    SlipPlane: Optional[List[Optional[PersistablePoint]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/spencer/"

    def get_slipplane_output(self) -> SpencerSlipPlaneResult:
        """Get condensed slipplane data"""
        try:
            return SpencerSlipPlaneResult(
                slipplane=[Point(x=p.X, z=p.Z) for p in self.SlipPlane]
            )
        except (ValidationError, TypeError):
            raise ValueError(
                f"Slip plane not available for {self.__class__.__name__} with id {self.Id}"
            )


class UpliftVanParticleSwarmResult(DStabilitySubStructure):
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    LeftCenter: Optional[PersistablePoint] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    RightCenter: Optional[PersistablePoint] = None
    Slices: Optional[List[Optional[PersistableSlice]]] = None
    TangentLine: Optional[float] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/upliftvanparticleswarm/"

    def get_slipcircle_output(self) -> UpliftVanSlipCircleResult:
        """Get condensed slipplane data"""
        try:
            return UpliftVanSlipCircleResult(
                x_left=self.LeftCenter.X,
                z_left=self.LeftCenter.Z,
                x_right=self.RightCenter.X,
                z_right=self.RightCenter.Z,
                z_tangent=self.TangentLine,
            )
        except (ValidationError, AttributeError):
            raise ValueError(
                f"Slipcircle not available for {self.__class__.__name__} with id {self.Id}"
            )


class UpliftVanReliabilityResult(DStabilitySubStructure):
    Converged: Optional[bool] = None
    FailureProbability: Optional[float] = None
    Id: Optional[str] = None
    LeftCenter: Optional[PersistablePoint] = None
    ReliabilityIndex: Optional[float] = None
    RightCenter: Optional[PersistablePoint] = None
    SoilContributions: Optional[List[Optional[PersistableSoilContribution]]] = None
    StageContributions: Optional[List[Optional[PersistableStageContribution]]] = None
    StateLinePointContributions: Optional[
        List[Optional[PersistableStateLinePointContribution]]
    ] = None
    StatePointContributions: Optional[
        List[Optional[PersistableStatePointContribution]]
    ] = None
    TangentLine: Optional[float] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/upliftvanreliability/"

    def get_slipcircle_output(self) -> UpliftVanSlipCircleResult:
        """Get condensed slipcircle data"""
        try:
            return UpliftVanSlipCircleResult(
                x_left=self.LeftCenter.X,
                z_left=self.LeftCenter.Z,
                x_right=self.RightCenter.X,
                z_right=self.RightCenter.Z,
                z_tangent=self.TangentLine,
            )
        except (ValidationError, AttributeError):
            raise ValueError(
                f"Slipcircle not available for {self.__class__.__name__} with id {self.Id}"
            )


class UpliftVanResult(DStabilitySubStructure):
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    LeftCenter: Optional[PersistablePoint] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    RightCenter: Optional[PersistablePoint] = None
    Slices: Optional[List[Optional[PersistableSlice]]] = None
    TangentLine: Optional[float] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/upliftvan/"

    def get_slipcircle_output(self) -> UpliftVanSlipCircleResult:
        """Get condensed slipcircle data"""
        try:
            return UpliftVanSlipCircleResult(
                x_left=self.LeftCenter.X,
                z_left=self.LeftCenter.Z,
                x_right=self.RightCenter.X,
                z_right=self.RightCenter.Z,
                z_tangent=self.TangentLine,
            )
        except (ValidationError, AttributeError):
            raise ValueError(
                f"Slipcircle not available for {self.__class__.__name__} with id {self.Id}"
            )


DStabilityResult = Union[
    UpliftVanResult,
    UpliftVanParticleSwarmResult,
    UpliftVanReliabilityResult,
    SpencerGeneticAlgorithmResult,
    SpencerReliabilityResult,
    SpencerResult,
    BishopBruteForceResult,
    BishopReliabilityResult,
    BishopResult,
]

###########################
# INPUT AND OUTPUT COMBINED
###########################


class DStabilityStructure(BaseModelStructure):
    """Highest level DStability class that should be parsed to and serialized from.

    The List[] items (one for each stage in the model) will be stored in a subfolder
    to multiple json files. Where the first (0) instance
    has no suffix, but the second one has (1 => _1) etc.

    also parses the outputs which are part of the json files
    """

    # input part
    waternets: List[Waternet] = [Waternet(Id="14")]  # waternets/waternet_x.json
    waternetcreatorsettings: List[WaternetCreatorSettings] = [
        WaternetCreatorSettings(Id="15")
    ]  # waternetcreatorsettings/waternetcreatorsettings_x.json
    states: List[State] = [State(Id="16")]  # states/states_x.json
    statecorrelations: List[StateCorrelation] = [
        StateCorrelation(Id="17")
    ]  # statecorrelations/statecorrelations_x.json
    stages: List[Stage] = [
        Stage(
            CalculationSettingsId="20",
            DecorationsId="12",
            GeometryId="11",
            Id="0",
            Label="Stage 1",
            LoadsId="18",
            Notes="Default stage by GEOLib",
            ReinforcementsId="19",
            SoilLayersId="13",
            StateId="16",
            StateCorrelationsId="17",
            WaternetCreatorSettingsId="15",
            WaternetId="14",
        )
    ]  # stages/stage_x.json
    soillayers: List[SoilLayerCollection] = [
        SoilLayerCollection(Id="13")
    ]  # soillayers/soillayers_x.json
    soilcorrelation: SoilCorrelation = SoilCorrelation()  # soilcorrelations.json
    soils: SoilCollection = SoilCollection()  # soils.json
    soilvisualizations: SoilVisualisation = SoilVisualisation()  # soilvisualizations.json
    reinforcements: List[Reinforcements] = [
        Reinforcements(Id="19")
    ]  # reinforcements/reinforcements_x.json
    projectinfo: ProjectInfo = ProjectInfo()  # projectinfo.json
    nailproperties: NailProperties = NailProperties()  # nailpropertiesforsoils.json
    loads: List[Loads] = [Loads(Id="18")]  # loads/loads_x.json
    decorations: List[Decorations] = [
        Decorations(Id="12")
    ]  # decorations/decorations_x.json
    calculationsettings: List[CalculationSettings] = [
        CalculationSettings(Id="20")
    ]  # calculationsettings/calculationsettings_x.json
    geometries: List[Geometry] = [Geometry(Id="11")]  # geometries/geometry_x.json

    # Output parts
    uplift_van_results: List[UpliftVanResult] = []
    uplift_van_particle_swarm_results: List[UpliftVanParticleSwarmResult] = []
    uplift_van_reliability_results: List[UpliftVanReliabilityResult] = []
    spencer_genetic_algorithm_results: List[SpencerGeneticAlgorithmResult] = []
    spencer_reliability_results: List[SpencerReliabilityResult] = []
    spencer_results: List[SpencerResult] = []
    bishop_bruteforce_results: List[BishopBruteForceResult] = []
    bishop_reliability_results: List[BishopReliabilityResult] = []
    bishop_results: List[BishopResult] = []

    class Config:
        arbitrary_types_allowed = True
        validate_assignment = True
        extra: "forbid"

    @root_validator(skip_on_failure=True, allow_reuse=True)
    def ensure_validaty_foreign_keys(cls, values):
        """TODO Include more fk relations, left for another issue."""
        for i, stage in enumerate(values.get("stages")):
            if not values.get("stages")[i].GeometryId == values.get("geometries")[i].Id:
                raise ValueError("Ids not linked!")
        return values

    @property
    def stage_specific_fields(self):
        return [
            "waternets",
            "waternetcreatorsettings",
            "states",
            "statecorrelations",
            "stages",
            "soillayers",
            "reinforcements",
            "loads",
            "decorations",
            "calculationsettings",
            "geometries",
        ]

    def get_stage_specific_fields(self, stage=0) -> Tuple[str, DStabilitySubStructure]:
        """Yield stage specific fields for given stage."""
        for fieldname in self.stage_specific_fields:
            field = getattr(self, fieldname)
            if len(field) > stage:
                yield fieldname, field[stage]

    def renumber_fk_fields(self, instance, mapping: Dict, unique_id: int) -> int:
        """Replace id (foreign key) fields on instance based on a mapping and unique id."""
        fk = ForeignKeys()
        fkfields = fk.class_fields

        def get_correct_key(key, mapping):
            if key not in mapping:
                nonlocal unique_id
                mapping[key] = unique_id
                unique_id += 1
            return mapping[key]

        for fkfield in fkfields.get(instance.__class__.__name__, []):
            value = getattr(instance, fkfield)
            if isinstance(value, (list, set, tuple)):
                setattr(
                    instance, fkfield, [get_correct_key(x, mapping) for x in value],
                )
            if isinstance(value, (int, float, str)):
                setattr(instance, fkfield, get_correct_key(value, mapping))

        return unique_id

    def duplicate_stage(
        self, current_stage: int, label: str, notes: str, unique_start_id: int
    ):
        """Duplicates an existing stage.
        Copies the specific stage fields for a stage and renumbers all Ids,
        taking into account foreign keys by using the same renumbering.
        """

        old_to_new = {}
        for fieldname, stagefield in self.get_stage_specific_fields(current_stage):
            newstagefield = stagefield.copy(deep=True)

            # Renumber the upper class
            unique_start_id = self.renumber_fk_fields(
                newstagefield, old_to_new, unique_start_id
            )
            # Renumber all children
            for classinstance in children(newstagefield):
                unique_start_id = self.renumber_fk_fields(
                    classinstance, old_to_new, unique_start_id
                )

            # Update the stage with extra supplied fields
            if fieldname == "stages":
                newstagefield.Label = label
                newstagefield.Notes = notes

            getattr(self, fieldname).append(newstagefield)

        return len(self.stages) - 1, unique_start_id

    def add_default_stage(self, label: str, notes: str, unique_start_id=500) -> int:
        """Add a new default (empty) stage to DStability."""
        self.waternets += [Waternet(Id=str(unique_start_id + 1))]
        self.waternetcreatorsettings += [
            WaternetCreatorSettings(Id=str(unique_start_id + 2))
        ]
        self.states += [State(Id=str(unique_start_id + 3))]
        self.statecorrelations += [StateCorrelation(Id=str(unique_start_id + 4))]
        self.stages += [
            Stage(
                CalculationSettingsId=str(unique_start_id + 10),
                DecorationsId=str(unique_start_id + 9),
                GeometryId=str(unique_start_id + 8),
                Id=str(unique_start_id),
                Label=label,
                LoadsId=str(unique_start_id + 7),
                Notes=notes,
                ReinforcementsId=str(unique_start_id + 6),
                SoilLayersId=str(unique_start_id + 5),
                StateId=str(unique_start_id + 3),
                StateCorrelationsId=str(unique_start_id + 4),
                WaternetCreatorSettingsId=str(unique_start_id + 2),
                WaternetId=str(unique_start_id + 1),
            )
        ]
        self.soillayers += [SoilLayerCollection(Id=str(unique_start_id + 5))]
        self.soilcorrelation: SoilCorrelation = SoilCorrelation()
        self.reinforcements += [Reinforcements(Id=str(unique_start_id + 6))]
        self.loads += [Loads(Id=str(unique_start_id + 7))]
        self.decorations += [Decorations(Id=str(unique_start_id + 9))]
        self.calculationsettings += [CalculationSettings(Id=str(unique_start_id + 10))]
        self.geometries += [Geometry(Id=str(unique_start_id + 8))]

        return len(self.stages) - 1, unique_start_id + 11

    def get_unique_id(self) -> int:
        """Return unique id that can be used in DStability.
        Finds all existing ids, takes the max and does +1.
        """

        fk = ForeignKeys()
        classfields = fk.class_fields

        ids = []
        for instance in children(self):
            for field in classfields.get(instance.__class__.__name__, []):
                value = getattr(instance, field)
                if isinstance(value, (list, set, tuple)):
                    ids.extend(value)
                if isinstance(value, (int, float, str)):
                    ids.append(value)

        new_id = max({int(id) for id in ids if id is not None}) + 1
        return new_id

    def validator(self):
        return DStabilityValidator(self)

    def has_stage(self, stage_id: int) -> bool:
        try:
            self.stages[stage_id]
            return True
        except IndexError:
            return False

    def has_result(self, stage_id: int) -> bool:
        if self.has_stage(stage_id):
            result_id = self.stages[stage_id].ResultId
            if result_id is None:
                return False
            else:
                return True
        return False

    def has_loads(self, stage_id: int) -> bool:
        if self.has_stage(stage_id):
            loads_id = self.stages[stage_id].LoadsId
            if loads_id is None:
                return False
            else:
                return True
        return False

    def has_soil_layers(self, stage_id: int) -> bool:
        if self.has_stage(stage_id):
            soil_layers_id = self.stages[stage_id].SoilLayersId
            if soil_layers_id is None:
                return False
            else:
                return True
        return False

    def has_soil_layer(self, stage_id: int, soil_layer_id: int) -> bool:
        if self.has_soil_layers(stage_id):
            for layer in self.soillayers[stage_id].SoilLayers:
                if str(soil_layer_id) == layer.LayerId:
                    return True
            return False
        return False

    def has_reinforcements(self, stage_id: int) -> bool:
        if self.has_stage(stage_id):
            reinforcements_id = self.stages[stage_id].ReinforcementsId
            if reinforcements_id is None:
                return False
            else:
                return True
        return False

    def get_result_substructure(
        self, analysis_type: AnalysisTypeEnum, calculation_type: CalculationTypeEnum
    ) -> List[DStabilityResult]:

        result_types_mapping = {
            AnalysisTypeEnum.UPLIFT_VAN: {
                "non_probabilistic": self.uplift_van_results,
                "probabilistic": self.uplift_van_reliability_results,
            },
            AnalysisTypeEnum.UPLIFT_VAN_PARTICLE_SWARM: {
                "non_probabilistic": self.uplift_van_particle_swarm_results,
                "probabilistic": self.uplift_van_reliability_results,
            },
            AnalysisTypeEnum.SPENCER_GENETIC: {
                "non_probabilistic": self.spencer_genetic_algorithm_results,
                "probabilistic": self.spencer_reliability_results,
            },
            AnalysisTypeEnum.SPENCER: {
                "non_probabilistic": self.spencer_results,
                "probabilistic": self.spencer_reliability_results,
            },
            AnalysisTypeEnum.BISHOP_BRUTE_FORCE: {
                "non_probabilistic": self.bishop_bruteforce_results,
                "probabilistic": self.bishop_reliability_results,
            },
            AnalysisTypeEnum.BISHOP: {
                "non_probabilistic": self.bishop_results,
                "probabilistic": self.bishop_reliability_results,
            },
        }

        if calculation_type == CalculationTypeEnum.PROBABILISTIC:
            return result_types_mapping[analysis_type]["probabilistic"]

        return result_types_mapping[analysis_type]["non_probabilistic"]


class ForeignKeys(DStabilityBaseModelStructure):
    """A dataclass that store the connections between the
    various unique Ids used in DStability. These can be seen
    as (implicit) foreign keys.
    """

    mapping: Dict[str, Tuple[str, ...]] = {
        "Waternet.Id": ("Stage.WaternetId",),
        "PersistableHeadLine.Id": (
            "PersistableReferenceLine.BottomHeadLineId",
            "PersistableReferenceLine.TopHeadLineId",
        ),
        "PersistableReferenceLine.Id": ("Waternet.PhreaticLineId",),
        "PersistableLayer.Id": (
            "PersistableStatePoint.LayerId",
            "PersistableSoilLayer.LayerId",
            "PersistableConsolidation.LayerId",
            "PersistableLayerLoad.LayerId",
            "PersistableBerm.AddedLayerId",
            "WaternetCreatorSettings.AquiferInsideAquitardLayerId",
            "WaternetCreatorSettings.AquiferLayerId",
        ),
        # Soil commented out for now, isn't used in stages
        # "PersistableSoil.Id": (
        #     "PersistableSoilVisualization.SoilId",
        #     "PersistableSoilLayer.SoilId",
        #     "PersistableSoilCorrelation.CorrelatedSoilIds",
        #     "PersistableNailPropertiesForSoil.SoilId",
        #     "PersistableSoilContribution.SoilId"
        # ),
        "CalculationSettings.Id": ("Stage.CalculationSettingsId",),
        "Decorations.Id": ("Stage.DecorationsId",),
        "Geometry.Id": ("Stage.GeometryId",),
        "Loads.Id": ("Stage.LoadsId",),
        "Reinforcements.Id": ("Stage.ReinforcementsId",),
        "Result.Id": ("Stage.ResultId",),
        "SoilLayerCollection.Id": ("Stage.SoilLayersId",),
        "StateCorrelation.Id": ("Stage.StateCorrelationsId",),
        "State.Id": ("Stage.StateId",),
        "WaternetCreatorSettings.Id": ("Stage.WaternetCreatorSettingsId",),
        "Stage.Id": ("PersistableStageContribution.StageId",),
        "PersistableStateLinePoint.Id": (
            "PersistableStateCorrelation.CorrelatedStateIds",
            "PersistableStateLinePointContribution.StateLinePointId",
        ),
        "PersistableStatePoint.Id": ("PersistableStatePointContribution.StatePointId",),
    }

    @property
    def class_fields(self) -> Dict[str, List[str]]:
        """Return a mapping in the form:
        classname: [fields]
        """
        id_keys = chain(*((k, *v) for k, v in self.mapping.items()))
        class_fields = defaultdict(list)
        for id_key in id_keys:
            classname, fieldname = id_key.split(".")
            class_fields[classname].append(fieldname)
        return class_fields
