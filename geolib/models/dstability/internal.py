import inspect
import sys
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel as DataModel
from pydantic import validator

from geolib import __version__ as version
from geolib.models.base_model import BaseModelStructure

from .dstability_validator import DStabilityValidator

BaseModelStructure.Config.arbitrary_types_allowed = True
DataModel.Config.arbitrary_types_allowed = True


class DStabilitySubStructure(BaseModelStructure):
    @classmethod
    def structure_name(cls):
        class_name = cls.__name__
        return str.split(str.lower(class_name), ".")[-1]

    @classmethod
    def structure_group(cls):
        return cls.structure_name()


# waternet schema
class PersistablePoint(DataModel):
    X: Optional[float]
    Z: Optional[float]


class PersistableHeadLine(DataModel):
    Id: Optional[str]
    Label: Optional[str]
    Notes: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class PersistableReferenceLine(DataModel):
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

    ContentVersion: Optional[str]
    HeadLines: Optional[List[Optional[PersistableHeadLine]]]
    Id: Optional[str]
    PhreaticLineId: Optional[str]
    ReferenceLines: Optional[List[Optional[PersistableReferenceLine]]]
    UnitWeightWater: Optional[float]


# waternet creator


class PersistableDitchCharacteristics(DataModel):
    DitchBottomEmbankmentSide: Optional[float]
    DitchBottomLandSide: Optional[float]
    DitchEmbankmentSide: Optional[float]
    DitchLandSide: Optional[float]


class PersistableEmbankmentCharacteristics(DataModel):
    EmbankmentToeLandSide: Optional[float]
    EmbankmentToeWaterSide: Optional[float]
    EmbankmentTopLandSide: Optional[float]
    EmbankmentTopWaterSide: Optional[float]
    ShoulderBaseLandSide: Optional[float]


class EmbankmentSoilScenario(str, Enum):
    CLAY_EMBANKMENT_ON_CLAY = "ClayEmbankmentOnClay"
    CLAY_EMBANKMENT_ON_SAND = "ClayEmbankmentOnSand"
    SAND_EMBANKMENT_ON_CLAY = "SandEmbankmentOnClay"
    SAND_EMBANKMENT_ON_SAND = "SandEmbankmentOnSand"


class WaternetCreatorSettings(DStabilitySubStructure):
    """waternetcreatorsettings/waternetcreatorsettings_x.json"""

    AdjustForUplift: Optional[bool]
    AquiferInsideAquitardLayerId: Optional[str]
    AquiferLayerId: Optional[str]
    AquiferLayerInsideAquitardLeakageLengthInwards: Optional[float]
    AquiferLayerInsideAquitardLeakageLengthOutwards: Optional[float]
    AquitardHeadLandSide: Optional[float]
    AquitardHeadWaterSide: Optional[float]
    ContentVersion: Optional[str]
    DitchCharacteristics: Optional[PersistableDitchCharacteristics]
    DrainageConstruction: Optional[PersistablePoint]
    EmbankmentCharacteristics: Optional[PersistableEmbankmentCharacteristics]
    EmbankmentSoilScenario: Optional[EmbankmentSoilScenario]
    Id: Optional[str]
    InitialLevelEmbankmentTopLandSide: Optional[float]
    InitialLevelEmbankmentTopWaterSide: Optional[float]
    IntrusionLength: Optional[float]
    IsAquiferLayerInsideAquitard: Optional[bool]
    IsDitchPresent: Optional[bool]
    IsDrainageConstructionPresent: Optional[bool]
    MeanWaterLevel: Optional[float]
    NormativeWaterLevel: Optional[float]
    OffsetEmbankmentToeLandSide: Optional[float]
    OffsetEmbankmentTopLandSide: Optional[float]
    OffsetEmbankmentTopWaterSide: Optional[float]
    OffsetShoulderBaseLandSide: Optional[float]
    PleistoceneLeakageLengthInwards: Optional[float]
    PleistoceneLeakageLengthOutwards: Optional[float]
    UseDefaultOffsets: Optional[bool]
    WaterLevelHinterland: Optional[float]

    @classmethod
    def structure_group(cls) -> str:
        return "waternetcreatorsettings"


# stateschema.json


