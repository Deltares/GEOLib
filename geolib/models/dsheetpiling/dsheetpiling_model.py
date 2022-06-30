from abc import ABCMeta, abstractmethod
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Any, List, Optional, Type, Union

from pydantic import FilePath, PositiveFloat
from pydantic.types import confloat, conint

from geolib.geometry import Point
from geolib.models import BaseDataClass, BaseModel, BaseModelStructure
from geolib.models.dsheetpiling.constructions import DiaphragmWall, Pile, Sheet
from geolib.models.meta import CONSOLE_RUN_BATCH_FLAG
from geolib.soils import Soil

from .calculation_options import CalculationOptions, CalculationOptionsPerStage
from .dsheetpiling_parserprovider import DSheetPilingParserProvider
from .internal import CalculationOptions as CalculationOptionsInternal
from .internal import (
    DSheetPilingDumpStructure,
    DSheetPilingOutputStructure,
    DSheetPilingStructure,
    Water,
)
from .loads import (
    Earthquake,
    HorizontalLineLoad,
    Moment,
    NormalForce,
    SoilDisplacement,
    SurchargeLoad,
    UniformLoad,
)
from .profiles import SoilProfile
from .serializer import DSheetPilingInputSerializer
from .settings import (
    CalculationType,
    CurveSettings,
    DesignType,
    LateralEarthPressureMethod,
    LateralEarthPressureMethodStage,
    ModelType,
    PartialFactorCalculationType,
    PartialFactorSetCUR,
    PartialFactorSetEC,
    PartialFactorSetEC7NADB,
    PartialFactorSetEC7NADNL,
    PartialFactorSetVerifyEC,
    PassiveSide,
    Side,
    SinglePileLoadOptions,
    VerifyType,
)
from .supports import Anchor, RigidSupport, SpringSupport, Strut
from .surface import Surface
from .water_level import WaterLevel


class BaseModelType(BaseDataClass, metaclass=ABCMeta):
    """Base Class for Model types (Pile, Sheet, Wall)."""

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError

    def to_internal(self):
        return dict(self)


class SheetModelType(BaseModelType):
    method: Optional[LateralEarthPressureMethod] = None
    check_vertical_balance: Optional[bool] = None
    verification: Optional[bool] = None
    trildens_calculation: Optional[bool] = None
    reliability_analysis: Optional[bool] = None
    elastic_calculation: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.SHEET_PILING


class WoodenSheetPileModelType(BaseModelType):
    method: Optional[LateralEarthPressureMethod] = None
    check_vertical_balance: Optional[bool] = None
    verification: Optional[bool] = None
    elastic_calculation: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.SHEET_PILING


class SinglePileModelType(BaseModelType):
    pile_load_option: Optional[SinglePileLoadOptions] = None
    elastic_calculation: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.SINGLE_PILE

    def to_internal(self):
        if self.pile_load_option:
            if self.pile_load_option.value == "forces":
                return {"pile_load_option": 0, "pile_load_by_user": 0}
            elif self.pile_load_option.value == "user_defined_displacements":
                return {"pile_load_option": 1, "pile_load_by_user": 0}
            elif self.pile_load_option.value == "calculated_displacements":
                return {"pile_load_option": 1, "pile_load_by_user": 1}
        else:
            return {}


class DiaphragmModelType(BaseModelType):
    method: Optional[LateralEarthPressureMethod] = None
    check_vertical_balance: Optional[bool] = None
    verification: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.DIAPHRAGM_WALL


