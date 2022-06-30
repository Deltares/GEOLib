import logging
from enum import Enum
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import List, Optional, Type, Union

from pydantic import FilePath, confloat

from geolib.geometry import Point
from geolib.models import BaseDataClass, BaseModel, BaseModelStructure
from geolib.models.internal import Bool
from geolib.models.meta import CONSOLE_RUN_BATCH_FLAG
from geolib.soils import Soil

from .dfoundations_parserprovider import DFoundationsParserProvider
from .internal import CalculationOptions as InternalModelOptions
from .internal import CalculationType as InternalCalculationType
from .internal import (
    CPTList,
    DFoundationsDumpfileOutputStructure,
    DFoundationsDumpStructure,
    DFoundationsStructure,
    ModelTypeEnum,
    PositionsBearingPiles,
    PositionsTensionPiles,
    PreliminaryDesign,
    SoilCollection,
)
from .internal import SubCalculationType as CalculationType
from .internal_soil import Soil as InternalSoil
from .piles import (
    BearingPile,
    BearingPileLocation,
    Pile,
    PileLocation,
    TensionPile,
    TensionPileLocation,
)
from .profiles import Profile
from .serializer import DFoundationsInputSerializer

logger = logging.getLogger(__name__)


class ModelOptions(BaseDataClass):
    # Rigidity of superstructure
    is_rigid: Bool = True

    # Transformation
    max_allowed_settlement_lim_state_str: confloat(ge=0, le=100000) = 0
    max_allowed_rel_rotation_lim_state_str: confloat(ge=0.0001, le=10000) = 0.0001
    max_allowed_settlement_lim_state_serv: confloat(ge=0, le=100000) = 0
    max_allowed_rel_rotation_lim_state_serv: confloat(ge=0.0001, le=10000) = 0.0001

    # Factors
    factor_xi3: Optional[confloat(ge=0.01, le=10)] = None
    factor_xi4: Optional[confloat(ge=0.01, le=10)] = None
    ea_gem: Optional[confloat(ge=1)] = None

    # Combined Model Options
    is_suppress_qc_reduction: Bool = False
    is_overrule_excavation: Bool = False
    use_pile_group: Bool = True
    is_write_intermediate_results: Bool = False
    use_interaction_model: Bool = False
    use_almere_rules: Bool = False
    use_extra_almere_rules: Bool = False

    def _to_internal(self):
        return InternalModelOptions(**self.dict())

    @classmethod
    def model_type(cls):
        raise NotImplementedError("Implement in concrete classes.")


class BearingPilesModel(ModelOptions):

    factor_gamma_b: Optional[confloat(ge=1, le=100)] = None
    factor_gamma_s: Optional[confloat(ge=1, le=100)] = None
    factor_gamma_fnk: Optional[confloat(ge=-100, le=100)] = None
    area: Optional[confloat(ge=0, le=100000)] = None

    @classmethod
    def model_type(cls):
        return ModelTypeEnum.BEARING_PILES


class TensionPilesModel(ModelOptions):
    unit_weight_water: confloat(ge=0.01, le=20) = 9.81
    use_compaction: Bool = False
    surcharge: confloat(ge=0, le=1e7) = 0
    use_piezometric_levels: Bool = True

    factor_gamma_var: Optional[confloat(ge=0.01, le=100)] = None
    factor_gamma_st: Optional[confloat(ge=0.01, le=100)] = None
    factor_gamma_gamma: Optional[confloat(ge=0.01, le=100)] = None

    @classmethod
    def model_type(cls):
        return ModelTypeEnum.TENSION_PILES


class CalculationOptions(BaseDataClass):
    """
    Set calculation type:

    # Verification
    VERIFICATION_DESIGN = 0  # Only valid for Bearing Piles
    VERIFICATION_COMPLETE = 1

    # Preliminary Design
    INDICATION_BEARING_CAPACITY = 2
    BEARING_CAPACITY_AT_FIXED_PILETIP_LEVELS = 3
    PILETIP_LEVELS_AND_NET_BEARING_CAPACITY = 4

    Note that cpt_test_level is related to the
    chosen CPTs for the calculation. The GUI will
    override the display of an invalid value.
    """

    calculationtype: CalculationType

    net_bearing_capacity: Optional[float] = 0  # [kN]
    cpt_test_level: Optional[float] = 0.0  # [m]

    trajectory_begin: float = -10.00
    trajectory_end: float = -25.00
    trajectory_interval: float = 0.50

    def _to_internal(self):
        fields = self.dict(exclude={"calculationtype"})
        return PreliminaryDesign(**fields)