class PersistableStochasticParameter(DataModel):
    IsProbabilistic: Optional[bool]
    Mean: Optional[float]
    StandardDeviation: Optional[float]


class StateType(Enum):
    OCR = "Ocr"
    POP = "Pop"
    YIELD_STRESS = "YieldStress"


class PersistableStress(DataModel):
    Ocr: Optional[float]
    Pop: Optional[float]
    PopStochasticParameter: Optional[PersistableStochasticParameter]
    StateType: Optional[StateType]
    YieldStress: Optional[float]


class PersistableStateLinePoint(DataModel):
    Above: Optional[PersistableStress]
    Below: Optional[PersistableStress]
    Id: Optional[str]
    IsAboveAndBelowCorrelated: Optional[bool]
    IsProbabilistic: Optional[bool]
    Label: Optional[str]
    X: Optional[float]


class PersistableStateLine(DataModel):
    Points: Optional[List[Optional[PersistablePoint]]]
    Values: Optional[List[Optional[PersistableStateLinePoint]]]


class PersistableStatePoint(DataModel):
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

    ContentVersion: Optional[str]
    Id: Optional[str]
    StateLines: Optional[List[Optional[PersistableStateLine]]]
    StatePoints: Optional[List[Optional[PersistableStatePoint]]]


# statecorrelation


class PersistableStateCorrelation(DataModel):
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

    ContentVersion: Optional[str]
    Id: Optional[str]
    StateCorrelations: Optional[List[Optional[PersistableStateCorrelation]]]


