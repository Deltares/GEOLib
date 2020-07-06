import logging
from abc import ABCMeta, abstractmethod
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import List, Optional, Type, Union, Any
from pydantic.types import confloat, conint

from pydantic import BaseModel as DataModel
from pydantic import FilePath, PositiveFloat

from geolib.geometry import Point
from geolib.models import BaseModel, BaseModelStructure
from geolib.soils import Soil
from geolib.soils.layers import Profile

from geolib.models.dsheetpiling.constructions import (
    DiaphragmWall,
    Pile,
    Sheet,
)
from .dsheetpiling_parserprovider import DSheetPilingParserProvider
from .loads import (
    Earthquake,
    HorizontalLineLoad,
    Moment,
    NormalForce,
    SoilDisplacement,
    SurchargeLoad,
    UniformLoad,
)
from .internal import CalculationOptions as CalculationOptionsInternal
from .internal import DSheetPilingStructure, DSheetPilingOutputStructure
from .loads import (
    Earthquake,
    HorizontalLineLoad,
    Moment,
    NormalForce,
    SoilDisplacement,
    SurchargeLoad,
    UniformLoad,
)
from .serializer import DSheetPilingInputSerializer
from .surface import Surface
from .supports import Anchor, RigidSupport, SpringSupport, Strut

from .settings import (
    ModelType,
    SinglePileLoadOptions,
    LateralEarthPressureMethod,
    PassiveSide,
    CalculationType,
    DesignType,
    EuroCodePartialFactorSet,
    PartialFactorSetEC7NADNL,
    PartialFactorCalculationType,
    PartialFactorSetEC7NADB,
    DesignPartialFactorSet,
    VerifyType,
    VerifyEurocodePartialFactorSet,
    Side,
)

from .calculation_options import CalculationOptionsPerStage, CalculationOptions
from .water_level import WaterLevel


class BaseModelType(DataModel, metaclass=ABCMeta):
    """Base Class for Model types (Pile, Sheet, Wall)."""

    @property
    @abstractmethod
    def model(self):
        raise NotImplementedError


class SheetModelType(BaseModelType):
    method: Optional[LateralEarthPressureMethod] = None
    check_vertical_balance: Optional[bool] = None
    verification: Optional[bool] = None
    trildens_calculation: Optional[bool] = None
    reliability_analysis: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.SHEET_PILING


class WoodenSheetPileModelType(BaseModelType):
    method: Optional[LateralEarthPressureMethod] = None
    check_vertical_balance: Optional[bool] = None
    verification: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.SHEET_PILING


class SinglePileModelType(BaseModelType):
    pile_load_option: Optional[SinglePileLoadOptions] = None

    @property
    def model(self) -> ModelType:
        return ModelType.SINGLE_PILE


class DiaphragmModelType(BaseModelType):
    method: Optional[LateralEarthPressureMethod] = None
    check_vertical_balance: Optional[bool] = None
    verification: Optional[bool] = None

    @property
    def model(self) -> ModelType:
        return ModelType.DIAPHRAGM_WALL


