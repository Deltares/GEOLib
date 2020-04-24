import inspect
import sys, re
from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel as DataClass
from pydantic import validator

from geolib.models import BaseModel
from geolib import __version__ as version
from geolib.models.base_model_structure import BaseModelStructure
from geolib.soils import Soil

from .dstability_validator import DStabilityValidator

_CAMEL_TO_SNAKE_PATTERN = re.compile(r'(?<!^)(?=[A-Z])')
def camel_to_snake(name: str) -> str:  # TODO move to utils
  name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
  return _CAMEL_TO_SNAKE_PATTERN.sub('_', name).lower()

def snake_to_camel(name: str) -> str:  # TODO move to utils
    return ''.join(word.title() for word in name.split('_'))

BaseModelStructure.Config.arbitrary_types_allowed = True
DataClass.Config.arbitrary_types_allowed = True


class DStabilitySubStructure(BaseModelStructure):
    @classmethod
    def structure_name(cls):
        class_name = cls.__name__
        return str.split(str.lower(class_name), ".")[-1]

    @classmethod
    def structure_group(cls):
        return cls.structure_name()


# waternet schema
class PersistablePoint(DataClass):
    X: Optional[float]
    Z: Optional[float]


class PersistableHeadLine(DataClass):
    Id: Optional[str]
    Label: Optional[str]
    Notes: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class PersistableReferenceLine(DataClass):
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


class PersistableDitchCharacteristics(DataClass):
    DitchBottomEmbankmentSide: Optional[float]
    DitchBottomLandSide: Optional[float]
    DitchEmbankmentSide: Optional[float]
    DitchLandSide: Optional[float]


class PersistableEmbankmentCharacteristics(DataClass):
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


class PersistableStochasticParameter(DataClass):
    IsProbabilistic: Optional[bool]
    Mean: Optional[float]
    StandardDeviation: Optional[float]


class StateType(Enum):
    OCR = "Ocr"
    POP = "Pop"
    YIELD_STRESS = "YieldStress"


class PersistableStress(DataClass):
    Ocr: Optional[float]
    Pop: Optional[float]
    PopStochasticParameter: Optional[PersistableStochasticParameter]
    StateType: Optional[StateType]
    YieldStress: Optional[float]


class PersistableStateLinePoint(DataClass):
    Above: Optional[PersistableStress]
    Below: Optional[PersistableStress]
    Id: Optional[str]
    IsAboveAndBelowCorrelated: Optional[bool]
    IsProbabilistic: Optional[bool]
    Label: Optional[str]
    X: Optional[float]


class PersistableStateLine(DataClass):
    Points: Optional[List[Optional[PersistablePoint]]]
    Values: Optional[List[Optional[PersistableStateLinePoint]]]


class PersistableStatePoint(DataClass):
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


class PersistableStateCorrelation(DataClass):
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


class PersistableSoilVisualization(DataClass):
    Color: Optional[str]
    PersistableShadingType: Optional[PersistableShadingType]
    SoilId: Optional[str]


class SoilVisualisation(DataClass):
    ContentVersion: Optional[str]
    SoilVisualizations: Optional[List[Optional[PersistableSoilVisualization]]]


class PersistableSoilLayer(DataClass):
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
    SoilLayers: Optional[List[Optional[PersistableSoilLayer]]] = []


class PersistableSoilCorrelation(DataClass):
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


class PersistableSoil(DataClass):
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
    StrengthIncreaseExponentStochasticParameter: Optional[PersistableStochasticParameter]
    VolumetricWeightAbovePhreaticLevel: Optional[float]
    VolumetricWeightBelowPhreaticLevel: Optional[float]

    @classmethod
    def from_soil(cls, soil: Soil) -> "PersistableSoil":
        """
        Convert Soil to PersistableSoil.

        Args:
            soil (Soil): the given soil

        Returns:
            PersistableSoil: Converted soil
        """
        # convert snake_case members to CamelCase
        return cls(
            **{snake_to_camel(k): v for k, v in dict(soil).items()}            
        )

    def to_soil(self) -> Soil:
        """
        Convert PersistableSoil to Soil

        Returns:
            Soil: Converted PersistableSoil
        """
        # convert CamelCase members to snake_case
        return Soil(
            **{
                camel_to_snake(k) : v for k, v in dict(self).items()
            }
        )


