from collections import defaultdict
from datetime import datetime, date
from enum import Enum
from itertools import chain
from math import isfinite
from typing import List, Optional, Set, Dict, Tuple

from geolib import BaseModelStructure
from pydantic import ValidationError, confloat, conlist, root_validator, validator

from geolib import __version__ as version
from geolib.geometry import Point
from geolib.models.dgeoflow.dgeoflow_validator import DGeoflowValidator
from geolib.models.dgeoflow.utils import children
from geolib.soils import Soil, StorageParameters
from geolib.utils import snake_to_camel


class DGeoflowBaseModelStructure(BaseModelStructure):
    def dict(_, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        return {
            k: "NaN" if isinstance(v, float) and not isfinite(v) else v
            for k, v in data.items()
        }


class DGeoflowSubStructure(DGeoflowBaseModelStructure):
    @classmethod
    def structure_name(cls):
        class_name = cls.__name__
        return str.split(str.lower(class_name), ".")[-1]

    @classmethod
    def structure_group(cls):
        return cls.structure_name()


class PersistableStochasticParameter(DGeoflowBaseModelStructure):
    IsProbabilistic: bool = False
    Mean: float = 1.0
    StandardDeviation: float = 0.0


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


class PersistableSoilVisualization(DGeoflowBaseModelStructure):
    Color: Optional[str]
    PersistableShadingType: Optional[PersistableShadingType]
    SoilId: Optional[str]


class SoilVisualisation(DGeoflowBaseModelStructure):
    ContentVersion: Optional[str] = "1"
    SoilVisualizations: Optional[List[Optional[PersistableSoilVisualization]]] = []

    @classmethod
    def structure_name(cls) -> str:
        return "soilvisualizations"


class PersistableSoilLayer(DGeoflowBaseModelStructure):
    LayerId: Optional[str]
    SoilId: Optional[str]


class SoilLayerCollection(DGeoflowSubStructure):
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


class PersistableSoil(DGeoflowBaseModelStructure):
    Code: str = ""
    Id: str = ""
    Name: str = ""
    Notes: str = ""
    HorizontalPermeability: float
    VerticalPermeability: float


class SoilCollection(DGeoflowSubStructure):
    """soils.json"""

    ContentVersion: Optional[str] = "1"
    Soils: List[PersistableSoil] = [
        PersistableSoil(
            Code="H_Aa_ht_new",
            Id="2",
            Name="Embankment new",
        ),
        PersistableSoil(
            Id="3",
            Name="Embankment old",
            Code="H_Aa_ht_old",
        ),
        PersistableSoil(
            Id="4",
            Name="Clay, shallow",
            Code="H_Rk_k_shallow",
        ),
        PersistableSoil(
            Id="5",
            Name="Clay, deep",
            Code="H_Rk_k_deep",
        ),
        PersistableSoil(
            Id="6",
            Name="Organic clay",
            Code="H_Rk_ko",
        ),
        PersistableSoil(
            Id="7",
            Name="Peat, shallow",
            Code="H_vhv_v",
        ),
        PersistableSoil(
            Id="8",
            Name="Peat, deep",
            Code="H_vbv_v",
        ),
        PersistableSoil(
            Id="9",
            Name="Sand",
            Code="Sand",
        ),
        PersistableSoil(
            Id="10",
            Name="Clay with silt",
            Code="P_Rk_k&s",
        ),
        PersistableSoil(
            Id="11",
            Name="Sand with clay",
            Code="H_Ro_z&k",
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
            SoilWeightParameters,
        )

        soil_weight_parameters = SoilWeightParameters()
        soil_weight_parameters.saturated_weight.mean = (
            persistable_soil.VolumetricWeightAbovePhreaticLevel
        )
        soil_weight_parameters.unsaturated_weight.mean = (
            persistable_soil.VolumetricWeightAbovePhreaticLevel
        )

        storage_parameters = StorageParameters(vertical_permeability=persistable_soil.VerticalPermeability,
                                               horizontal_permeability=persistable_soil.HorizontalPermeability)

        return Soil(
            id=persistable_soil.Id,
            name=persistable_soil.Name,
            code=persistable_soil.Code,
            storage_parameters=storage_parameters
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


class ProjectInfo(DGeoflowSubStructure):
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

class PersistablePoint(DGeoflowBaseModelStructure):
    X: Optional[float] = "NaN"
    Z: Optional[float] = "NaN"

class PersistableLayer(DGeoflowBaseModelStructure):
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

class Geometry(DGeoflowSubStructure):
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




class DGeoflowStructure(BaseModelStructure):
    """Highest level DStability class that should be parsed to and serialized from.

    The List[] items (one for each stage in the model) will be stored in a subfolder
    to multiple json files. Where the first (0) instance
    has no suffix, but the second one has (1 => _1) etc.

    also parses the outputs which are part of the json files
    """

    # input part

    soillayers: List[SoilLayerCollection] = [
        SoilLayerCollection(Id="13")
    ]  # soillayers/soillayers_x.json
    soils: SoilCollection = SoilCollection()  # soils.json
    soilvisualizations: SoilVisualisation = SoilVisualisation()  # soilvisualizations.json

    projectinfo: ProjectInfo = ProjectInfo()  # projectinfo.json
    geometries: List[Geometry] = [Geometry(Id="11")]  # geometries/geometry_x.json


    #TODO: SCENARIOS
    #TODO: BOUNDARYCONDITIOMS
    #TODO: LAYERACTIVATIONS
    #TODO: MESHPROPERTIES

    # # Output parts
    # uplift_van_results: List[UpliftVanResult] = []
    # uplift_van_particle_swarm_results: List[UpliftVanParticleSwarmResult] = []
    # uplift_van_reliability_results: List[UpliftVanReliabilityResult] = []
    # spencer_genetic_algorithm_results: List[SpencerGeneticAlgorithmResult] = []
    # spencer_reliability_results: List[SpencerReliabilityResult] = []
    # spencer_results: List[SpencerResult] = []
    # bishop_bruteforce_results: List[BishopBruteForceResult] = []
    # bishop_reliability_results: List[BishopReliabilityResult] = []
    # bishop_results: List[BishopResult] = []

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
            "soillayers",
            "geometries",
        ]

    def get_stage_specific_fields(self, stage=0) -> Tuple[str, DGeoflowSubStructure]:
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

    # def duplicate_stage(
    #         self, current_stage: int, label: str, notes: str, unique_start_id: int
    # ):
    #     """Duplicates an existing stage.
    #     Copies the specific stage fields for a stage and renumbers all Ids,
    #     taking into account foreign keys by using the same renumbering.
    #     """
    #
    #     old_to_new = {}
    #     for fieldname, stagefield in self.get_stage_specific_fields(current_stage):
    #         newstagefield = stagefield.copy(deep=True)
    #
    #         # Renumber the upper class
    #         unique_start_id = self.renumber_fk_fields(
    #             newstagefield, old_to_new, unique_start_id
    #         )
    #         # Renumber all children
    #         for classinstance in children(newstagefield):
    #             unique_start_id = self.renumber_fk_fields(
    #                 classinstance, old_to_new, unique_start_id
    #             )
    #
    #         # Update the stage with extra supplied fields
    #         if fieldname == "stages":
    #             newstagefield.Label = label
    #             newstagefield.Notes = notes
    #
    #         getattr(self, fieldname).append(newstagefield)
    #
    #     return len(self.stages) - 1, unique_start_id
    #
    # def add_default_stage(self, label: str, notes: str, unique_start_id=500) -> int:
    #     """Add a new default (empty) stage to DGeoflow."""
    #     self.soillayers += [SoilLayerCollection(Id=str(unique_start_id + 5))]
    #     self.geometries += [Geometry(Id=str(unique_start_id + 8))]
    #
    #     return len(self.stages) - 1, unique_start_id + 11

    def get_unique_id(self) -> int:
        """Return unique id that can be used in DGeoflow.
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
        return DGeoflowValidator(self)

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


class ForeignKeys(DGeoflowBaseModelStructure):
    """A dataclass that store the connections between the
    various unique Ids used in DStability. These can be seen
    as (implicit) foreign keys.
    """

    mapping: Dict[str, Tuple[str, ...]] = {
        # "Waternet.Id": ("Stage.WaternetId",),
        # "PersistableHeadLine.Id": (
        #     "PersistableReferenceLine.BottomHeadLineId",
        #     "PersistableReferenceLine.TopHeadLineId",
        # ),
        # "PersistableReferenceLine.Id": ("Waternet.PhreaticLineId",),
        # "PersistableLayer.Id": (
        #     "PersistableStatePoint.LayerId",
        #     "PersistableSoilLayer.LayerId",
        #     "PersistableConsolidation.LayerId",
        #     "PersistableLayerLoad.LayerId",
        #     "PersistableBerm.AddedLayerId",
        #     "WaternetCreatorSettings.AquiferInsideAquitardLayerId",
        #     "WaternetCreatorSettings.AquiferLayerId",
        # ),
        # Soil commented out for now, isn't used in stages
        # "PersistableSoil.Id": (
        #     "PersistableSoilVisualization.SoilId",
        #     "PersistableSoilLayer.SoilId",
        #     "PersistableSoilCorrelation.CorrelatedSoilIds",
        #     "PersistableNailPropertiesForSoil.SoilId",
        #     "PersistableSoilContribution.SoilId"
        # ),
        # "CalculationSettings.Id": ("Stage.CalculationSettingsId",),
        # "Decorations.Id": ("Stage.DecorationsId",),
        "Geometry.Id": ("Stage.GeometryId",),
        "Loads.Id": ("Stage.LoadsId",),
        # "Reinforcements.Id": ("Stage.ReinforcementsId",),
        # "Result.Id": ("Stage.ResultId",),
        "SoilLayerCollection.Id": ("Stage.SoilLayersId",),
        # "StateCorrelation.Id": ("Stage.StateCorrelationsId",),
        # "State.Id": ("Stage.StateId",),
        # "WaternetCreatorSettings.Id": ("Stage.WaternetCreatorSettingsId",),
        # "Stage.Id": ("PersistableStageContribution.StageId",),
        # "PersistableStateLinePoint.Id": (
        #     "PersistableStateCorrelation.CorrelatedStateIds",
        #     "PersistableStateLinePointContribution.StateLinePointId",
        # ),
        # "PersistableStatePoint.Id": ("PersistableStatePointContribution.StatePointId",),
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