class DSheetPilingModel(BaseModel):
    """DSheetPiling is a tool used to design sheetpile and diaphragm walls and
    horizontally loaded piles.

    This model can read, modify and create
    *.shi files, read *.shd and *.err files.
    """

    current_stage: Optional[int] = None  # Forces user to always set a stage.
    water_weight: float = 9.81

    datastructure: BaseModelStructure = DSheetPilingStructure()

    @property
    def parser_provider_type(self) -> Type[DSheetPilingParserProvider]:
        return DSheetPilingParserProvider

    @property
    def console_path(self) -> Path:
        return Path("DSheetPilingConsole/DSheetPilingConsole.exe")

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

    def execute(self, timeout: int = 30) -> Union[CompletedProcess, ValueError]:
        """Execute a Model and wait for `timeout` seconds."""
        if self.filename is None:
            raise ValueError("Set filename or serialize first!")
        if not self.filename.exists():
            logging.warning("Serializing before executing.")
            self.serialize(self.filename)
        return run(
            [str(self.meta.console_folder / self.console_path), "/b", str(self.filename)],
            timeout=timeout,
            cwd=self.filename.parent,
        )

    def _is_calculation_per_stage_required(self) -> bool:
        """ Function that checks if [CALCULATION PER STAGE] can be modified. This is true for a verify sheet-piling calculation and method B."""
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
        self.datastructure.input_data.water = f"  {unit_weight}  Unit weight of water"

    def add_stage(
        self,
        name: str,
        copy: bool = False,
        pile_top_displacement: float = 0,
        passive_side: Optional[PassiveSide] = None,
        method_left: Optional[LateralEarthPressureMethod] = None,
        method_right: Optional[LateralEarthPressureMethod] = None,
        set_current: bool = True,
    ) -> int:
        """Add a new stage to the model.

        When using a Single Pile model, the lateral earth pressure method left and right need to be the same.

        Args:
            name: Name of the stage.
            copy: If True, the current stage will be copied.
            pile_top_displacement: Pile top displacement [m]. When not provided, Use top displacement will be set to false.
            passive_side: Option to set the passive side for the stage.
            method_left: LateralEarthPressureMethod for the left side, must be compatible with the Model LateralEarthPressureMethod
            method_right: LateralEarthPressureMethod for the right side, must be compatible with the Model LateralEarthPressureMethod

        Raises:
            ValueError: duplicate stage names, copy=True
            ValidationError: when input arguments are not within constraints

        Returns:
            int: Stage id which can be used to modify the stage.
        """
        if copy:
            raise ValueError("Copying of stages is currently not supported")
        new_stage_id = self.current_stage + 1 if self.current_stage is not None else 0
        self.datastructure.input_data.add_stage(
            name, pile_top_displacement, passive_side, method_left, method_right
        )
        self.current_stage = new_stage_id
        return new_stage_id

    def add_calculation_options_per_stage(
        self, calculation_options_per_stage: CalculationOptionsPerStage
    ):
        if self._is_calculation_per_stage_required():
            if calculation_options_per_stage:
                self.datastructure.input_data.add_calculation_options_per_stage(
                    input_calc_options=calculation_options_per_stage,
                    stage_id=self.current_stage,
                )
            else:
                raise ValueError(
                    f"calculation_options_per_stage is not defined for stage {self.current_stage}."
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

        self.datastructure.input_data.set_model(**dict(model), model=model.model)

    def set_calculation_options(self, calculation_options: CalculationOptions) -> None:
        if not issubclass(type(calculation_options), CalculationOptions):
            raise ValueError(
                f"model should be of subtype CalculationOptions, received {calculation_options}"
            )
        self.datastructure.input_data.set_calculation_options(**dict(calculation_options))

    def add_head_line(
        self,
        left: Optional[WaterLevel] = None,
        right: Optional[WaterLevel] = None,
        stage_id: Optional[int] = None,
    ) -> None:
        """Set water level for a stage.

        If a water level already exists, it is refered to that water level.

        Related to the [WATERLEVELS] block in the .shi file.

        Args:
            left: WaterLevel
            stage_id: ID of the stage. Of no ID is provided, the current stage ID will be taken.

        Raises:
            ValueError: When no stage has yet been added.
        """
        stage_id = self._get_default_stage_none_provided(stage_id)
        if not (left or right):
            raise ValueError("Provide either left or right water level")
        if left:
            self.datastructure.input_data.add_water_level(
                stage_id, left.to_internal(), side=Side.LEFT
            )
        if right:
            self.datastructure.input_data.add_water_level(
                stage_id, right.to_internal(), side=Side.RIGHT
            )

    def add_surface(
        self,
        surface: Surface,
        side: Side,
        stage_id: int,
    ) -> None:
        """Set surface for a stage.

        Surface is added to [SURFACES] if not yet added; reference is done by name.
        A reference to [CONSTRUCTION STAGES]

        Args:
            surface: Surface.
            side: Side which determines on which side the surface is added.
            stage_id: Surface is added to this stage.

        Raises:
            ValueError: When no stage has yet been added.
        """
        self._check_if_stage_id_exists(stage_id)
        self.datastructure.input_data.add_surface(
            stage_id, surface.to_internal(), side=side
        )

    def add_profile(self, left: Profile, right=Profile, stage=None):
        """Add profile on either left/rightside of the model. Requires setup of
        the Profile first.
        .. TODO::     Can we use the add_layer method here as well?
        """

    def add_sheet(
        self, sheet: Union[Sheet, DiaphragmWall], location_top: Optional[Point] = None
    ) -> None:
        """Add sheet/wall to the list of sheet piles."""
        self.datastructure.input_data.add_element_in_sheet_piling(
            sheet=sheet, location_top=location_top
        )

    def add_pile(self, pile: Pile, location_top: Optional[Point] = None) -> None:
        """Add pile to the model.

        Requires setup of the Pile and Locations first.
        """
        self.datastructure.input_data.add_element_in_sheet_piling(
            sheet=pile, location_top=location_top
        )

    def add_non_uniform_load(
        self,
        left: Union[None, SurchargeLoad],
        sheet: Union[
            None, Moment, HorizontalLineLoad, NormalForce, SoilDisplacement, Earthquake
        ],
        right: Union[None, SurchargeLoad],
        location: Point,
        stage=None,
    ):
        """Add all other loads.

        Only SoilDisplacement and Earthquake are valid for a Pile
        construction.
        """

    def add_support(
        self,
        support: Union[Anchor, Strut, SpringSupport, RigidSupport],
        pre_stress: Optional[PositiveFloat] = None,
        stage_id: Optional[int] = None,
    ) -> None:
        """Add support.

        Anchor and Strut supports are only available for the sheetpiling model.

        Args:
            support: A DSheetPiling suppport.
            pre_stress: Prestress for the support which is added to a construction stage.
                        This is a tension stress for the anchor and a compression stress for the strut.
            stage_id: ID of the stage. Of no ID is provided, the current stage ID will be taken.

        """
        stage_id = self._get_default_stage_none_provided(stage_id)

        if isinstance(self.model_type, str):
            raise ValueError("Cannot read model type when it's not yet set; set model.")
        if not isinstance(support, (Anchor, Strut, SpringSupport, RigidSupport)):
            raise ValueError(f"Provide a valid support, received {support}")
        if self.model_type == ModelType.SINGLE_PILE and isinstance(
            support, (Anchor, Strut)
        ):
            raise ValueError(
                f"Only spring and rigid supports can be used for the single pile model; received {support}"
            )

        self.datastructure.input_data.add_support(
            stage_id, support.to_internal(), pre_stress=pre_stress
        )

    def add_soil(self, soil: Soil) -> str:
        """ Soil is converted in the internal structure and added in soil_collection."""
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