class DFoundationsModel(BaseModel):
    r"""D-Foundations enables the user to calculate piles (bearing and tension)
    and shallow foundation in accordance with the Dutch (and Belgian) standards.

    This model can read, modify and create \*.foi files, read \*.fod and \*.err files.
    """

    datastructure: Union[
        DFoundationsDumpStructure,
        DFoundationsStructure,
    ] = DFoundationsStructure()

    @property
    def parser_provider_type(self) -> Type[DFoundationsParserProvider]:
        return DFoundationsParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DFoundationsConsole/DFoundationsConsole.exe")

    @property
    def console_flags(self) -> List[str]:
        return [CONSOLE_RUN_BATCH_FLAG]

    @property
    def output(self) -> DFoundationsDumpfileOutputStructure:
        return self.datastructure.dumpfile.dumpfile_output

    @property
    def input(self):
        return self.datastructure.input_data

    def serialize(self, filename: FilePath):
        serializer = DFoundationsInputSerializer(ds=self.datastructure.dict())
        serializer.write(filename)
        self.filename = filename

    def set_model(
        self,
        model: Union[BearingPilesModel, TensionPilesModel],
        calculation: CalculationOptions,
    ) -> None:
        """(Re)Set ModelType (Bearing/Tension) and ConstructionType for model.

        Please note:

        - All profiles will be automatically selected for calculation
        - Only the relevant pile types will be used (bearing/tension):

            - Only the first one added will be used in the case of verification calculation

        - On model change (bearing to tensions and reverse) the soils will be replaced by defaults

        It is advised to only use this method once at the beginning of your workflow.
        """
        logger.warning(
            "Setting model, "
            "prior made modifications in the current D-Foundations model might be overwritten."
        )
        self.datastructure.input_data.model.model = model.model_type()
        self.datastructure.input_data.calculation_options = model._to_internal()
        self.datastructure.input_data.calculationtype = InternalCalculationType(
            sub_calculationtype=calculation.calculationtype
        )
        self.datastructure.input_data.preliminary_design = calculation._to_internal()
        self.datastructure.input_data.preliminary_design.profiles = list(
            range(len(self.profiles.profiles))
        )
        self.datastructure.input_data.soil_collection.soil = InternalSoil.default_soils(
            model=model.model_type().name
        )

    @property
    def soils(self) -> SoilCollection:
        return self.datastructure.input_data.soil_collection

    def add_soil(self, soil: Soil) -> str:
        """Soil is converted in the internal structure and added in soil_collection."""
        soil_internal = soil._to_dfoundations()
        new_soil = self.datastructure.input_data.soil_collection.add_soil_if_unique(
            soil_internal
        )
        return new_soil.name

    @property
    def cpts(self) -> CPTList:
        return self.datastructure.input_data.cpt_list

    def add_profile(self, profile: Profile) -> str:
        """Add profile on location to the model. Requires setup of the Profile and Location first."""

        # Replace materials' names with ids
        for layer in profile.layers:
            soil_id = self.soils.find_soil_id(layer.get("material", None))
            layer["material"] = soil_id

        cpt = profile.cpt._to_internal()

        cpt_id = self.cpts.add_cpt(cpt)
        internal_profile = profile._to_internal(cpt_id)

        profile = self.profiles.add_profile_if_unique(internal_profile)

        # Automatically select all profiles for calculation
        if isinstance(self.datastructure.input_data.preliminary_design, str):
            logger.warning("Overwriting unparsed calculation settings.")
            self.datastructure.input_data.preliminary_design = PreliminaryDesign()
        self.datastructure.input_data.preliminary_design.profiles = list(
            range(len(self.profiles.profiles))
        )

        return profile.name

    def add_pile_if_unique(self, pile: Pile, location: PileLocation):
        """Add pile on location to the model. Requires setup of the Pile and Location first."""
        if isinstance(pile, BearingPile) and isinstance(location, BearingPileLocation):
            piles = self.bearing_piles
            locations = self.bearing_pile_locations
        elif isinstance(pile, TensionPile) and isinstance(location, TensionPileLocation):
            piles = self.tension_piles
            locations = self.tension_pile_locations
        else:
            logger.warning(
                "Pile and Pile Location are mixed tension an bearing pile/location, "
                "the pile and location is not added."
            )
            return

        i_pile = pile._to_internal()
        if i_pile not in piles:
            piles.append(i_pile)

        pile_id = len(locations) + 1
        if location.pile_name == "":
            location.pile_name = "Pos(" + str(pile_id) + ")"
        i_location = location._to_internal(pile_id)
        if i_location not in locations:
            locations.append(i_location)

        # Enable Pile in calculation
        if isinstance(self.datastructure.input_data.preliminary_design, str):
            logger.warning("Overwriting unparsed calculation settings.")
            self.datastructure.input_data.preliminary_design = PreliminaryDesign()
        self.datastructure.input_data.preliminary_design.pile_types = list(
            range(len(piles))
        )

    @property
    def bearing_piles(self):
        """Enables easy access to the bearing piles in the internal dict-like datastructure.
        Also enables edit/delete for individual Piles."""
        if isinstance(self.datastructure.input_data.types___bearing_piles, str):
            self.datastructure.input_data.types___bearing_piles = []

        return self.datastructure.input_data.types___bearing_piles

    @property
    def tension_piles(self):
        """Enables easy access to the tension piles in the internal dict-like datastructure.
        Also enables edit/delete for individual Piles."""
        if isinstance(self.datastructure.input_data.types___tension_piles_cur, str):
            self.datastructure.input_data.types___tension_piles_cur = []

        return self.datastructure.input_data.types___tension_piles_cur

    @property
    def bearing_pile_locations(self):
        """Enables easy access to the bearing piles location in the internal dict-like datastructure.
        Also enables edit/delete for individual bearing pile locations."""
        if isinstance(self.datastructure.input_data.positions___bearing_piles, str):
            self.datastructure.input_data.positions___bearing_piles = (
                PositionsBearingPiles()
            )
        return self.datastructure.input_data.positions___bearing_piles.positions

    @property
    def tension_pile_locations(self):
        """Enables easy access to the tension piles location in the internal dict-like datastructure.
        Also enables edit/delete for individual tension pile locations."""
        if isinstance(self.datastructure.input_data.positions___tension_piles_cur, str):
            self.datastructure.input_data.positions___tension_piles_cur = (
                PositionsTensionPiles()
            )
        return self.datastructure.input_data.positions___tension_piles_cur.positions

    @property
    def profiles(self):
        """Enables easy access to the profiles in the internal dict-like datastructure. Also enables edit/delete for individual Piles."""
        return self.datastructure.input_data.profiles