class DSheetPilingModel(BaseModel):
    r"""DSheetPiling is a tool used to design sheetpile and diaphragm walls and
    horizontally loaded piles.

    This model can read, modify and create \*.shi files, read \*.shd and \*.err files.
    """

    current_stage: Optional[int] = None  # Forces user to always set a stage.
    datastructure: Union[
        DSheetPilingStructure, DSheetPilingDumpStructure
    ] = DSheetPilingStructure()

    @property
    def parser_provider_type(self) -> Type[DSheetPilingParserProvider]:
        return DSheetPilingParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DSheetPilingConsole/DSheetPilingConsole.exe")

    @property
    def console_flags(self) -> List[str]:
        return [CONSOLE_RUN_BATCH_FLAG]

    @property
    def output(self) -> DSheetPilingOutputStructure:
        return self.datastructure.dumpfile.output_data

    @property
    def model_type(self) -> Union[str, ModelType]:
        return self.datastructure.input_data.model.model

    def serialize(self, filename: FilePath):
        ds = self.datastructure.input_data.dict()
        ds.update(
            {
                "version": self.datastructure.version.dict(),
                "version_externals": self.datastructure.version_externals.dict(),
            }
        )
        serializer = DSheetPilingInputSerializer(ds=ds)
        serializer.write(filename)
        self.filename = filename

    def _is_calculation_per_stage_required(self) -> bool:
        """Function that checks if [CALCULATION PER STAGE] can be modified. This is true for a verify sheet-piling calculation and method B."""
        _map_method_b_available = {
            VerifyType.CUR: self.datastructure.input_data.calculation_options.curmethod,
            VerifyType.EC7NL: self.datastructure.input_data.calculation_options.ec7nlmethod,
            VerifyType.EC7BE: self.datastructure.input_data.calculation_options.nbmethod,
        }
        if (
            self.datastructure.input_data.calculation_options.inputcalculationtype
            == CalculationType.VERIFY_SHEETPILING
        ):
            if (
                _map_method_b_available[
                    self.datastructure.input_data.calculation_options.verifytype
                ]
                == PartialFactorCalculationType.METHODA
            ):
                raise ValueError(
                    "MethodA selected for VERIFY_SHEETPILING calculation. Calculation_per_stage options should not be defined or the type of calculation should be switch to MethodB"
                )
        else:
            raise ValueError(
                "Calculation_per_stage should only be defined if VERIFY_SHEETPILING calculation was selected."
            )
        return True

    def set_unit_weight_water(self, unit_weight: float) -> None:
        """Sets the unit weight for water in the [WATER] block"""
        self.datastructure.input_data.water = Water(unit_weight_of_water=unit_weight)

    def add_stage(
        self,
        name: str,
        passive_side: PassiveSide,
        method_left: LateralEarthPressureMethodStage,
        method_right: LateralEarthPressureMethodStage,
        pile_top_displacement: float = 0.0,
    ) -> int:
        """Add a new stage to the model.

        When using a Single Pile model, the lateral earth pressure method left and right need to be the same.
        Their inputs however do not effect the outcome of the calculation.

        Args:
            name: Name of the stage.
            passive_side: Option to set the passive side for the stage.
            method_left: LateralEarthPressureMethodStage applied to left side, must be compatible with the Model LateralEarthPressureMethod
            method_right: LateralEarthPressureMethodStage applied to right side, must be compatible with the Model LateralEarthPressureMethod
            pile_top_displacement: Pile top displacement [m]. When not provided, Use top displacement will be set to false.

        Raises:
            ValidationError: when input arguments are not within constraints

        Returns:
            int: Stage id which can be used to modify the stage.
        """
        new_stage_id = self.current_stage + 1 if self.current_stage is not None else 0
        self.datastructure.input_data.add_stage(
            name, passive_side, method_left, method_right, pile_top_displacement
        )
        self.current_stage = new_stage_id
        return new_stage_id

    def add_calculation_options_per_stage(
        self, calculation_options_per_stage: CalculationOptionsPerStage, stage_id: int
    ) -> None:
        """Set calculation options per stage.

        Calculation options per stage are set in [CALCULATION OPTIONS PER STAGE].

        Args:
            stage_id: Curvesettings are set to this stage. This refers to the Pythonic input and has a starting point of 0.

        Raises:
            ValueError: When non-existing stage_id is passed or when no
                        CalculationOptionsPerStage are required.
        """
        if self._is_calculation_per_stage_required():
            self._check_if_stage_id_exists(stage_id)
            self.datastructure.input_data.add_calculation_options_per_stage(
                input_calc_options=calculation_options_per_stage,
                stage_id=stage_id,
            )
        else:
            raise ValueError(
                f"calculation_options_per_stage is not required for stage {stage_id}."
            )

    def _get_default_stage_none_provided(self, stage_id: Optional[int]) -> int:
        stage_id = stage_id if stage_id is not None else self.current_stage
        if stage_id is None:
            raise ValueError("No stages available yet: add a stage first.")
        self._check_if_stage_id_exists(stage_id)
        return stage_id

    def _check_if_stage_id_exists(self, stage_id: int) -> None:
        if not self.datastructure.input_data.has_stage(stage_id):
            raise ValueError(
                f"Stage {stage_id} is not added to the internal datastructure"
            )

    def set_model(self, model: BaseModelType) -> None:
        """(Re)Set BaseModelType (Pile, Sheet, Wall) for model."""
        if not issubclass(type(model), BaseModelType):
            raise ValueError(
                f"model should be of subtype BaseModelType, received {model}"
            )

        self.datastructure.input_data.set_model(**model.to_internal(), model=model.model)

    def set_calculation_options(self, calculation_options: CalculationOptions) -> None:
        """Set calculation options.

        Calculation options per stage are set in [CALCULATION OPTIONS].

        Args:
            stage_id: Curvesettings are set to this stage.
        """
        if not issubclass(type(calculation_options), CalculationOptions):
            raise ValueError(
                f"model should be of subtype CalculationOptions, received {calculation_options}"
            )
        self.datastructure.input_data.set_calculation_options(**dict(calculation_options))

    def set_curve_settings(
        self,
        curve_settings: CurveSettings,
    ):
        """Set curve settings for soil profiles.

        Curve settings are set in  [SOIL PROFILES].

        Args:
            curve_settings: Curvesettings
        """
        self.datastructure.input_data.set_curve_settings(curve_settings)

    def add_head_line(
        self,
        water_level: WaterLevel,
        side: Side,
        stage_id: int,
    ) -> None:
        """Set water level for a stage.

        If a water level already exists, it is refered to that water level.

        Related to the [WATERLEVELS] block in the .shi file.

        Args:
            water_level: WaterLevel.
            side: Side which determines on which side the surface is added.
            stage_id: WaterLevel is added to this stage.

        Raises:
            ValueError: When non-existing stage_id is passed.
        """
        self._check_if_stage_id_exists(stage_id)
        self.datastructure.input_data.add_water_level(
            stage_id, water_level.to_internal(), side=side
        )

    def add_surface(
        self,
        surface: Surface,
        side: Side,
        stage_id: int,
    ) -> None:
        """Set surface for a stage.

        Surface is added to [SURFACES] if not yet added; reference is done by name.
        A reference in [CONSTRUCTION STAGES] is updated.

        Args:
            surface: Surface.
            side: Side which determines on which side the surface is added.
            stage_id: Surface is added to this stage.

        Raises:
            ValueError: When non-existing stage_id is passed.
        """
        self._check_if_stage_id_exists(stage_id)
        self.datastructure.input_data.add_surface(
            stage_id, surface.to_internal(), side=side
        )

    def add_profile(
        self,
        profile: SoilProfile,
        side: Side,
        stage_id: int,
    ) -> None:
        """Add a Profile on the left or right side of a stage.

        Profile is added to [SOIL PROFILES] if not yet added; reference is done by name.
        A reference in [CONSTRUCTION STAGES] is updated.

        Args:
            profile: Profile.
            side: Side which determines on which side the profile is added.
            stage_id: Surface is added to this stage.

        Raises:
            ValueError: When non-existing stage_id is passed.
        """
        self._check_if_stage_id_exists(stage_id)
        self.datastructure.input_data.add_profile(
            stage_id, profile.to_internal(), side=side
        )

    def set_construction(
        self, top_level: float, elements: List[Union[Sheet, DiaphragmWall, Pile]]
    ) -> None:
        """Sets construction for the DSheetPilingModel.

        Elements are added to [SHEET PILING].
        Removes current sheetpiling when called.

        Args:
            top_level: Top level of the sheet piling.
            elements: List of sheet piling elements, can be Sheet, DiaphragmWall, or Pile.
            Elements are sorted on sheetpilingelementlevel.
        """
        self.datastructure.input_data.set_construction(
            top_level=top_level, elements=[element.to_internal() for element in elements]
        )

    def add_load(
        self,
        load: Union[
            Moment,
            HorizontalLineLoad,
            NormalForce,
            SoilDisplacement,
            Earthquake,
            UniformLoad,
        ],
        stage_id: int,
    ):
        """Adds other loads of type Moment, HorizontalLineLoad, NormalForce, SoilDisplacement or Earthquake

        Args:
            load: Add a load with the types of Moment, HorizontalLineLoad, NormalForce, SoilDisplacement or Earthquake.
            Note that SoilDisplacement and Earthquake are only valid for a Pile construction.
            stage_id: Load is added to this stage.

        Raises:
            ValueError: When non-existing stage_id is passed.
            ValueError: When a verification calculation is selected but duration_type and load_type are not defined for the load.
        """
        self._check_if_stage_id_exists(stage_id)
        self.datastructure.input_data.add_load(load=load.to_internal(), stage_id=stage_id)

    def add_surcharge_load(self, load: SurchargeLoad, side: Side, stage_id: int) -> None:
        """Add surcharge load to a stage.

        Args:
            load: SurchargeLoad.
            side: Side which determines on which side the load is added.
            stage_id: SurchareLoad is added to this stage.

        Raises:
            ValueError: When non-existing stage_id is passed.
        """
        self._check_if_stage_id_exists(stage_id)
        self.datastructure.input_data.add_surcharge_load(
            stage_id, load.to_internal(), side=side
        )

    def add_anchor_or_strut(
        self,
        support: Union[Anchor, Strut],
        stage_id: int,
        pre_stress: PositiveFloat = 0.1,
    ) -> None:
        """Add anchor or strut to a stage.

        Anchor and Strut supports are only available for the sheetpiling model.

        Args:
            support: Anchor and Strut.
            pre_stress: Prestress for the support which is added to a construction stage.
                        This is a tension stress for the anchor and a compression stress for the strut.
            stage_id: Support is added to this stage.
        """
        self._check_if_stage_id_exists(stage_id)

        if isinstance(self.model_type, str):
            raise ValueError("Cannot read model type when it's not yet set; set model.")
        if self.model_type == ModelType.SINGLE_PILE:
            raise ValueError(
                f"Only spring and rigid supports can be used for the single pile model; received {support}"
            )

        if isinstance(support, Anchor):
            self.datastructure.input_data.add_anchor(
                stage_id, support.to_internal(), pre_tension=pre_stress
            )
        elif isinstance(support, Strut):
            self.datastructure.input_data.add_strut(
                stage_id, support.to_internal(), pre_compression=pre_stress
            )
        else:
            raise ValueError(f"support should be Anchor or Strut, received {support}")

    def add_support(
        self,
        support: Union[SpringSupport, RigidSupport],
        stage_id: int,
    ) -> None:
        """Add spring or rigid support to a stage.

        Args:
            support: SpringSupport or RigidSupport.
            stage_id: ID of the stage. Of no ID is provided, the current stage ID will be taken.
        """
        self._check_if_stage_id_exists(stage_id)
        if isinstance(support, SpringSupport):
            self.datastructure.input_data.add_spring_support(
                stage_id,
                support.to_internal(),
            )
        elif isinstance(support, RigidSupport):
            self.datastructure.input_data.add_rigid_support(
                stage_id,
                support.to_internal(),
            )
        else:
            raise ValueError(
                f"support should be SpringSupport or RigidSupport, received {support}"
            )

    def add_soil(self, soil: Soil) -> str:
        """Soil is converted in the internal structure and added in soil_collection."""
        soil_internal = soil._to_dsheetpiling()
        new_soil = self.datastructure.input_data.soil_collection.add_soil_if_unique(
            soil_internal
        )
        return new_soil.name

    @property
    def sheets(self):
        """Enables easy access to the sheets in the internal dict-like
        datastructure.

        Also enables edit/delete for individual Sheets.
        """

    @property
    def profiles(self):
        """Enables easy access to the profiles in the internal dict-like
        datastructure.

        Also enables edit/delete for individual Profiles.
        """