class SoilCollection(DStabilitySubStructure):
    """soils.json"""

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

    def add_soil(self, soil: Soil) -> None:
        """
        Add a new soil to the model.

        Args:
            soil (Soil): a new soil

        Returns:
            None
        """
        ps = PersistableSoil.from_soil(soil)
        self.Soils.append(ps)

    def get_soil(self, id: int) -> Soil:
        """
        Get soil by the given id.

        Args:
            id (int): id of the soil

        Returns:
            Soil: or None if not available
        """
        for s in self.Soils:
            if s.Id == id:
                return s.to_soil()
        raise ValueError(f"Soil id {id} not found in the SoilCollection")

    def edit_soil(self, soil: Soil) -> None:
        """
        Update a soil.

        Args:
            soil (Soil): soil class with the new properties

        Returns:
            bool: True for succes, False otherwise
        """
        for ps in self.Soils:
            if ps.Code == soil.code:
                ps.from_soil(soil)
                return True

        return False

    ContentVersion: Optional[str]
    Soils: List[Optional[PersistableSoil]] = []


# Reinforcements


class PersistableForbiddenLine(DataClass):
    End: Optional[PersistablePoint]
    Label: Optional[str]
    Start: Optional[PersistablePoint]


class PersistableGeotextile(DataClass):
    End: Optional[PersistablePoint]
    Label: Optional[str]
    ReductionArea: Optional[float]
    Start: Optional[PersistablePoint]
    TensileStrength: Optional[float]


class PersistableStressAtDistance(DataClass):
    Distance: Optional[float]
    Stress: Optional[float]


class PersistableNail(DataClass):
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


class PersistableBondStress(DataClass):
    Sigma: Optional[float]
    Tau: Optional[float]


class PersistableNailPropertiesForSoil(DataClass):
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


class PersistableConsolidation(DataClass):
    Degree: Optional[float]
    LayerId: Optional[str]


class PersistableEarthquake(DataClass):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    FreeWaterFactor: Optional[float]
    HorizontalFactor: Optional[float]
    IsEnabled: Optional[bool]
    VerticalFactor: Optional[float]


class PersistableLayerLoad(DataClass):
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    LayerId: Optional[str]


class PersistableLineLoad(DataClass):
    Angle: Optional[float]
    Consolidations: Optional[List[Optional[PersistableConsolidation]]]
    Label: Optional[str]
    Location: Optional[PersistablePoint]
    Magnitude: Optional[float]
    Spread: Optional[float]


class PersistableTree(DataClass):
    Force: Optional[float]
    Label: Optional[str]
    Location: Optional[PersistablePoint]
    RootZoneWidth: Optional[float]
    Spread: Optional[float]


class PersistableUniformLoad(DataClass):
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


class PersistableLayer(DataClass):
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


class PersistableBerm(DataClass):
    AddedLayerId: Optional[str]
    Label: Optional[str]
    Points: Optional[List[Optional[PersistablePoint]]]


class PersistableExcavation(DataClass):
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


class PersistableCircle(DataClass):
    Center: Optional[PersistablePoint]
    Radius: Optional[float]


class PersistableBishopSettings(DataClass):
    Circle: Optional[PersistableCircle]


class PersistableGridEnhancements(DataClass):
    ExtrapolateSearchSpace: Optional[bool]


class NullablePersistablePoint(DataClass):
    X: Optional[float]
    Z: Optional[float]


class PersistableSearchGrid(DataClass):
    BottomLeft: Optional[NullablePersistablePoint]
    NumberOfPointsInX: Optional[int]
    NumberOfPointsInZ: Optional[int]
    Space: Optional[float]


class PersistableSlipPlaneConstraints(DataClass):
    IsSizeConstraintsEnabled: Optional[bool]
    IsZoneAConstraintsEnabled: Optional[bool]
    IsZoneBConstraintsEnabled: Optional[bool]
    MinimumSlipPlaneDepth: Optional[float]
    MinimumSlipPlaneLength: Optional[float]
    WidthZoneA: Optional[float]
    WidthZoneB: Optional[float]
    XLeftZoneA: Optional[float]
    XLeftZoneB: Optional[float]