class Stage(DStabilitySubStructure):
    """stages/stage_x.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "stage"

    @classmethod
    def structure_group(cls) -> str:
        return "stages"

    CalculationSettingsId: Optional[str]
    ContentVersion: Optional[str]
    DecorationsId: Optional[str]
    GeometryId: Optional[str]
    Id: Optional[str]
    Label: Optional[str]
    LoadsId: Optional[str]
    Notes: Optional[str]
    ReinforcementsId: Optional[str]
    ResultId: Optional[str]
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


class PersistableSoilVisualization(DataModel):
    Color: Optional[str]
    PersistableShadingType: Optional[PersistableShadingType]
    SoilId: Optional[str]


class SoilVisualisation(DataModel):
    ContentVersion: Optional[str]
    SoilVisualizations: Optional[List[Optional[PersistableSoilVisualization]]]


class PersistableSoilLayer(DataModel):
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

    ContentVersion: Optional[str]
    Id: Optional[str]
    SoilLayers: Optional[List[Optional[PersistableSoilLayer]]]


class PersistableSoilCorrelation(DataModel):
    CorrelatedSoilIds: Optional[List[Optional[str]]]


class SoilCorrelation(DStabilitySubStructure):
    """soilcorrelations.json"""

    ContentVersion: Optional[str]
    SoilCorrelations: Optional[List[Optional[PersistableSoilCorrelation]]]

    @classmethod
    def structure_name(cls) -> str:
        return "soilcorrelations"


class ShearStrengthModelTypePhreaticLevel(Enum):
    C_PHI = "CPhi"
    NONE = "None"
    SU = "Su"


class PersistableSoil(DataModel):
    Code: Optional[str]
    Cohesion: Optional[float]
    CohesionAndFrictionAngleCorrelated: Optional[bool]
    CohesionStochasticParameter: Optional[PersistableStochasticParameter]
    Dilatancy: Optional[float]
    DilatancyStochasticParameter: Optional[PersistableStochasticParameter]
    FrictionAngle: Optional[float]
    FrictionAngleStochasticParameter: Optional[PersistableStochasticParameter]
    Id: Optional[str]
    IsProbabilistic: Optional[bool]
    Name: Optional[str]
    ShearStrengthModelTypeAbovePhreaticLevel: Optional[
        ShearStrengthModelTypePhreaticLevel
    ]
    ShearStrengthModelTypeBelowPhreaticLevel: Optional[
        ShearStrengthModelTypePhreaticLevel
    ]
    ShearStrengthRatio: Optional[float]
    ShearStrengthRatioAndShearStrengthExponentCorrelated: Optional[bool]
    ShearStrengthRatioStochasticParameter: Optional[PersistableStochasticParameter]
    StrengthIncreaseExponent: Optional[float]
    StrengthIncreaseExponentStochasticParameter: Optional[
        PersistableStochasticParameter
    ]
    VolumetricWeightAbovePhreaticLevel: Optional[float]
    VolumetricWeightBelowPhreaticLevel: Optional[float]


class SoilCollection(DStabilitySubStructure):
    """soils.json"""

    @classmethod
    def structure_name(cls) -> str:
        return "soils"

    ContentVersion: Optional[str]
    Soils: Optional[List[Optional[PersistableSoil]]]


# Reinforcements


class PersistableForbiddenLine(DataModel):
    End: Optional[PersistablePoint]
    Label: Optional[str]
    Start: Optional[PersistablePoint]


class PersistableGeotextile(DataModel):
    End: Optional[PersistablePoint]
    Label: Optional[str]
    ReductionArea: Optional[float]
    Start: Optional[PersistablePoint]
    TensileStrength: Optional[float]


class PersistableStressAtDistance(DataModel):
    Distance: Optional[float]
    Stress: Optional[float]


class PersistableNail(DataModel):
    BendingStiffness: Optional[float]
    CriticalAngle: Optional[float]
    Diameter: Optional[float]
    Direction: Optional[float]
    GroutDiameter: Optional[float]
    HorizontalSpacing: Optional[float]
    Label: Optional[str]
    LateralStresses: Optional[List[Optional[PersistableStressAtDistance]]]
    Length: Optional[float]
    Location: Optional[PersistablePoint]
    MaxPullForce: Optional[float]
    PlasticMoment: Optional[float]
    ShearStresses: Optional[List[Optional[PersistableStressAtDistance]]]
    UseFacing: Optional[bool]
    UseLateralStress: Optional[bool]
    UseShearStress: Optional[bool]


class Reinforcements(DStabilitySubStructure):
    """reinforcements/reinforcements_x.json"""

    ContentVersion: Optional[str]
    ForbiddenLines: Optional[List[Optional[PersistableForbiddenLine]]]
    Geotextiles: Optional[List[Optional[PersistableGeotextile]]]
    Id: Optional[str]
    Nails: Optional[List[Optional[PersistableNail]]]


class ProjectInfo(DStabilitySubStructure):
    """projectinfo.json."""

    Analyst: Optional[str]
    ContentVersion: Optional[str]
    Created: Optional[date] = datetime.now().date()
    CrossSection: Optional[str]
    Date: Optional[date] = datetime.now().date()
    IsDataValidated: Optional[bool] = False
    LastModified: Optional[date] = datetime.now().date()
    LastModifier: Optional[str] = "GEOLib"
    Path: Optional[str]
    Project: Optional[str]
    Remarks: Optional[str] = f"Created with GEOLib {version}"

    @validator("Created", "Date", "LastModified", pre=True, allow_reuse=True)
    def nltime(cls, datestring):
        return datetime.strptime(datestring, "%d-%M-%Y").date()


class PersistableBondStress(DataModel):
    Sigma: Optional[float]
    Tau: Optional[float]


class PersistableNailPropertiesForSoil(DataModel):
    BondStresses: Optional[List[Optional[PersistableBondStress]]]
    CompressionRatio: Optional[float]
    RheologicalCoefficient: Optional[float]
    SoilId: Optional[str]


class NailProperties(DStabilitySubStructure):
    """nailpropertiesforsoils.json"""

    ContentVersion: Optional[str]
    NailPropertiesForSoils: Optional[List[Optional[PersistableNailPropertiesForSoil]]]

    @classmethod
    def structure_name(cls) -> str:
        return "nailpropertiesforsoils"


class PersistableConsolidation(DataModel):
    Degree: Optional[float]
    LayerId: Optional[str]


class PersistableEarthquake(DataModel):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    FreeWaterFactor: Optional[float]
    HorizontalFactor: Optional[float]
    IsEnabled: Optional[bool]
    VerticalFactor: Optional[float]


class PersistableLayerLoad(DataModel):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    LayerId: Optional[str]


class PersistableLineLoad(DataModel):
    Angle: Optional[float]
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    Label: Optional[str]
    Location: Optional[PersistablePoint]
    Magnitude: Optional[float]
    Spread: Optional[float]


class PersistableTree(DataModel):
    Force: Optional[float]
    Label: Optional[str]
    Location: Optional[PersistablePoint]
    RootZoneWidth: Optional[float]
    Spread: Optional[float]


class PersistableUniformLoad(DataModel):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    End: Optional[float]
    Label: Optional[str]
    Magnitude: Optional[float]
    Spread: Optional[float]
    Start: Optional[float]


class Loads(DStabilitySubStructure):
    """loads/loads_x.json"""

    ContentVersion: Optional[str]
    Earthquake: Optional[PersistableEarthquake]
    Id: Optional[str]
    LayerLoads: Optional[List[Optional[PersistableLayerLoad]]]
    LineLoads: Optional[List[Optional[PersistableLineLoad]]]
    Trees: Optional[List[Optional[PersistableTree]]]
    UniformLoads: Optional[List[Optional[PersistableUniformLoad]]]


class PersistableLayer(DataModel):
    Id: Optional[str]
    Label: Optional[str]
    Notes: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class Geometry(DStabilitySubStructure):
    """geometries/geometry_x.json"""

    @classmethod
    def structure_group(cls) -> str:
        return "geometries"

    ContentVersion: Optional[str]
    Id: Optional[str]
    Layers: Optional[List[Optional[PersistableLayer]]]


class PersistableBerm(DataModel):
    AddedLayerId: Optional[str]
    Label: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class PersistableExcavation(DataModel):
    Label: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class Decorations(DStabilitySubStructure):
    """decorations/decorations_x.json."""

    Berms: Optional[List[Optional[PersistableBerm]]]
    ContentVersion: Optional[str]
    Excavations: Optional[List[Optional[PersistableExcavation]]]
    Id: Optional[str]


# Calculation Settings


class AnalysisType(Enum):
    BISHOP = "Bishop"
    BISHOP_BRUTE_FORCE = "BishopBruteForce"
    SPENCER = "Spencer"
    SPENCER_GENETIC = "SpencerGenetic"
    UPLIFT_VAN = "UpliftVan"
    UPLIFT_VAN_PARTICLE_SWARM = "UpliftVanParticleSwarm"


class PersistableCircle(DataModel):
    Center: Optional[PersistablePoint]
    Radius: Optional[float]


class PersistableBishopSettings(DataModel):
    Circle: Optional[PersistableCircle]


class PersistableGridEnhancements(DataModel):
    ExtrapolateSearchSpace: Optional[bool]


class NullablePersistablePoint(DataModel):
    X: Optional[float]
    Z: Optional[float]


class PersistableSearchGrid(DataModel):
    BottomLeft: Optional[NullablePersistablePoint]
    NumberOfPointsInX: Optional[int]
    NumberOfPointsInZ: Optional[int]
    Space: Optional[float]


class PersistableSlipPlaneConstraints(DataModel):
    IsSizeConstraintsEnabled: Optional[bool]
    IsZoneAConstraintsEnabled: Optional[bool]
    IsZoneBConstraintsEnabled: Optional[bool]
    MinimumSlipPlaneDepth: Optional[float]
    MinimumSlipPlaneLength: Optional[float]
    WidthZoneA: Optional[float]
    WidthZoneB: Optional[float]
    XLeftZoneA: Optional[float]
    XLeftZoneB: Optional[float]


class PersistableTangentLines(DataModel):
    BottomTangentLineZ: Optional[float]
    NumberOfTangentLines: Optional[int]
    Space: Optional[float]


class PersistableBishopBruteForceSettings(DataModel):
    GridEnhancements: Optional[PersistableGridEnhancements]
    SearchGrid: Optional[PersistableSearchGrid]
    SlipPlaneConstraints: Optional[PersistableSlipPlaneConstraints]
    TangentLines: Optional[PersistableTangentLines]


class CalculationType(Enum):
    DESIGN = "Design"
    DETERMINISTIC = "Deterministic"
    MEAN = "Mean"
    PROBABILISTIC = "Probabilistic"


class PersistableSpencerSettings(DataModel):
    SlipPlane: Optional[List[Optional[PersistablePoint]]]


class OptionsType(Enum):
    DEFAULT = "Default"
    THOROUGH = "Thorough"


class PersistableGeneticSlipPlaneConstraints(DataModel):
    IsEnabled: Optional[bool]
    MinimumAngleBetweenSlices: Optional[float]
    MinimumThrustLinePercentageInsideSlices: Optional[float]


class PersistableSpencerGeneticSettings(DataModel):
    OptionsType: Optional[OptionsType]
    SlipPlaneA: Optional[List[Optional[PersistablePoint]]]
    SlipPlaneB: Optional[List[Optional[PersistablePoint]]]
    SlipPlaneConstraints: Optional[PersistableGeneticSlipPlaneConstraints]


class PersistableTwoCirclesOnTangentLine(DataModel):
    FirstCircleCenter: Optional[NullablePersistablePoint]
    FirstCircleRadius: Optional[float]
    SecondCircleCenter: Optional[NullablePersistablePoint]


class PersistableUpliftVanSettings(DataModel):
    SlipPlane: Optional[PersistableTwoCirclesOnTangentLine]


class PersistableSearchArea(DataModel):
    Height: Optional[float]
    TopLeft: Optional[NullablePersistablePoint]
    Width: Optional[float]


class PersistableTangentArea(DataModel):
    Height: Optional[float]
    TopZ: Optional[float]


class PersistableUpliftVanParticleSwarmSettings(DataModel):
    OptionsType: Optional[OptionsType]
    SearchAreaA: Optional[PersistableSearchArea]
    SearchAreaB: Optional[PersistableSearchArea]
    SlipPlaneConstraints: Optional[PersistableSlipPlaneConstraints]
    TangentArea: Optional[PersistableTangentArea]


class CalculationSettings(DStabilitySubStructure):
    """calculationsettings/calculationsettings_x.json"""

    AnalysisType: Optional[AnalysisType]
    Bishop: Optional[PersistableBishopSettings]
    BishopBruteForce: Optional[PersistableBishopBruteForceSettings]
    CalculationType: Optional[CalculationType]
    ContentVersion: Optional[str]
    Id: Optional[str]
    ModelFactorMean: Optional[float]
    ModelFactorStandardDeviation: Optional[float]
    Spencer: Optional[PersistableSpencerSettings]
    SpencerGenetic: Optional[PersistableSpencerGeneticSettings]
    UpliftVan: Optional[PersistableUpliftVanSettings]
    UpliftVanParticleSwarm: Optional[PersistableUpliftVanParticleSwarmSettings]


class DStabilityInputStructure(BaseModelStructure):
    """Highest level DStability class that should be parsed to and serialized from.

    The List[] items (one for each stage in the model) will be stored in a subfolder 
    to multiple json files. Where the first (0) instance
    has no suffix, but the second one has (1 => _1) etc."""

    waternets: List[Waternet] = [Waternet()]  # waternets/waternet_x.json
    waternetcreatorsettings: List[WaternetCreatorSettings] = [
        WaternetCreatorSettings()
    ]  # waternetcreatorsettings/waternetcreatorsettings_x.json
    states: List[State] = [State()]  # states/states_x.json
    statecorrelations: List[StateCorrelation] = [
        StateCorrelation()
    ]  # statecorrelations/statecorrelations_x.json
    stages: List[Stage] = [Stage()]  # stages/stage_x.json
    soillayers: List[SoilLayerCollection] = [
        SoilLayerCollection()
    ]  # soillayers/soillayers_x.json
    soilcorrelation: SoilCorrelation = SoilCorrelation()  # soilcorrelations.json
    soils: SoilCollection = SoilCollection()  # soils.json
    reinforcements: List[Reinforcements] = [
        Reinforcements()
    ]  # reinforcements/reinforcements_x.json
    projectinfo: ProjectInfo = ProjectInfo()  # projectinfo.json
    nailproperties: NailProperties = NailProperties()  # nailpropertiesforsoils.json
    loads: List[Loads] = [Loads()]  # loads/loads_x.json
    decorations: List[Decorations] = [Decorations()]  # decorations/decorations_x.json
    calculationsettings: List[CalculationSettings] = [
        CalculationSettings()
    ]  # calculationsettings/calculationsettings_x.json
    geometries: List[Geometry] = [Geometry()]  # geometries/geometry_x.json

    def validator(self):
        return DStabilityValidator(self)
