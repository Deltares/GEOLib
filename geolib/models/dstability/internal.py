"""
The internal data model structure.
"""

from collections import defaultdict
from datetime import date, datetime
from enum import Enum
from itertools import chain
from math import isfinite

from pydantic import Field, ValidationError, field_validator, model_validator
from typing_extensions import Annotated

from geolib import __version__ as version
from geolib.geometry import Point
from geolib.models.base_model_structure import BaseModelStructure
from geolib.soils import Soil

from .dstability_validator import DStabilityValidator
from .utils import children


class DStabilityBaseModelStructure(BaseModelStructure):
    def dict(_, *args, **kwargs):
        data = super().model_dump(*args, **kwargs)
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
    slipplane: list[Point]


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
    X: float | str | None = "NaN"
    Z: float | str | None = "NaN"


class PersistableHeadLine(DStabilityBaseModelStructure):
    Id: str | None = None
    Label: str | None = ""
    Notes: str | None = ""
    Points: list[PersistablePoint | None] | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableReferenceLine(DStabilityBaseModelStructure):
    BottomHeadLineId: str | None = None
    Id: str | None = None
    Label: str | None = ""
    Notes: str | None = ""
    Points: list[PersistablePoint | None] | None = None
    TopHeadLineId: str | None = None

    @field_validator("Id", "TopHeadLineId", "BottomHeadLineId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class Waternet(DStabilitySubStructure):
    """waternets/waternet_x.json."""

    @classmethod
    def structure_group(cls) -> str:
        return "waternets"

    @classmethod
    def structure_name(cls) -> str:
        return "waternets"

    Id: str | None = None
    ContentVersion: str | None = "2"
    PhreaticLineId: str | None = None
    HeadLines: list[PersistableHeadLine] = []
    ReferenceLines: list[PersistableReferenceLine] = []
    UnitWeightWater: float | None = 9.81

    @field_validator("Id", "PhreaticLineId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
        points: list[Point],
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
        points: list[Point],
        bottom_head_line_id: str | None = None,
        top_head_line_id: str | None = None,
    ) -> PersistableReferenceLine:
        reference_line = PersistableReferenceLine(
            Id=reference_line_id, Label=label, Notes=notes
        )
        reference_line.Points = [PersistablePoint(X=p.x, Z=p.z) for p in points]

        if bottom_head_line_id is not None and not self.has_head_line_id(
            bottom_head_line_id
        ):
            raise ValueError(
                f"Unknown headline id {bottom_head_line_id} for bottom_head_line_id"
            )

        if top_head_line_id is not None and not self.has_head_line_id(top_head_line_id):
            raise ValueError(
                f"Unknown headline id {top_head_line_id} for top_head_line_id"
            )

        reference_line.BottomHeadLineId = bottom_head_line_id
        reference_line.TopHeadLineId = top_head_line_id

        self.ReferenceLines.append(reference_line)
        return reference_line


class PersistableDitchCharacteristics(DStabilityBaseModelStructure):
    DitchBottomEmbankmentSide: float | str | None = "NaN"
    DitchBottomLandSide: float | str | None = "NaN"
    DitchEmbankmentSide: float | str | None = "NaN"
    DitchLandSide: float | str | None = "NaN"


class PersistableEmbankmentCharacteristics(DStabilityBaseModelStructure):
    EmbankmentToeLandSide: float | str | None = "NaN"
    EmbankmentToeWaterSide: float | str | None = "NaN"
    EmbankmentTopLandSide: float | str | None = "NaN"
    EmbankmentTopWaterSide: float | str | None = "NaN"
    ShoulderBaseLandSide: float | str | None = "NaN"


class EmbankmentSoilScenarioEnum(str, Enum):
    CLAY_EMBANKMENT_ON_CLAY = "ClayEmbankmentOnClay"
    CLAY_EMBANKMENT_ON_SAND = "ClayEmbankmentOnSand"
    SAND_EMBANKMENT_ON_CLAY = "SandEmbankmentOnClay"
    SAND_EMBANKMENT_ON_SAND = "SandEmbankmentOnSand"


class WaternetCreatorSettings(DStabilitySubStructure):
    """waternetcreatorsettings/waternetcreatorsettings_x.json"""

    AdjustForUplift: bool | None = False
    AquiferInsideAquitardLayerId: str | None = None
    AquiferLayerId: str | None = None
    AquiferLayerInsideAquitardLeakageLengthInwards: float | str | None = "NaN"
    AquiferLayerInsideAquitardLeakageLengthOutwards: float | str | None = "NaN"
    AquitardHeadLandSide: float | str | None = "NaN"
    AquitardHeadWaterSide: float | str | None = "NaN"
    ContentVersion: str | None = "2"
    DitchCharacteristics: PersistableDitchCharacteristics | None = (
        PersistableDitchCharacteristics()
    )
    DrainageConstruction: PersistablePoint | None = PersistablePoint()
    EmbankmentCharacteristics: PersistableEmbankmentCharacteristics | None = (
        PersistableEmbankmentCharacteristics()
    )
    EmbankmentSoilScenario: EmbankmentSoilScenarioEnum = (
        EmbankmentSoilScenarioEnum.CLAY_EMBANKMENT_ON_CLAY
    )
    Id: str | None = None
    InitialLevelEmbankmentTopLandSide: float | str | None = "NaN"
    InitialLevelEmbankmentTopWaterSide: float | str | None = "NaN"
    IntrusionLength: float | str | None = "NaN"
    IsAquiferLayerInsideAquitard: bool | None = False
    IsDitchPresent: bool | None = False
    IsDrainageConstructionPresent: bool | None = False
    MeanWaterLevel: float | str | None = "NaN"
    NormativeWaterLevel: float | str | None = "NaN"
    OffsetEmbankmentToeLandSide: float | str | None = "NaN"
    OffsetEmbankmentTopLandSide: float | str | None = "NaN"
    OffsetEmbankmentTopWaterSide: float | str | None = "NaN"
    OffsetShoulderBaseLandSide: float | str | None = "NaN"
    PleistoceneLeakageLengthInwards: float | str | None = "NaN"
    PleistoceneLeakageLengthOutwards: float | str | None = "NaN"
    UseDefaultOffsets: bool | None = True
    WaterLevelHinterland: float | str | None = "NaN"

    field_validator("Id", "AquiferLayerId", mode="before")

    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    @classmethod
    def structure_group(cls) -> str:
        return "waternetcreatorsettings"


class PersistableStochasticParameter(DStabilityBaseModelStructure):
    IsProbabilistic: bool = False
    Mean: float = 1.0
    StandardDeviation: float = 0.0


class InternalStateTypeEnum(Enum):
    OCR = "Ocr"
    POP = "Pop"
    YIELD_STRESS = "YieldStress"


class PersistableStress(DStabilityBaseModelStructure):
    Ocr: float = 1.0
    Pop: float = 0.0
    PopStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    StateType: InternalStateTypeEnum | None = None
    YieldStress: float = 0.0


class PersistableStateLinePoint(DStabilityBaseModelStructure):
    Above: PersistableStress | None = None
    Below: PersistableStress | None = None
    Id: str | None = None
    IsAboveAndBelowCorrelated: bool | None = None
    IsProbabilistic: bool | None = None
    Label: str | None = ""
    Notes: str | None = ""
    X: float | str | None = "NaN"

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableStateLine(DStabilityBaseModelStructure):
    Points: list[PersistablePoint | None] | None = None
    Values: list[PersistableStateLinePoint | None] | None = None


class PersistableStatePoint(DStabilityBaseModelStructure):
    Id: str | None = None
    IsProbabilistic: bool | None = None
    Label: str | None = ""
    LayerId: str | None = None
    Notes: str | None = ""
    Point: PersistablePoint | None = None
    Stress: PersistableStress | None = None

    @field_validator("Id", "LayerId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class State(DStabilitySubStructure):
    """states/states_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "states"

    @classmethod
    def structure_group(cls) -> str:
        return "states"

    ContentVersion: str | None = "2"
    Id: str | None = None
    StateLines: list[PersistableStateLine] = []
    StatePoints: list[PersistableStatePoint] = []

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    def add_state_point(self, state_point: PersistableStatePoint) -> None:
        self.StatePoints.append(state_point)

    def add_state_line(
        self,
        points: list[PersistablePoint],
        state_points: list[PersistableStateLinePoint],
    ) -> PersistableStateLine:
        state_line = PersistableStateLine(Points=points, Values=state_points)
        self.StateLines.append(PersistableStateLine(Points=points, Values=state_points))
        return state_line

    def get_state(self, state_id: int) -> PersistableStatePoint | PersistableStateLine:
        for state in self.StatePoints + self.StateLines:
            if state.Id == str(state_id):
                return state

        raise ValueError(f"State point with id {state_id} not found")


# statecorrelation


class PersistableStateCorrelation(DStabilityBaseModelStructure):
    CorrelatedStateIds: list[str | None] | None = None
    IsFullyCorrelated: bool | None = None

    @field_validator("CorrelatedStateIds", mode="before")
    def transform_id_to_str(cls, values) -> str:
        out = []
        for value in values:
            if value is None:
                out.append(None)
            else:
                out.append(str(value))
        return out


class StateCorrelation(DStabilitySubStructure):
    """statecorrelations/statecorrelations_1.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "statecorrelations"

    @classmethod
    def structure_group(cls) -> str:
        return "statecorrelations"

    ContentVersion: str | None = "2"
    Id: str | None = None
    StateCorrelations: list[PersistableStateCorrelation | None] | None = []

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    def add_state_correlation(
        self, state_correlation: PersistableStateCorrelation
    ) -> None:
        self.StateCorrelations.append(state_correlation)


class Stage(DStabilitySubStructure):
    """stages/stage_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "stage"

    @classmethod
    def structure_group(cls) -> str:
        return "stages"

    DecorationsId: str | None = None
    GeometryId: str | None = None
    Id: str | None = None
    Label: str | None = ""
    LoadsId: str | None = None
    Notes: str | None = ""
    ReinforcementsId: str | None = None
    SoilLayersId: str | None = None
    StateCorrelationsId: str | None = None
    StateId: str | None = None
    WaternetCreatorSettingsId: str | None = None
    WaternetId: str | None = None

    @field_validator(
        "DecorationsId",
        "GeometryId",
        "Id",
        "LoadsId",
        "ReinforcementsId",
        "SoilLayersId",
        "StateId",
        "WaternetId",
        mode="before",
    )
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableCalculation(DStabilityBaseModelStructure):
    Id: str | None = None
    Label: str | None = ""
    Notes: str | None = ""
    ResultId: str | None = None
    CalculationSettingsId: str | None = None

    @field_validator("Id", "ResultId", "CalculationSettingsId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class Scenario(DStabilitySubStructure):
    """scenarios/scenario_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "scenario"

    @classmethod
    def structure_group(cls) -> str:
        return "scenarios"

    Stages: list[Stage] | None = []
    Calculations: list[PersistableCalculation] | None = []
    ContentVersion: str | None = "2"
    Id: str | None = None
    Label: str | None = ""
    Notes: str | None = ""

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableShadingTypeEnum(Enum):
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
    Color: str | None = None
    PersistableShadingType: PersistableShadingTypeEnum | None
    SoilId: str | None = None

    @field_validator("SoilId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class SoilVisualisation(DStabilityBaseModelStructure):
    ContentVersion: str | None = "2"
    SoilVisualizations: list[PersistableSoilVisualization | None] | None = []

    @classmethod
    def structure_name(cls) -> str:
        return "soilvisualizations"


class PersistableSoilLayer(DStabilityBaseModelStructure):
    LayerId: str | None = None
    SoilId: str | None = None

    @field_validator("LayerId", "SoilId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class SoilLayerCollection(DStabilitySubStructure):
    """soillayers/soillayers_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "soillayers"

    @classmethod
    def structure_group(cls) -> str:
        return "soillayers"

    ContentVersion: str | None = "2"
    Id: str | None = None
    SoilLayers: list[PersistableSoilLayer] = []

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    def add_soillayer(self, layer_id: str, soil_id: str) -> PersistableSoilLayer:
        psl = PersistableSoilLayer(LayerId=layer_id, SoilId=soil_id)
        self.SoilLayers.append(psl)
        return psl

    def get_ids(self, exclude_soil_layer_id: int | None) -> set[str]:
        if exclude_soil_layer_id is not None:
            exclude_soil_layer_id = str(exclude_soil_layer_id)
        return {
            layer.LayerId
            for layer in self.SoilLayers
            if layer.LayerId != exclude_soil_layer_id
        }


class PersistableSoilCorrelation(DStabilityBaseModelStructure):
    CorrelatedSoilIds: list[str] | None = None

    @field_validator("CorrelatedSoilIds", mode="before")
    def transform_id_to_str(cls, values) -> str:
        out = []
        for value in values:
            if value is None:
                out.append(None)
            else:
                out.append(str(value))
        return out


class SoilCorrelation(DStabilitySubStructure):
    """soilcorrelations.json"""

    ContentVersion: str | None = "2"
    SoilCorrelations: list[PersistableSoilCorrelation | None] | None = []

    @classmethod
    def structure_name(cls) -> str:
        return "soilcorrelations"

    def add_soil_correlation(self, list_correlated_soil_ids: list[str]):
        """
        Add a new soil correlation to the model.

        Args:
            list_correlated_soil_ids (list[str]): a list of soil ids that are correlated

        Returns:
            None
        """
        self.SoilCorrelations.append(
            PersistableSoilCorrelation(CorrelatedSoilIds=list_correlated_soil_ids)
        )


class ShearStrengthModelTypePhreaticLevelInternal(Enum):
    """
    Shear Strength Model Type. These types represent the types that
    are internally defined in the json files of D-Stability.
    """

    MOHR_COULOMB_ADVANCED = "MohrCoulombAdvanced"
    MOHR_COULOMB_CLASSIC = "MohrCoulombClassic"
    NONE = "None"
    SU = "Su"
    SUTABLE = "SuTable"
    SIGMATAUTABLE = "SigmaTauTable"

    def to_global_shear_strength_model(self):
        transform_dictionary = {
            "MohrCoulombAdvanced": "Mohr_Coulomb",
            "MohrCoulombClassic": "Mohr_Coulomb",
            "None": "None",
            "Su": "SHANSEP",
            "SuTable": "SuTable",
            "SigmaTauTable": "SigmaTauTable",
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
    SuTablePoints: list[PersistableSuTablePoint] = []
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


class PersistableSigmaTauTablePoint(DStabilitySubStructure):
    EffectiveStress: float = 0.0
    ShearStrength: float = 0.0


class PersistableSigmaTauTable(DStabilityBaseModelStructure):
    SigmaTauTablePoints: list[PersistableSigmaTauTablePoint] = []
    IsSigmaTauTableProbabilistic: bool = False
    SigmaTauTableVariationCoefficient: float = 0.0

    def to_global_sigma_tau_table(self):
        from geolib.soils import SigmaTauTablePoint

        sigma_tau_table = []
        for sigma_tau_table_point in self.SigmaTauTablePoints:
            sigma_tau_table.append(
                SigmaTauTablePoint(
                    shearStrength=sigma_tau_table_point.ShearStrength,
                    effective_stress=sigma_tau_table_point.EffectiveStress,
                )
            )
        return sigma_tau_table


class PersistableMohrCoulombClassicShearStrengthModel(DStabilityBaseModelStructure):
    Cohesion: float | None = 0.0
    CohesionAndFrictionAngleCorrelated: bool = False
    CohesionStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    FrictionAngle: float | None = 0.0
    FrictionAngleStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )


class PersistableMohrCoulombAdvancedShearStrengthModel(DStabilityBaseModelStructure):
    Cohesion: float | None = 0.0
    CohesionAndFrictionAngleCorrelated: bool = False
    CohesionStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    Dilatancy: float | None = 0.0
    DilatancyStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    FrictionAngle: float | None = 0.0
    FrictionAngleStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )


class PersistableSuShearStrengthModel(DStabilityBaseModelStructure):
    ShearStrengthRatio: float | None = 0.0
    ShearStrengthRatioAndShearStrengthExponentCorrelated: bool = False
    ShearStrengthRatioStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )
    StrengthIncreaseExponent: float | None = 1.0
    StrengthIncreaseExponentStochasticParameter: PersistableStochasticParameter = (
        PersistableStochasticParameter()
    )


class PersistableSoil(DStabilityBaseModelStructure):
    Code: str = ""
    Id: str = ""
    IsProbabilistic: bool = False
    Name: str | None = ""
    Notes: str | None = ""
    ShearStrengthModelTypeAbovePhreaticLevel: (
        ShearStrengthModelTypePhreaticLevelInternal
    ) = ShearStrengthModelTypePhreaticLevelInternal.MOHR_COULOMB_ADVANCED
    ShearStrengthModelTypeBelowPhreaticLevel: (
        ShearStrengthModelTypePhreaticLevelInternal
    ) = ShearStrengthModelTypePhreaticLevelInternal.SU
    MohrCoulombClassicShearStrengthModel: (
        PersistableMohrCoulombClassicShearStrengthModel
    ) = PersistableMohrCoulombClassicShearStrengthModel()
    MohrCoulombAdvancedShearStrengthModel: (
        PersistableMohrCoulombAdvancedShearStrengthModel
    ) = PersistableMohrCoulombAdvancedShearStrengthModel()
    SuShearStrengthModel: PersistableSuShearStrengthModel = (
        PersistableSuShearStrengthModel()
    )
    VolumetricWeightAbovePhreaticLevel: float = 0.0
    VolumetricWeightBelowPhreaticLevel: float = 0.0
    SuTable: PersistableSuTable = PersistableSuTable()
    SigmaTauTable: PersistableSigmaTauTable = PersistableSigmaTauTable()

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class SoilCollection(DStabilitySubStructure):
    """soils.json"""

    ContentVersion: str | None = "2"
    Soils: list[PersistableSoil] = [
        PersistableSoil(
            Id="2",
            Name="Embankment new",
            Code="H_Aa_ht_new",
            MohrCoulombAdvancedShearStrengthModel=PersistableMohrCoulombAdvancedShearStrengthModel(
                Cohesion=7.0, FrictionAngle=30.0, Dilatancy=0.0
            ),
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.26,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=19.3,
            VolumetricWeightBelowPhreaticLevel=19.3,
        ),
        PersistableSoil(
            Id="3",
            Name="Embankment old",
            Code="H_Aa_ht_old",
            MohrCoulombAdvancedShearStrengthModel=PersistableMohrCoulombAdvancedShearStrengthModel(
                Cohesion=7.0, FrictionAngle=30.0, Dilatancy=0.0
            ),
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.26,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="4",
            Name="Clay, shallow",
            Code="H_Rk_k_shallow",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.23,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=14.8,
            VolumetricWeightBelowPhreaticLevel=14.8,
        ),
        PersistableSoil(
            Id="5",
            Name="Clay, deep",
            Code="H_Rk_k_deep",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.23,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=15.6,
            VolumetricWeightBelowPhreaticLevel=15.6,
        ),
        PersistableSoil(
            Id="6",
            Name="Organic clay",
            Code="H_Rk_ko",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.24,
                StrengthIncreaseExponent=0.85,
            ),
            VolumetricWeightAbovePhreaticLevel=13.9,
            VolumetricWeightBelowPhreaticLevel=13.9,
        ),
        PersistableSoil(
            Id="7",
            Name="Peat, shallow",
            Code="H_vhv_v",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.3,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=10.1,
            VolumetricWeightBelowPhreaticLevel=10.1,
        ),
        PersistableSoil(
            Id="8",
            Name="Peat, deep",
            Code="H_vbv_v",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.27,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=11.0,
            VolumetricWeightBelowPhreaticLevel=11.0,
        ),
        PersistableSoil(
            Id="9",
            Name="Sand",
            Code="Sand",
            MohrCoulombAdvancedShearStrengthModel=PersistableMohrCoulombAdvancedShearStrengthModel(
                Cohesion=0.0, FrictionAngle=30.0, Dilatancy=0.0
            ),
            ShearStrengthModelTypeBelowPhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.MOHR_COULOMB_ADVANCED,
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=20.0,
        ),
        PersistableSoil(
            Id="10",
            Name="Clay with silt",
            Code="P_Rk_k&s",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.22,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="11",
            Name="Sand with clay",
            Code="H_Ro_z&k",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SU,
            SuShearStrengthModel=PersistableSuShearStrengthModel(
                ShearStrengthRatio=0.22,
                StrengthIncreaseExponent=0.9,
            ),
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="12",
            Name="Dilatent clay",
            Code="Dilatent clay",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SUTABLE,
            SuTable=PersistableSuTable(
                StrengthIncreaseExponent=0.8,
                SuTablePoints=[
                    PersistableSuTablePoint(EffectiveStress=0, Su=0),
                    PersistableSuTablePoint(EffectiveStress=100, Su=200),
                    PersistableSuTablePoint(EffectiveStress=200, Su=300),
                ],
            ),
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="13",
            Name="Embankment dry",
            Code="Embankment dry",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SUTABLE,
            SuTable=PersistableSuTable(
                StrengthIncreaseExponent=0.8,
                SuTablePoints=[
                    PersistableSuTablePoint(EffectiveStress=0, Su=0),
                    PersistableSuTablePoint(EffectiveStress=29, Su=29),
                    PersistableSuTablePoint(EffectiveStress=40, Su=32),
                    PersistableSuTablePoint(EffectiveStress=60, Su=37),
                    PersistableSuTablePoint(EffectiveStress=80, Su=42),
                    PersistableSuTablePoint(EffectiveStress=100, Su=48),
                    PersistableSuTablePoint(EffectiveStress=120, Su=55),
                    PersistableSuTablePoint(EffectiveStress=140, Su=62),
                    PersistableSuTablePoint(EffectiveStress=160, Su=69),
                    PersistableSuTablePoint(EffectiveStress=180, Su=77),
                ],
            ),
            VolumetricWeightAbovePhreaticLevel=18.0,
            VolumetricWeightBelowPhreaticLevel=18.0,
        ),
        PersistableSoil(
            Id="14",
            Name="S_Tau material",
            Code="S_Tau material",
            ShearStrengthModelTypeAbovePhreaticLevel=ShearStrengthModelTypePhreaticLevelInternal.SIGMATAUTABLE,
            SigmaTauTable=PersistableSigmaTauTable(
                SigmaTauTablePoints=[
                    PersistableSigmaTauTablePoint(EffectiveStress=0, ShearStrength=5),
                    PersistableSigmaTauTablePoint(EffectiveStress=10, ShearStrength=5),
                    PersistableSigmaTauTablePoint(EffectiveStress=35, ShearStrength=30),
                    PersistableSigmaTauTablePoint(EffectiveStress=100, ShearStrength=60),
                ]
            ),
            VolumetricWeightAbovePhreaticLevel=16.0,
            VolumetricWeightBelowPhreaticLevel=16.0,
        ),
    ]

    @classmethod
    def structure_name(cls) -> str:
        return "soils"

    def has_soil_code(self, code: str) -> bool:
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
            or persistable_soil.ShearStrengthModelTypeBelowPhreaticLevel.value == "Su"
        ):
            # SHANSEP model is selected so the StrengthIncreaseExponentStochasticParameter from persistable_soil should be used
            return self.__to_global_stochastic_parameter(
                persistable_soil.SuShearStrengthModel.StrengthIncreaseExponentStochasticParameter
            )
        elif (
            persistable_soil.ShearStrengthModelTypeAbovePhreaticLevel.value == "SuTable"
            or persistable_soil.ShearStrengthModelTypeBelowPhreaticLevel.value
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
            SigmaTauParameters,
            SoilWeightParameters,
            UndrainedParameters,
        )

        mohr_coulomb_parameters = MohrCoulombParameters(
            cohesion=self.__to_global_stochastic_parameter(
                persistable_soil.MohrCoulombAdvancedShearStrengthModel.CohesionStochasticParameter
            ),
            friction_angle=self.__to_global_stochastic_parameter(
                persistable_soil.MohrCoulombAdvancedShearStrengthModel.FrictionAngleStochasticParameter
            ),
            dilatancy_angle=self.__to_global_stochastic_parameter(
                persistable_soil.MohrCoulombAdvancedShearStrengthModel.DilatancyStochasticParameter
            ),
            cohesion_and_friction_angle_correlated=persistable_soil.MohrCoulombAdvancedShearStrengthModel.CohesionAndFrictionAngleCorrelated,
        )

        sigma_tau_parameters = SigmaTauParameters(
            sigma_tau_table=persistable_soil.SigmaTauTable.to_global_sigma_tau_table(),
            probabilistic_sigma_tau_table=persistable_soil.SigmaTauTable.IsSigmaTauTableProbabilistic,
            sigma_tau_table_variation_coefficient=persistable_soil.SigmaTauTable.SigmaTauTableVariationCoefficient,
        )

        strength_increase_exponent = self.__determine_strength_increase_exponent(
            persistable_soil
        )
        undrained_parameters = UndrainedParameters(
            shear_strength_ratio=self.__to_global_stochastic_parameter(
                persistable_soil.SuShearStrengthModel.ShearStrengthRatioStochasticParameter
            ),
            strength_increase_exponent=strength_increase_exponent,
            shear_strength_ratio_and_shear_strength_exponent_correlated=persistable_soil.SuShearStrengthModel.ShearStrengthRatioAndShearStrengthExponentCorrelated,
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
            sigma_tau_parameters=sigma_tau_parameters,
            soil_weight_parameters=soil_weight_parameters,
            undrained_parameters=undrained_parameters,
        )

    def get_soil(self, code: str) -> PersistableSoil:
        """
        Get soil by the given code.

        Args:
            code (str): code of the soil

        Returns:
            Soil: the soil object
        """
        for persistable_soil in self.Soils:
            if persistable_soil.Code == code:
                return persistable_soil

        raise ValueError(f"Soil code '{code}' not found in the SoilCollection")

    def get_soil_by_name(self, name: str) -> PersistableSoil:
        """
        Get soil by the given name.

        Args:
            code (str): name of the soil

        Returns:
            Soil: the soil object
        """
        for persistable_soil in self.Soils:
            if persistable_soil.Name == name:
                return persistable_soil

        raise ValueError(f"Soil name '{name}' not found in the SoilCollection")

    def get_global_soil(self, code: str) -> Soil:
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


# Reinforcements


class PersistableForbiddenLine(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    End: PersistablePoint | None = None
    Start: PersistablePoint | None = None


class PersistableGeotextile(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    End: PersistablePoint | None = None
    ReductionArea: float | str | None = "NaN"
    Start: PersistablePoint | None = None
    TensileStrength: float | str | None = "NaN"


class PersistableStressAtDistance(DStabilityBaseModelStructure):
    Distance: float | str | None = "NaN"
    Stress: float | str | None = "NaN"


class PersistableNail(DStabilityBaseModelStructure):
    BendingStiffness: float | None = 0.0
    CriticalAngle: float | None = 0.0
    Diameter: float | str | None = "NaN"
    Direction: float | None = 0.0
    GroutDiameter: float | None = 0.0
    HorizontalSpacing: float | None = 0.0
    Label: str | None = ""
    LateralStresses: list[PersistableStressAtDistance | None] | None = []
    Length: float | str | None = "NaN"
    Location: PersistablePoint | None = None
    MaxPullForce: float | None = 0.0
    Key: int | None = 1
    Notes: str | None = ""
    PlasticMoment: float | None = 0.0
    ShearStresses: list[PersistableStressAtDistance | None] | None = []
    UseFacing: bool | None = False
    UseLateralStress: bool | None = False
    UseShearStress: bool | None = False


class Reinforcements(DStabilitySubStructure):
    """reinforcements/reinforcements_x.json"""

    Id: str | None = None
    ContentVersion: str | None = "2"
    ForbiddenLines: list[PersistableForbiddenLine] = []
    Geotextiles: list[PersistableGeotextile] = []
    Nails: list[PersistableNail] = []

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    def add_reinforcement(
        self, reinforcement: "DStabilityReinforcement"
    ) -> PersistableForbiddenLine | PersistableGeotextile | PersistableNail:
        internal_datastructure = reinforcement._to_internal_datastructure()
        plural_class_name = f"{reinforcement.__class__.__name__}s"
        getattr(self, plural_class_name).append(internal_datastructure)
        return internal_datastructure


class ProjectInfo(DStabilitySubStructure):
    """projectinfo.json."""

    Analyst: str | None = ""
    ApplicationCreated: str | None = ""
    ApplicationModified: str | None = ""
    ContentVersion: str | None = "2"
    Created: date | None = datetime.now().date()
    CrossSection: str | None = ""
    Date: date | None = datetime.now().date()
    IsDataValidated: bool | None = False
    LastModified: date | None = datetime.now().date()
    LastModifier: str | None = "GEOLib"
    Path: str | None = ""
    Project: str | None = ""
    Remarks: str | None = f"Created with GEOLib {version}"

    @classmethod
    def nltime(cls, date: date | str) -> date:
        if isinstance(date, str):
            position = date.index(max(date.split("-"), key=len))
            if position > 0:
                date = datetime.strptime(date, "%d-%m-%Y").date()
            else:
                date = datetime.strptime(date, "%Y-%m-%d").date()
        return date

    nltime_validator = field_validator("Created", "Date", "LastModified", mode="before")(
        nltime
    )


class PersistableBondStress(DStabilityBaseModelStructure):
    Sigma: float | str | None = "NaN"
    Tau: float | str | None = "NaN"


class PersistableNailPropertiesForSoil(DStabilityBaseModelStructure):
    AreBondStressesActive: bool | None = False
    BondStresses: list[PersistableBondStress | None] | None = []
    CompressionRatio: float | str | None = "NaN"
    RheologicalCoefficient: float | str | None = "NaN"
    SoilId: str | None = None

    @field_validator("SoilId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class NailProperties(DStabilitySubStructure):
    """nailpropertiesforsoils.json"""

    ContentVersion: str | None = "2"
    NailPropertiesForSoils: list[PersistableNailPropertiesForSoil | None] | None = []

    @classmethod
    def structure_name(cls) -> str:
        return "nailpropertiesforsoils"


class PersistableConsolidation(DStabilityBaseModelStructure):
    Degree: float | str | None = "NaN"
    LayerId: str | None = None

    @field_validator("LayerId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableEarthquake(DStabilityBaseModelStructure):
    Consolidations: list[PersistableConsolidation | None] | None = []
    FreeWaterFactor: float | None = 0.0
    HorizontalFactor: float | None = 0.0
    IsEnabled: bool | None = False
    Label: str | None = ""
    Notes: str | None = ""
    VerticalFactor: float | None = 0.0


class PersistableLayerLoad(DStabilityBaseModelStructure):
    Consolidations: list[PersistableConsolidation | None] | None = []
    LayerId: str | None = None

    @field_validator("LayerId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableLineLoad(DStabilityBaseModelStructure):
    Angle: float | str | None = "NaN"
    Consolidations: list[PersistableConsolidation | None] | None = []
    Label: str | None = ""
    Location: PersistablePoint | None = None
    Magnitude: float | str | None = "NaN"
    Notes: str | None = ""
    Spread: float | str | None = "NaN"


class PersistableTree(DStabilityBaseModelStructure):
    Force: float | str | None = "NaN"
    Label: str | None = ""
    Location: PersistablePoint | None = None
    Notes: str | None = ""
    RootZoneWidth: float | str | None = "NaN"
    Spread: float | str | None = "NaN"


class PersistableUniformLoad(DStabilityBaseModelStructure):
    Consolidations: list[PersistableConsolidation | None] | None = []
    End: float | str | None = "NaN"
    Label: str | None = ""
    Magnitude: float | str | None = "NaN"
    Notes: str | None = ""
    Spread: float | str | None = "NaN"
    Start: float | str | None = "NaN"


Load = PersistableUniformLoad | PersistableLineLoad | PersistableLayerLoad


class Loads(DStabilitySubStructure):
    """loads/loads_x.json"""

    Id: str | None = None
    ContentVersion: str | None = "2"
    Earthquake: PersistableEarthquake | None = PersistableEarthquake()
    LayerLoads: list[PersistableLayerLoad | None] | None = []
    LineLoads: list[PersistableLineLoad | None] | None = []
    Trees: list[PersistableTree | None] | None = []
    UniformLoads: list[PersistableUniformLoad | None] | None = []

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    def add_load(
        self, load: "DStabilityLoad", consolidations: list["Consolidation"]
    ) -> (
        PersistableUniformLoad
        | PersistableLineLoad
        | PersistableLayerLoad
        | PersistableTree
    ):
        internal_datastructure = load.to_internal_datastructure()

        # Add consolidations if the load supports it
        if hasattr(internal_datastructure, "Consolidations"):
            internal_datastructure.Consolidations = [
                c.to_internal_datastructure() for c in consolidations
            ]

        target = load.__class__.__name__
        if target == "Earthquake":
            setattr(self, target, internal_datastructure)
        if target == "TreeLoad":
            getattr(self, "Trees").append(internal_datastructure)
        else:
            target += "s"
            getattr(self, target).append(internal_datastructure)

        return internal_datastructure

    def add_layer_load(
        self, soil_layer_id: int, consolidations: list["Consolidation"]
    ) -> PersistableLayerLoad:
        layer_load = PersistableLayerLoad(
            LayerId=str(soil_layer_id),
            Consolidations=[c.to_internal_datastructure() for c in consolidations],
        )
        self.LayerLoads.append(layer_load)
        return layer_load


class PersistableLayer(DStabilityBaseModelStructure):
    Id: str | None = None
    Label: str | None = ""
    Notes: str | None = ""
    Points: Annotated[list[PersistablePoint], Field(min_length=3)]

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    @classmethod
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

    polygon_chack_validator = field_validator("Points", mode="before")(polygon_checks)


class Geometry(DStabilitySubStructure):
    """geometries/geometry_x.json"""

    @classmethod
    def structure_group(cls) -> str:
        return "geometries"

    ContentVersion: str | None = "2"
    Id: str | None = None
    Layers: list[PersistableLayer] = []

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
        self, id: str, label: str, notes: str, points: list[Point]
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
            points (list[Points]): list of Point classes

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


class PersistableElevation(DStabilityBaseModelStructure):
    AddedLayerId: str | None = None
    Label: str | None = ""
    Notes: str | None = ""
    Points: list[PersistablePoint | None] | None = None

    @field_validator("AddedLayerId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableExcavation(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    Points: list[PersistablePoint | None] | None = None


class Decorations(DStabilitySubStructure):
    """decorations/decorations_x.json."""

    Elevations: list[PersistableElevation | None] | None = []
    ContentVersion: str | None = "2"
    Excavations: list[PersistableExcavation | None] | None = []
    Id: str | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    def add_excavation(self, excavation: PersistableExcavation):
        self.Excavations.append(excavation)


# Calculation Settings


class PersistableCircle(DStabilityBaseModelStructure):
    Center: PersistablePoint | None = PersistablePoint()
    Radius: float | str | None = "NaN"


class PersistableBishopSettings(DStabilityBaseModelStructure):
    Circle: PersistableCircle | None = PersistableCircle()
    Label: str | None = ""
    Notes: str | None = ""


class PersistableGridEnhancements(DStabilityBaseModelStructure):
    ExtrapolateSearchSpace: bool | None = True


class NullablePersistablePoint(DStabilityBaseModelStructure):
    X: float | str | None = "NaN"
    Z: float | str | None = "NaN"


class PersistableSearchGrid(DStabilityBaseModelStructure):
    BottomLeft: NullablePersistablePoint | None = None
    Label: str | None = ""
    Notes: str | None = ""
    NumberOfPointsInX: int | None = 1
    NumberOfPointsInZ: int | None = 1
    Space: float | None = 1.0


class PersistableSlipPlaneConstraints(DStabilityBaseModelStructure):
    IsSizeConstraintsEnabled: bool | None = False
    IsZoneAConstraintsEnabled: bool | None = False
    IsZoneBConstraintsEnabled: bool | None = False
    MinimumSlipPlaneDepth: float | None = 0.0
    MinimumSlipPlaneLength: float | None = 0.0
    WidthZoneA: float | None = 0.0
    WidthZoneB: float | None = 0.0
    XLeftZoneA: float | None = 0.0
    XLeftZoneB: float | None = 0.0


class PersistableTangentLines(DStabilityBaseModelStructure):
    BottomTangentLineZ: float | str | None = "NaN"
    Label: str | None = ""
    Notes: str | None = ""
    NumberOfTangentLines: int | None = 1
    Space: float | None = 0.5


class PersistableBishopBruteForceSettings(DStabilityBaseModelStructure):
    GridEnhancements: PersistableGridEnhancements | None = PersistableGridEnhancements()
    SearchGrid: PersistableSearchGrid | None = PersistableSearchGrid()
    SlipPlaneConstraints: PersistableSlipPlaneConstraints | None = (
        PersistableSlipPlaneConstraints()
    )
    TangentLines: PersistableTangentLines | None = PersistableTangentLines()


class CalculationTypeEnum(Enum):
    DESIGN = "Design"
    DETERMINISTIC = "Deterministic"
    MEAN = "Mean"
    PROBABILISTIC = "Probabilistic"


CalculationType = CalculationTypeEnum


class PersistableGeneticSlipPlaneConstraints(DStabilityBaseModelStructure):
    IsEnabled: bool | None = False
    MinimumAngleBetweenSlices: float | None = 0.0
    MinimumThrustLinePercentageInsideSlices: float | None = 0.0


class PersistableSpencerSettings(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    SlipPlane: list[PersistablePoint | None] | None = None
    SlipPlaneConstraints: PersistableGeneticSlipPlaneConstraints | None = (
        PersistableGeneticSlipPlaneConstraints()
    )


class OptionsTypeEnum(Enum):
    DEFAULT = "Default"
    THOROUGH = "Thorough"


OptionsType = OptionsTypeEnum


class PersistableSpencerGeneticSettings(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    OptionsType: OptionsTypeEnum | None = OptionsType.DEFAULT
    SlipPlaneA: list[PersistablePoint | None] | None = None
    SlipPlaneB: list[PersistablePoint | None] | None = None
    SlipPlaneConstraints: PersistableGeneticSlipPlaneConstraints | None = (
        PersistableGeneticSlipPlaneConstraints()
    )


class PersistableTwoCirclesOnTangentLine(DStabilityBaseModelStructure):
    FirstCircleCenter: NullablePersistablePoint | None = NullablePersistablePoint()
    FirstCircleRadius: float | str | None = "NaN"
    SecondCircleCenter: NullablePersistablePoint | None = NullablePersistablePoint()


class PersistableUpliftVanSettings(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    SlipPlane: PersistableTwoCirclesOnTangentLine | None = (
        PersistableTwoCirclesOnTangentLine()
    )


class PersistableSearchArea(DStabilityBaseModelStructure):
    Height: float | None = 0.0
    Label: str | None = ""
    Notes: str | None = ""
    TopLeft: NullablePersistablePoint | None = None
    Width: float | None = 0.0


class PersistableTangentArea(DStabilityBaseModelStructure):
    Height: float | None = 0.0
    Label: str | None = ""
    Notes: str | None = ""
    TopZ: float | str | None = "NaN"


class PersistableUpliftVanParticleSwarmSettings(DStabilityBaseModelStructure):
    Label: str | None = ""
    Notes: str | None = ""
    OptionsType: OptionsTypeEnum | None = OptionsType.DEFAULT
    SearchAreaA: PersistableSearchArea | None = PersistableSearchArea()
    SearchAreaB: PersistableSearchArea | None = PersistableSearchArea()
    SlipPlaneConstraints: PersistableSlipPlaneConstraints | None = (
        PersistableSlipPlaneConstraints()
    )
    TangentArea: PersistableTangentArea | None = PersistableTangentArea()


class CalculationSettings(DStabilitySubStructure):
    """calculationsettings/calculationsettings_x.json"""

    AnalysisType: AnalysisTypeEnum | None = AnalysisTypeEnum.BISHOP_BRUTE_FORCE
    Bishop: PersistableBishopSettings | None = PersistableBishopSettings()
    BishopBruteForce: PersistableBishopBruteForceSettings | None = (
        PersistableBishopBruteForceSettings()
    )
    CalculationType: CalculationTypeEnum | None = CalculationTypeEnum.DETERMINISTIC
    ContentVersion: str | None = "2"
    Id: str | None = "19"
    ModelFactorMean: float | None = 1.05
    ModelFactorStandardDeviation: float | None = 0.033
    Spencer: PersistableSpencerSettings | None = PersistableSpencerSettings()
    SpencerGenetic: PersistableSpencerGeneticSettings | None = (
        PersistableSpencerGeneticSettings()
    )
    UpliftVan: PersistableUpliftVanSettings | None = PersistableUpliftVanSettings()
    UpliftVanParticleSwarm: PersistableUpliftVanParticleSwarmSettings | None = (
        PersistableUpliftVanParticleSwarmSettings()
    )

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
    ArcLength: float | str | None = "NaN"
    BottomAngle: float | str | None = "NaN"
    BottomLeft: PersistablePoint | None = None
    BottomRight: PersistablePoint | None = None
    CohesionInput: float | str | None = "NaN"
    CohesionOutput: float | str | None = "NaN"
    DegreeOfConsolidationLoadPorePressure: float | str | None = "NaN"
    DegreeOfConsolidationPorePressure: float | str | None = "NaN"
    DilatancyInput: float | str | None = "NaN"
    DilatancyOutput: float | str | None = "NaN"
    EffectiveStress: float | str | None = "NaN"
    HorizontalPorePressure: float | str | None = "NaN"
    HorizontalSoilQuakeStress: float | str | None = "NaN"
    HydrostaticPorePressure: float | str | None = "NaN"
    InputShearStress: float | str | None = "NaN"
    Label: str | None = None
    LoadStress: float | str | None = "NaN"
    MInput: float | str | None = "NaN"
    NormalStress: float | str | None = "NaN"
    Ocr: float | str | None = "NaN"
    OutputShearStress: float | str | None = "NaN"
    PhiInput: float | str | None = "NaN"
    PhiOutput: float | str | None = "NaN"
    PiezometricPorePressure: float | str | None = "NaN"
    Pop: float | str | None = "NaN"
    ResultantForce: float | str | None = "NaN"
    ResultantMoment: float | str | None = "NaN"
    SInput: float | str | None = "NaN"
    ShearStress: float | str | None = "NaN"
    SuInput: float | str | None = "NaN"
    SuOutput: float | str | None = "NaN"
    SurfacePorePressure: float | str | None = "NaN"
    TopAngle: float | str | None = "NaN"
    TopLeft: PersistablePoint | None = None
    TopRight: PersistablePoint | None = None
    TotalPorePressure: float | str | None = "NaN"
    TotalStress: float | str | None = "NaN"
    UpliftFactor: float | str | None = "NaN"
    VerticalPorePressure: float | str | None = "NaN"
    VerticalSoilQuakeStress: float | str | None = "NaN"
    WaterQuakeStress: float | str | None = "NaN"
    Weight: float | str | None = "NaN"
    Width: float | str | None = "NaN"
    YieldStress: float | str | None = "NaN"
    ShearStrengthModelType: ShearStrengthModelTypePhreaticLevelInternal | None = None


class BishopBruteForceResult(DStabilitySubStructure):
    Circle: PersistableCircle | None = None
    FactorOfSafety: float | str | None = "NaN"
    Id: str | None = None
    Points: list[PersistablePoint | None] | None = None
    Slices: list[PersistableSlice | None] | None = None
    ResultThreshold: float | str | None = "NaN"
    SlipPlaneResults: list | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
    Alpha: float | str | None = "NaN"
    Property: str | None = None
    SoilId: str | None = None
    UncorrelatedAlpha: float | str | None = "NaN"
    Value: float | str | None = "NaN"

    @field_validator("SoilId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableCalculationContribution(DStabilityBaseModelStructure):
    Alpha: float | str | None = "NaN"
    Property: str | None = None
    CalculationId: str | None = None
    UncorrelatedAlpha: float | str | None = "NaN"
    Value: float | str | None = "NaN"

    @field_validator("CalculationId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableStateLinePointContribution(DStabilityBaseModelStructure):
    Alpha: float | str | None = "NaN"
    Property: str | None = None
    StateLinePointId: str | None = None
    UncorrelatedAlpha: float | str | None = "NaN"
    Value: float | str | None = "NaN"

    @field_validator("StateLinePointId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class PersistableStatePointContribution(DStabilityBaseModelStructure):
    Alpha: float | str | None = "NaN"
    Property: str | None = None
    StatePointId: str | None = None
    UncorrelatedAlpha: float | str | None = "NaN"
    Value: float | str | None = "NaN"

    @field_validator("StatePointId", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)


class BishopReliabilityResult(DStabilitySubStructure):
    Circle: PersistableCircle | None = None
    Converged: bool | None = None
    FailureProbability: float | str | None = "NaN"
    Id: str | None = None
    ReliabilityIndex: float | str | None = "NaN"
    DistanceToConvergence: float | str | None = "NaN"
    SoilContributions: list[PersistableSoilContribution | None] | None = None
    CalculationContributions: list[PersistableCalculationContribution | None] | None = (
        None
    )
    StateLinePointContributions: (
        list[PersistableStateLinePointContribution | None] | None
    ) = None
    StatePointContributions: list[PersistableStatePointContribution | None] | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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


class BishopBruteForceReliabilityResult(DStabilitySubStructure):
    Circle: PersistableCircle | None = None
    Converged: bool | None = None
    FailureProbability: float | str | None = "NaN"
    Id: str | None = None
    ReliabilityIndex: float | str | None = "NaN"
    DistanceToConvergence: float | str | None = "NaN"
    SoilContributions: list[PersistableSoilContribution | None] | None = None
    CalculationContributions: list[PersistableCalculationContribution | None] | None = (
        None
    )
    StateLinePointContributions: (
        list[PersistableStateLinePointContribution | None] | None
    ) = None
    StatePointContributions: list[PersistableStatePointContribution | None] | None = None
    ResultThreshold: float | str | None = "NaN"
    SlipPlaneResults: list | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    @classmethod
    def structure_group(cls) -> str:
        return "results/bishopbruteforcereliability/"

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
    Circle: PersistableCircle | None = None
    FactorOfSafety: float | str | None = "NaN"
    Id: str | None = None
    Points: list[PersistablePoint | None] | None = None
    Slices: list[PersistableSlice | None] | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
    ArcLength: float | str | None = "NaN"
    BottomAngle: float | str | None = "NaN"
    BottomLeft: PersistablePoint | None = None
    BottomRight: PersistablePoint | None = None
    CohesionInput: float | str | None = "NaN"
    CohesionOutput: float | str | None = "NaN"
    DegreeOfConsolidationLoadPorePressure: float | str | None = "NaN"
    DegreeOfConsolidationPorePressure: float | str | None = "NaN"
    DilatancyInput: float | str | None = "NaN"
    DilatancyOutput: float | str | None = "NaN"
    EffectiveStress: float | str | None = "NaN"
    HorizontalPorePressure: float | str | None = "NaN"
    HorizontalSoilQuakeStress: float | str | None = "NaN"
    HydrostaticPorePressure: float | str | None = "NaN"
    InputShearStress: float | str | None = "NaN"
    Label: str | None = None
    LeftForce: float | str | None = "NaN"
    LeftForceAngle: float | str | None = "NaN"
    LeftForceY: float | str | None = "NaN"
    LoadStress: float | str | None = "NaN"
    MInput: float | str | None = "NaN"
    NormalStress: float | str | None = "NaN"
    Ocr: float | str | None = "NaN"
    OutputShearStress: float | str | None = "NaN"
    PhiInput: float | str | None = "NaN"
    PhiOutput: float | str | None = "NaN"
    PiezometricPorePressure: float | str | None = "NaN"
    Pop: float | str | None = "NaN"
    ResultantForce: float | str | None = "NaN"
    ResultantMoment: float | str | None = "NaN"
    RightForce: float | str | None = "NaN"
    RightForceAngle: float | str | None = "NaN"
    RightForceY: float | str | None = "NaN"
    ShearStress: float | str | None = "NaN"
    SInput: float | str | None = "NaN"
    SuInput: float | str | None = "NaN"
    SuOutput: float | str | None = "NaN"
    SurfacePorePressure: float | str | None = "NaN"
    TopAngle: float | str | None = "NaN"
    TopLeft: PersistablePoint | None = None
    TopRight: PersistablePoint | None = None
    TotalPorePressure: float | str | None = "NaN"
    TotalStress: float | str | None = "NaN"
    UpliftFactor: float | str | None = "NaN"
    VerticalPorePressure: float | str | None = "NaN"
    VerticalSoilQuakeStress: float | str | None = "NaN"
    WaterQuakeStress: float | str | None = "NaN"
    Weight: float | str | None = "NaN"
    Width: float | str | None = "NaN"
    YieldStress: float | str | None = "NaN"
    ShearStrengthModelType: ShearStrengthModelTypePhreaticLevelInternal | None = None


class SpencerGeneticAlgorithmResult(DStabilitySubStructure):
    FactorOfSafety: float | str | None = "NaN"
    Id: str | None = None
    Points: list[PersistablePoint | None] | None = None
    Slices: list[PersistableSpencerSlice | None] | None = None
    SlipPlane: list[PersistablePoint | None] | None = None
    ResultThreshold: float | str | None = "NaN"
    SlipPlaneResults: list | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
    Converged: bool | None = None
    FailureProbability: float | str | None = "NaN"
    Id: str | None = None
    ReliabilityIndex: float | str | None = "NaN"
    DistanceToConvergence: float | str | None = "NaN"
    SlipPlane: list[PersistablePoint | None] | None = None
    SoilContributions: list[PersistableSoilContribution | None] | None = None
    CalculationContributions: list[PersistableCalculationContribution | None] | None = (
        None
    )
    StateLinePointContributions: (
        list[PersistableStateLinePointContribution | None] | None
    ) = None
    StatePointContributions: list[PersistableStatePointContribution | None] | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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


class SpencerGeneticAlgorithmReliabilityResult(DStabilitySubStructure):
    Converged: bool | None = None
    FailureProbability: float | str | None = "NaN"
    Id: str | None = None
    ReliabilityIndex: float | str | None = "NaN"
    DistanceToConvergence: float | str | None = "NaN"
    SlipPlane: list[PersistablePoint | None] | None = None
    SoilContributions: list[PersistableSoilContribution | None] | None = None
    CalculationContributions: list[PersistableCalculationContribution | None] | None = (
        None
    )
    StateLinePointContributions: (
        list[PersistableStateLinePointContribution | None] | None
    ) = None
    StatePointContributions: list[PersistableStatePointContribution | None] | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    @classmethod
    def structure_group(cls) -> str:
        return "results/spencergeneticreliability/"

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
    FactorOfSafety: float | str | None = "NaN"
    Id: str | None = None
    Points: list[PersistablePoint | None] | None = None
    Slices: list[PersistableSpencerSlice | None] | None = None
    SlipPlane: list[PersistablePoint | None] | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
    FactorOfSafety: float | str | None = "NaN"
    Id: str | None = None
    LeftCenter: PersistablePoint | None = None
    Points: list[PersistablePoint | None] | None = None
    RightCenter: PersistablePoint | None = None
    Slices: list[PersistableSlice | None] | None = None
    TangentLine: float | str | None = "NaN"
    ResultThreshold: float | str | None = "NaN"
    SlipPlaneResults: list | None = None

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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
    Converged: bool | None = None
    FailureProbability: float | str | None = "NaN"
    Id: str | None = None
    LeftCenter: PersistablePoint | None = None
    ReliabilityIndex: float | str | None = "NaN"
    DistanceToConvergence: float | str | None = "NaN"
    RightCenter: PersistablePoint | None = None
    SoilContributions: list[PersistableSoilContribution | None] | None = None
    CalculationContributions: list[PersistableCalculationContribution | None] | None = (
        None
    )
    StateLinePointContributions: (
        list[PersistableStateLinePointContribution | None] | None
    ) = None
    StatePointContributions: list[PersistableStatePointContribution | None] | None = None
    TangentLine: float | str | None = "NaN"

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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


class UpliftVanParticleSwarmReliabilityResult(DStabilitySubStructure):
    ResultThreshold: float | str | None = "NaN"
    SlipPlaneResults: list | None = None
    Converged: bool | None = None
    FailureProbability: float | str | None = "NaN"
    Id: str | None = None
    LeftCenter: PersistablePoint | None = None
    ReliabilityIndex: float | str | None = "NaN"
    DistanceToConvergence: float | str | None = "NaN"
    RightCenter: PersistablePoint | None = None
    SoilContributions: list[PersistableSoilContribution | None] | None = None
    CalculationContributions: list[PersistableCalculationContribution | None] | None = (
        None
    )
    StateLinePointContributions: (
        list[PersistableStateLinePointContribution | None] | None
    ) = None
    StatePointContributions: list[PersistableStatePointContribution | None] | None = None
    TangentLine: float | str | None = "NaN"

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

    @classmethod
    def structure_group(cls) -> str:
        return "results/upliftvanparticleswarmreliability/"

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
    FactorOfSafety: float | str | None = "NaN"
    Id: str | None = None
    LeftCenter: PersistablePoint | None = None
    Points: list[PersistablePoint | None] | None = None
    RightCenter: PersistablePoint | None = None
    Slices: list[PersistableSlice | None] | None = None
    TangentLine: float | str | None = "NaN"

    @field_validator("Id", mode="before")
    def transform_id_to_str(cls, value) -> str:
        if value is None:
            return None
        return str(value)

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


DStabilityResult = (
    UpliftVanResult
    | UpliftVanParticleSwarmResult
    | UpliftVanReliabilityResult
    | UpliftVanParticleSwarmReliabilityResult
    | SpencerGeneticAlgorithmResult
    | SpencerReliabilityResult
    | SpencerGeneticAlgorithmReliabilityResult
    | SpencerResult
    | BishopBruteForceResult
    | BishopReliabilityResult
    | BishopBruteForceReliabilityResult
    | BishopResult
    | None
)


###########################
# INPUT AND OUTPUT COMBINED
###########################


class DStabilityStructure(BaseModelStructure):
    """Highest level DStability class that should be parsed to and serialized from.

    The list[] items (one for each stage in the model) will be stored in a subfolder
    to multiple json files. Where the first (0) instance
    has no suffix, but the second one has (1 => _1) etc.

    also parses the outputs which are part of the json files
    """

    # input part
    waternets: list[Waternet] = [Waternet(Id="14")]  # waternets/waternet_x.json
    waternetcreatorsettings: list[WaternetCreatorSettings] = [
        WaternetCreatorSettings(Id="15")
    ]  # waternetcreatorsettings/waternetcreatorsettings_x.json
    states: list[State] = [State(Id="16")]  # states/states_x.json
    statecorrelations: list[StateCorrelation] = [
        StateCorrelation(Id="17")
    ]  # statecorrelations/statecorrelations_x.json
    scenarios: list[Scenario] = [
        Scenario(
            Id="0",
            Label="Scenario 1",
            Notes="Default Scenario by GEOLib",
            Stages=[
                Stage(
                    DecorationsId="12",
                    GeometryId="11",
                    Id="43",
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
            ],
            Calculations=[
                PersistableCalculation(
                    CalculationSettingsId="20",
                    Id="42",
                    Label="Calculation 1",
                    Notes="Default calculation by GEOLib",
                )
            ],
        )
    ]
    soillayers: list[SoilLayerCollection] = [SoilLayerCollection(Id="13")]
    soilcorrelation: SoilCorrelation = SoilCorrelation()
    soils: SoilCollection = SoilCollection()
    soilvisualizations: SoilVisualisation = SoilVisualisation()
    reinforcements: list[Reinforcements] = [Reinforcements(Id="19")]
    projectinfo: ProjectInfo = ProjectInfo()
    nailproperties: NailProperties = NailProperties()
    loads: list[Loads] = [Loads(Id="18")]
    decorations: list[Decorations] = [Decorations(Id="12")]
    calculationsettings: list[CalculationSettings] = [CalculationSettings(Id="20")]
    geometries: list[Geometry] = [Geometry(Id="11")]

    # Output parts
    uplift_van_results: list[UpliftVanResult] = []
    uplift_van_particle_swarm_results: list[UpliftVanParticleSwarmResult] = []
    uplift_van_reliability_results: list[UpliftVanReliabilityResult] = []
    uplift_van_particle_swarm_reliability_results: list[
        UpliftVanParticleSwarmReliabilityResult
    ] = []
    spencer_results: list[SpencerResult] = []
    spencer_genetic_algorithm_results: list[SpencerGeneticAlgorithmResult] = []
    spencer_reliability_results: list[SpencerReliabilityResult] = []
    spencer_genetic_algorithm_reliability_results: list[
        SpencerGeneticAlgorithmReliabilityResult
    ] = []
    bishop_results: list[BishopResult] = []
    bishop_bruteforce_results: list[BishopBruteForceResult] = []
    bishop_reliability_results: list[BishopReliabilityResult] = []
    bishop_bruteforce_reliability_results: list[BishopBruteForceReliabilityResult] = []

    @model_validator(mode="after")
    def ensure_validity_foreign_keys(self):
        def list_has_id(values, id):
            for entry in values:
                if entry.Id == id:
                    return True
            return False

        for _, scenario in enumerate(self.scenarios):
            for _, stage in enumerate(scenario.Stages):
                if not list_has_id(self.decorations, stage.DecorationsId):
                    raise ValueError("DecorationsIds not linked!")
                if not list_has_id(self.geometries, stage.GeometryId):
                    raise ValueError("GeometryIds not linked!")
                if not list_has_id(self.loads, stage.LoadsId):
                    raise ValueError("LoadsIds not linked!")
                if not list_has_id(self.reinforcements, stage.ReinforcementsId):
                    raise ValueError("ReinforcementsIds not linked!")
                if not list_has_id(self.soillayers, stage.SoilLayersId):
                    raise ValueError("SoilLayersIds not linked!")
                if not list_has_id(self.states, stage.StateId):
                    raise ValueError("StateIds not linked!")
                if not list_has_id(self.statecorrelations, stage.StateCorrelationsId):
                    raise ValueError("StateCorrelationsIds not linked!")
                if not list_has_id(
                    self.waternetcreatorsettings, stage.WaternetCreatorSettingsId
                ):
                    raise ValueError("WaternetCreatorSettingsIds not linked!")
                if not list_has_id(self.waternets, stage.WaternetId):
                    raise ValueError("WaternetIds not linked!")
            for _, calculation in enumerate(scenario.Calculations):
                if not list_has_id(
                    self.calculationsettings, calculation.CalculationSettingsId
                ):
                    raise ValueError("CalculationSettingsIds not linked!")
        return self

    def add_default_scenario(
        self, label: str, notes: str, unique_start_id: int | None = None
    ) -> tuple[int, int]:
        """Add a new default (empty) scenario to DStability."""
        if unique_start_id is None:
            unique_start_id = self.get_unique_id()

        scenario_id = unique_start_id + 13

        self.waternets += [Waternet(Id=str(unique_start_id + 1))]
        self.waternetcreatorsettings += [
            WaternetCreatorSettings(Id=str(unique_start_id + 2))
        ]
        self.states += [State(Id=str(unique_start_id + 3))]
        self.statecorrelations += [StateCorrelation(Id=str(unique_start_id + 4))]
        self.soillayers += [SoilLayerCollection(Id=str(unique_start_id + 5))]
        self.soilcorrelation: SoilCorrelation = SoilCorrelation()
        self.reinforcements += [Reinforcements(Id=str(unique_start_id + 6))]
        self.loads += [Loads(Id=str(unique_start_id + 7))]
        self.decorations += [Decorations(Id=str(unique_start_id + 9))]
        self.calculationsettings += [CalculationSettings(Id=str(unique_start_id + 10))]
        self.geometries += [Geometry(Id=str(unique_start_id + 8))]
        self.scenarios += [
            Scenario(
                Id=str(scenario_id),
                Label=label,
                Notes=notes,
                Stages=[
                    Stage(
                        Id=str(unique_start_id + 11),
                        Label="Stage 1",
                        Notes="",
                        DecorationsId=str(unique_start_id + 9),
                        GeometryId=str(unique_start_id + 8),
                        LoadsId=str(unique_start_id + 7),
                        ReinforcementsId=str(unique_start_id + 6),
                        SoilLayersId=str(unique_start_id + 5),
                        StateId=str(unique_start_id + 3),
                        StateCorrelationsId=str(unique_start_id + 4),
                        WaternetCreatorSettingsId=str(unique_start_id + 2),
                        WaternetId=str(unique_start_id + 1),
                    )
                ],
                Calculations=[
                    PersistableCalculation(
                        Id=str(unique_start_id + 12),
                        Label="Calculation 1",
                        Notes="",
                        CalculationSettingsId=str(unique_start_id + 10),
                    )
                ],
            )
        ]

        return len(self.scenarios) - 1, scenario_id

    def add_default_stage(
        self,
        scenario_index: int,
        label: str,
        notes: str,
        unique_start_id: int | None = None,
    ) -> tuple[int, int]:
        """Add a new default (empty) stage to DStability."""
        if unique_start_id is None:
            unique_start_id = self.get_unique_id()

        stage_id = unique_start_id + 13

        self.waternets += [Waternet(Id=str(unique_start_id + 1))]
        self.waternetcreatorsettings += [
            WaternetCreatorSettings(Id=str(unique_start_id + 2))
        ]
        self.states += [State(Id=str(unique_start_id + 3))]
        self.statecorrelations += [StateCorrelation(Id=str(unique_start_id + 4))]
        self.soillayers += [SoilLayerCollection(Id=str(unique_start_id + 5))]
        self.soilcorrelation: SoilCorrelation = SoilCorrelation()
        self.reinforcements += [Reinforcements(Id=str(unique_start_id + 6))]
        self.loads += [Loads(Id=str(unique_start_id + 7))]
        self.decorations += [Decorations(Id=str(unique_start_id + 9))]
        self.geometries += [Geometry(Id=str(unique_start_id + 8))]

        new_stage = Stage(
            Id=str(stage_id),
            Label=label,
            Notes=notes,
            DecorationsId=str(unique_start_id + 9),
            GeometryId=str(unique_start_id + 8),
            LoadsId=str(unique_start_id + 7),
            ReinforcementsId=str(unique_start_id + 6),
            SoilLayersId=str(unique_start_id + 5),
            StateId=str(unique_start_id + 3),
            StateCorrelationsId=str(unique_start_id + 4),
            WaternetCreatorSettingsId=str(unique_start_id + 2),
            WaternetId=str(unique_start_id + 1),
        )

        scenario = self.scenarios[scenario_index]

        if scenario.Stages is None:
            scenario.Stages = []

        scenario.Stages.append(new_stage)
        return len(scenario.Stages) - 1, stage_id

    def add_default_calculation(
        self,
        scenario_index: int,
        label: str,
        notes: str,
        unique_start_id: int | None = None,
    ) -> tuple[int, int]:
        """Add a new default (empty) calculation to DStability."""
        if unique_start_id is None:
            unique_start_id = self.get_unique_id()

        calculation_id = unique_start_id + 13

        self.calculationsettings += [CalculationSettings(Id=str(unique_start_id + 1))]

        new_calculation = PersistableCalculation(
            Id=str(calculation_id),
            Label=label,
            Notes=notes,
            CalculationSettingsId=str(unique_start_id + 1),
        )

        scenario = self.scenarios[scenario_index]

        if scenario.Calculations is None:
            scenario.Calculations = []

        scenario.Calculations.append(new_calculation)
        return len(scenario.Calculations) - 1, calculation_id

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

    def has_stage(self, scenario_index: int, stage_index: int) -> bool:
        try:
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            scenario.Stages[stage_index]
            return True
        except IndexError:
            return False

    def has_calculation(self, scenario_index: int, calculation_index: int) -> bool:
        try:
            scenario = self.scenarios[scenario_index]

            if scenario.Calculations is None:
                return False

            scenario.Calculations[calculation_index]
            return True
        except IndexError:
            return False

    def has_scenario(self, scenario_index: int) -> bool:
        try:
            self.scenarios[scenario_index]
            return True
        except IndexError:
            return False

    def has_result(self, scenario_index: int, calculation_index: int) -> bool:
        if self.has_calculation(scenario_index, calculation_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Calculations is None:
                return False

            result_id = scenario.Calculations[calculation_index].ResultId
            if result_id is None:
                return False
            else:
                return True
        return False

    def has_loads(self, scenario_index: int, stage_index: int) -> bool:
        if self.has_stage(scenario_index, stage_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            loads_id = scenario.Stages[stage_index].LoadsId
            if loads_id is None:
                return False
            else:
                return True
        return False

    def has_soil_layers(self, scenario_index: int, stage_index: int) -> bool:
        if self.has_stage(scenario_index, stage_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            soil_layers_id = scenario.Stages[stage_index].SoilLayersId
            if soil_layers_id is None:
                return False
            else:
                return True
        return False

    def has_soil_layer(
        self, scenario_index: int, stage_index: int, soil_layer_id: int
    ) -> bool:
        if self.has_soil_layers(scenario_index, stage_index):
            for layer in self.soillayers[stage_index].SoilLayers:
                if str(soil_layer_id) == layer.LayerId:
                    return True
            return False
        return False

    def has_reinforcements(self, scenario_index: int, stage_index: int) -> bool:
        if self.has_stage(scenario_index, stage_index):
            scenario = self.scenarios[scenario_index]

            if scenario.Stages is None:
                return False

            reinforcements_id = scenario.Stages[stage_index].ReinforcementsId
            if reinforcements_id is None:
                return False
            else:
                return True
        return False

    def _get_soil_layers(self, scenario_index: int, stage_index: int):
        soil_layers_id = self.scenarios[scenario_index].Stages[stage_index].SoilLayersId

        for soil_layers in self.soillayers:
            if soil_layers.Id == soil_layers_id:
                return soil_layers

        raise ValueError(
            f"No soil layers found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_excavations(self, scenario_index: int, stage_index: int):
        decorations_id = self.scenarios[scenario_index].Stages[stage_index].DecorationsId

        for decoration in self.decorations:
            if decoration.Id == decorations_id:
                return decoration.Excavations

        raise ValueError(
            f"No excavations found for stage {stage_index} in scenario {scenario_index}."
        )

    def _get_loads(self, scenario_index: int, stage_index: int):
        loads_id = self.scenarios[scenario_index].Stages[stage_index].LoadsId

        for loads in self.loads:
            if loads.Id == loads_id:
                return loads

        raise ValueError(
            f"No loads found for stage {stage_index} in scenario {scenario_index}."
        )

    def get_result_substructure(
        self, analysis_type: AnalysisTypeEnum, calculation_type: CalculationTypeEnum
    ) -> list[DStabilityResult]:
        result_types_mapping = {
            AnalysisTypeEnum.UPLIFT_VAN: {
                "non_probabilistic": self.uplift_van_results,
                "probabilistic": self.uplift_van_reliability_results,
            },
            AnalysisTypeEnum.UPLIFT_VAN_PARTICLE_SWARM: {
                "non_probabilistic": self.uplift_van_particle_swarm_results,
                "probabilistic": self.uplift_van_particle_swarm_reliability_results,
            },
            AnalysisTypeEnum.SPENCER_GENETIC: {
                "non_probabilistic": self.spencer_genetic_algorithm_results,
                "probabilistic": self.spencer_genetic_algorithm_reliability_results,
            },
            AnalysisTypeEnum.SPENCER: {
                "non_probabilistic": self.spencer_results,
                "probabilistic": self.spencer_reliability_results,
            },
            AnalysisTypeEnum.BISHOP_BRUTE_FORCE: {
                "non_probabilistic": self.bishop_bruteforce_results,
                "probabilistic": self.bishop_bruteforce_reliability_results,
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

    mapping: dict[str, tuple[str, ...]] = {
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
            "PersistableElevation.AddedLayerId",
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
        "CalculationSettings.Id": ("Calculation.CalculationSettingsId",),
        "Decorations.Id": ("Stage.DecorationsId",),
        "Geometry.Id": ("Stage.GeometryId",),
        "Loads.Id": ("Stage.LoadsId",),
        "Reinforcements.Id": ("Stage.ReinforcementsId",),
        "Result.Id": ("Calculation.ResultId",),
        "SoilLayerCollection.Id": ("Stage.SoilLayersId",),
        "StateCorrelation.Id": ("Stage.StateCorrelationsId",),
        "State.Id": ("Stage.StateId",),
        "WaternetCreatorSettings.Id": ("Stage.WaternetCreatorSettingsId",),
        "Calculation.Id": ("PersistableCalculationContribution.CalculationId",),
        "PersistableStateLinePoint.Id": (
            "PersistableStateCorrelation.CorrelatedStateIds",
            "PersistableStateLinePointContribution.StateLinePointId",
        ),
        "PersistableStatePoint.Id": ("PersistableStatePointContribution.StatePointId",),
    }

    @property
    def class_fields(self) -> dict[str, list[str]]:
        """Return a mapping in the form:
        classname: [fields]
        """
        id_keys = chain(*((k, *v) for k, v in self.mapping.items()))
        class_fields = defaultdict(list)
        for id_key in id_keys:
            classname, fieldname = id_key.split(".")
            class_fields[classname].append(fieldname)
        return class_fields