class PersistableTangentLines(DataClass):
    BottomTangentLineZ: Optional[float]
    NumberOfTangentLines: Optional[int]
    Space: Optional[float]


class PersistableBishopBruteForceSettings(DataClass):
    GridEnhancements: Optional[PersistableGridEnhancements]
    SearchGrid: Optional[PersistableSearchGrid]
    SlipPlaneConstraints: Optional[PersistableSlipPlaneConstraints]
    TangentLines: Optional[PersistableTangentLines]


class CalculationType(Enum):
    DESIGN = "Design"
    DETERMINISTIC = "Deterministic"
    MEAN = "Mean"
    PROBABILISTIC = "Probabilistic"


class PersistableSpencerSettings(DataClass):
    SlipPlane: Optional[List[Optional[PersistablePoint]]]


class OptionsType(Enum):
    DEFAULT = "Default"
    THOROUGH = "Thorough"


class PersistableGeneticSlipPlaneConstraints(DataClass):
    IsEnabled: Optional[bool]
    MinimumAngleBetweenSlices: Optional[float]
    MinimumThrustLinePercentageInsideSlices: Optional[float]


class PersistableSpencerGeneticSettings(DataClass):
    OptionsType: Optional[OptionsType]
    SlipPlaneA: Optional[List[Optional[PersistablePoint]]]
    SlipPlaneB: Optional[List[Optional[PersistablePoint]]]
    SlipPlaneConstraints: Optional[PersistableGeneticSlipPlaneConstraints]


class PersistableTwoCirclesOnTangentLine(DataClass):
    FirstCircleCenter: Optional[NullablePersistablePoint]
    FirstCircleRadius: Optional[float]
    SecondCircleCenter: Optional[NullablePersistablePoint]


class PersistableUpliftVanSettings(DataClass):
    SlipPlane: Optional[PersistableTwoCirclesOnTangentLine]


class PersistableSearchArea(DataClass):
    Height: Optional[float]
    TopLeft: Optional[NullablePersistablePoint]
    Width: Optional[float]


class PersistableTangentArea(DataClass):
    Height: Optional[float]
    TopZ: Optional[float]


class PersistableUpliftVanParticleSwarmSettings(DataClass):
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


########
# OUTPUT
########


class PersistableSlice(DataClass):
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


class BishopBruteForceResult(DStabilitySubStructure):
    Circle: Optional[PersistableCircle] = None
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSlice]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/bishopbruteforce"


class PersistableSoilContribution(DataClass):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    SoilId: Optional[str] = None
    Value: Optional[float] = None


class PersistableStageContribution(DataClass):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    StageId: Optional[str] = None
    Value: Optional[float] = None


class PersistableStateLinePointContribution(DataClass):
    Alpha: Optional[float] = None
    Property: Optional[str] = None
    StateLinePointId: Optional[str] = None
    Value: Optional[float] = None


class PersistableStatePointContribution(DataClass):
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
        return "results/bishopreliability"


class BishopResult(DStabilitySubStructure):
    Circle: Optional[PersistableCircle] = None
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSlice]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/bishop"


class PersistableSpencerSlice(BaseModelStructure):
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


class SpencerGeneticAlgorithmResult(DStabilitySubStructure):
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSpencerSlice]]] = None
    SlipPlane: Optional[List[Optional[PersistablePoint]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/spencergeneticalgorithm"


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
        return "results/spencerreliability"


class SpencerResult(DStabilitySubStructure):
    FactorOfSafety: Optional[float] = None
    Id: Optional[str] = None
    Points: Optional[List[Optional[PersistablePoint]]] = None
    Slices: Optional[List[Optional[PersistableSpencerSlice]]] = None
    SlipPlane: Optional[List[Optional[PersistablePoint]]] = None

    @classmethod
    def structure_group(cls) -> str:
        return "results/spencer"


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
        return "results/upliftvanparticleswarm"


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
        return "results/upliftvanreliability"


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
        return "results/upliftvan"


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

    def validator(self):
        return DStabilityValidator(self)
