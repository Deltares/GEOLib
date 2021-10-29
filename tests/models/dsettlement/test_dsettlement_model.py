import logging
import os
import pathlib
from datetime import timedelta
from pathlib import Path
from typing import List
from warnings import warn

import pydantic
import pytest
from pydantic.color import Color
from teamcity import is_running_under_teamcity

import geolib.models.dsettlement.loads as loads
import geolib.soils as soil_external
from geolib.errors import CalculationError
from geolib.geometry.one import Point
from geolib.models import BaseModel
from geolib.models.dsettlement.drain_types import DrainGridType, DrainSchedule, DrainType
from geolib.models.dsettlement.drains import (
    ScheduleValues,
    ScheduleValuesDetailedInput,
    ScheduleValuesOff,
    ScheduleValuesSimpleInput,
    VerticalDrain,
)
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import (
    Bool,
    Boundaries,
    Boundary,
    ConsolidationModel,
    Curve,
    Curves,
    Dimension,
    DispersionConditionLayerBoundary,
    DSeriePoint,
    DSettlementOutputStructure,
    DSettlementStructure,
    GeometryData,
    InternalProbabilisticCalculationType,
    Layer,
    Layers,
    Model,
    Points,
    PreconPressureWithinLayer,
    SoilModel,
    StrainType,
    StressDistributionLoads,
    StressDistributionSoil,
    Version,
)
from geolib.models.dsettlement.probabilistic_calculation_types import (
    ProbabilisticCalculationType,
)
from geolib.soils import (
    DistributionType,
    IsotacheParameters,
    Soil,
    SoilClassificationParameters,
    SoilWeightParameters,
    StateType,
    StochasticParameter,
)
from tests.utils import TestUtils, only_teamcity


class TestDSettlementModel:
    def setup_dsettlement_model(self):
        """Setup base structure from parsed file while
        we can't initialize one from scratch yet."""
        p = Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        return ds

    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DSettlementModel_instance(self):
        dsettlement_model = DSettlementModel()
        assert dsettlement_model is not None
        assert isinstance(
            dsettlement_model, BaseModel
        ), "DSettlementModel does not instanciate BaseModel"

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "filename", [pytest.param(Path("bm1-1.sli"), id="Input file")]
    )
    def test_given_filepath_when_parse_then_does_not_raise(self, filename: Path):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsettlement"))
        test_file = test_folder / filename
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert test_file.is_file()

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert ds.datastructure.version == Version()
        assert isinstance(ds.datastructure, DSettlementStructure)

    @pytest.mark.integrationtest
    def test_parse_output(self):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsettlement/benchmarks"))
        test_file = test_folder / "bm1-1.sld"
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsettlement"))
        output_test_file = output_test_folder / "results.json"
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert test_file.exists()

        # 3. Run test
        ds.parse(test_file)

        # 4. Verify Depths substructure
        assert ds.output.vertical[0].depths.depths[0] == -0.0000100
        assert ds.output.vertical[0].depths.depths[-1] == -2.0
        assert float(ds.output.vertical[0].depths.depths[-1]) == -2.0
        assert len(ds.output.vertical[0].depths.depths) == 14

        # 5. Verify Stresses substructure
        assert ds.output.vertical[0].stresses.stresses[0]["final_water_stress"] == 0.0
        assert ds.output.vertical[0].stresses.stresses[-1]["initial_total_stress"] == 40.0
        assert (
            type(ds.output.vertical[0].stresses.stresses[-1]["initial_total_stress"])
            == float
        )
        assert len(ds.output.vertical[0].stresses.stresses) == 14

        # 5. Verify residual settlements substructure
        assert (
            ds.output.residual_settlements[0].residualsettlements[0][
                "residual_settlement"
            ]
            == 0.1889574
        )
        assert ds.output.residual_settlements[0].residualsettlements[-1]["vertical"] == 1
        assert (
            type(
                ds.output.residual_settlements[0].residualsettlements[-1][
                    "residual_settlement"
                ]
            )
            == float
        )
        assert len(ds.output.residual_settlements[0].residualsettlements) == 2

        # Serialize to json for acceptance
        with open(output_test_file, "w") as io:
            io.write(ds.output.json(indent=4))

    @pytest.mark.acceptance
    @only_teamcity
    def test_execute_console_successfully(self):
        # 1. Set up test data.
        dm = DSettlementModel()
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "test.sli"
        )

        dm.parse(test_filepath)
        dm.serialize(test_output_filepath)

        # 2. Verify initial expectations.
        assert test_output_filepath.is_file()

        # 3. Run test.
        dm.filename = test_output_filepath
        model = dm.execute()

        # 3. Verify model has been parsed
        assert model

    @pytest.mark.unittest
    def test_execute_console_without_filename_raises_exception(self):
        # 1. Set up test data.
        df = DSettlementModel()

        # 2. Run test
        with pytest.raises(Exception):
            assert df.execute()

    @pytest.mark.integrationtest
    def test_set_calculation_times(self):
        # parse file
        ds = self.setup_dsettlement_model()
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_calc_times.sli"
        )

        # set time steps
        days = [0, 1, 1000]
        time_steps = [timedelta(days=day) for day in days]
        ds.set_calculation_times(time_steps=time_steps)
        ds.serialize(test_output_filepath)

        # assert if time steps are in data structure
        assert ds.datastructure.residual_times.time_steps == days

    @pytest.mark.integrationtest
    def test_get_layer_headlines_util(self):
        # Setup
        ds = self.setup_dsettlement_model()

        # Verify return structure and headline.top, headline.bottom for each layer
        headlines = ds.datastructure.get_headlines_for_layers()
        assert headlines == [[1, 1], [1, 1]]

    @pytest.mark.integrationtest
    def test_add_water_load(self):
        # Setup
        ds = self.setup_dsettlement_model()
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_waterloads.sli"
        )

        # Verify expecatations
        assert isinstance(ds.datastructure.water_loads, str)

        # Add water load
        ds.add_water_load("test", timedelta(days=5), 1)

        # Verify resulting datastructure
        assert not isinstance(ds.datastructure.water_loads, str)
        assert len(ds.datastructure.water_loads.waterloads) == 1
        assert ds.datastructure.water_loads.waterloads[0].name == "test"
        assert ds.datastructure.water_loads.waterloads[0].time == 5
        assert ds.datastructure.water_loads.waterloads[0].phreatic_line == 1
        assert ds.datastructure.water_loads.waterloads[0].headlines == [[1, 1], [1, 1]]

        # For manual verification
        ds.serialize(test_output_filepath)

    @pytest.mark.unittest
    def test_given_timedelta_lesser_than_zero_when_set_calculation_times_raises_valueerror(
        self,
    ):
        # 1. Set up test data.
        test_model = DSettlementModel()
        expected_mssg = "ensure this value is greater than or equal to 0"

        # 2. Run and verify expectations
        with pytest.raises(ValueError, match=expected_mssg):
            test_model.set_calculation_times(time_steps=[timedelta(days=-1)])

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "timesteps",
        [pytest.param("", id="Empty string"), pytest.param([], id="Empty list")],
    )
    def test_given_empty_time_steps_when_set_calculation_times_raises_attributeerror(
        self, timesteps
    ):
        # 1. Set up test model:
        test_model = DSettlementModel()
        # 2. Run test
        with pytest.raises(AttributeError):
            test_model.set_calculation_times(time_steps=[""])

    @pytest.mark.integrationtest
    def test_feature_verticals(self):
        ds = self.setup_dsettlement_model()
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "test_verticals.sli"
        )

        # set up the verical locations
        point1 = Point(label="1", x=0.0, y=1.0, z=0.0)
        point2 = Point(label="2", x=2.0, y=3.0, z=0.0)
        locations = [point1, point2]

        # call function
        ds.set_verticals(locations=locations)
        ds.serialize(test_output_filepath)

        # check if data were in datastructure
        assert ds.datastructure.verticals.total_mesh == 100
        assert ds.datastructure.verticals.locations[0].X == 0
        assert ds.datastructure.verticals.locations[0].Y == 0
        assert ds.datastructure.verticals.locations[0].Z == 1
        assert ds.datastructure.verticals.locations[1].X == 2
        assert ds.datastructure.verticals.locations[1].Y == 0
        assert ds.datastructure.verticals.locations[1].Z == 3

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filename", [pytest.param(Path("bm1-1.sli"), id="Input file")],
    )
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: Path):
        # 1. Set up test data
        test_folder = Path(TestUtils.get_local_test_data_dir("dsettlement"))
        test_file = test_folder / filename
        output_test_folder = Path(TestUtils.get_output_test_data_dir("dsettlement"))
        output_test_file = output_test_folder / filename
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert test_file.is_file()
        if output_test_file.is_file():
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure, "No data has been generated."
        assert isinstance(ds.datastructure, DSettlementStructure)
        input_datastructure = dict(ds.datastructure)

        # 4.2. Read the generated data.
        assert output_test_file.is_file()
        output_datastructure = dict(DSettlementModel().parse(output_test_file))
        assert not (
            input_datastructure is output_datastructure
        ), "Both references are the same."

        # 4.3. Compare values
        output_keys = output_datastructure.keys()
        errors = []
        for ds_key, ds_value in input_datastructure.items():
            if not (ds_key in output_keys):
                errors.append(f"Key {ds_key} not serialized!")
                continue
            if not (ds_value == output_datastructure[ds_key]):
                print(f"{ds_value} != {output_datastructure[ds_key]}")
                errors.append(f"Values for key {ds_key} differ from parsed to serialized")
        if errors:
            pytest.fail(f"Failed with the following {errors}")

    @pytest.mark.unittest
    def test_point_equals(self):
        # Setup data
        point1 = DSeriePoint(id=4, X=100.0, Y=-1.0, Z=0.0)
        point2 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)

        # Test equality
        assert point1 == point2

    @pytest.mark.unittest
    def test_curves_equals(self):
        # Setup data
        point1 = DSeriePoint(id=4, X=100.0, Y=-1.0, Z=0.0)
        point2 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)
        curve1 = Curve(id=1, points=[point1.id, point2.id])
        curve2 = Curve(id=2, points=[point1.id, point2.id])

        # Test equality
        assert curve1 == curve2

    @pytest.mark.unittest
    def test_boundaries_equals(self):
        # Setup data
        point1 = DSeriePoint(id=4, X=100.0, Y=-1.0, Z=0.0)
        point2 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)
        curve1 = Curve(id=1, points=[point1.id, point2.id])
        curve2 = Curve(id=2, points=[point1.id, point2.id])
        boundary1 = Boundary(id=1, curves=[curve1.id, curve2.id])
        boundary2 = Boundary(id=2, curves=[curve1.id, curve2.id])

        # Test equality
        assert boundary1 == boundary2

    @pytest.mark.unittest
    def test_layers_equals(self):
        # Setup data
        layer1 = Layer(
            id=4,
            material="a",
            piezo_top=1,
            piezo_bottom=1,
            boundary_top=1,
            boundary_bottom=2,
        )
        layer2 = Layer(
            id=6,
            material="a",
            piezo_top=1,
            piezo_bottom=1,
            boundary_top=1,
            boundary_bottom=2,
        )

        # Test equality
        assert layer1 == layer2

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "dserie_points, expected_result",
        [
            pytest.param(
                [Point(id=1, x=0.0, y=0.0, z=0.0), Point(id=2, x=100.0, y=0.0, z=0.0),],
                [1, 2],
                id="Default ordered points",
            ),
            pytest.param(
                [Point(id=4, x=100.0, y=0.0, z=1.0), Point(id=3, x=0.0, y=0.0, z=1.0),],
                [2, 1],
                id="Right to left sorted.",
            ),
        ],
    )
    def test_add_simpleboundary(
        self, dserie_points: List[Point], expected_result: List[int]
    ):
        # 1. Set up test model
        model = DSettlementModel()
        model.datastructure = DSettlementStructure()

        # 2. Verify initial expectations.
        assert len(dserie_points) == 2, "Required points not given."
        assert len(expected_result) == 2, "Required expected results not given."
        assert model.boundaries, "Field is none."
        assert not model.boundaries.boundaries, "There should not be any boundaries."

        # 3. Do test
        b_id = model.add_boundary(dserie_points)

        # 4. Verify final expectations.
        assert (
            len(model.boundaries.boundaries) == 1
        ), "There should be 1 boundary created."
        created_boundary = model.boundaries.boundaries[0]
        assert b_id == 0
        assert created_boundary.id == b_id
        assert len(created_boundary.curves) == 1, "There should be 1 curve created."

        curve = model.datastructure.geometry_data.get_curve(created_boundary.curves[0])
        assert curve.points == expected_result

    @pytest.mark.integrationtest
    def test_given_geometry_when_sort_then_boundaries_reordered(self):
        # 1. Set up test data.
        point1 = Point(x=0.0, y=0.0, z=0.0)
        point2 = Point(x=100.0, y=0.0, z=0.0)
        point3 = Point(x=0.0, y=0.0, z=1.0)
        point4 = Point(x=100.0, y=0.0, z=1.0)
        point5 = Point(x=0.0, y=0.0, z=-1.0)
        point6 = Point(x=100.0, y=0.0, z=-1.0)

        ds = DSettlementModel()
        ds.datastructure = DSettlementStructure()
        print(ds.datastructure.geometry_data)
        b_id = ds.add_boundary(
            [point1, point2],
            use_probabilistic_defaults=False,
            stdv=0.05,
            distribution_boundaries=DistributionType.Normal,
        )
        print(ds.datastructure.geometry_data)

        assert b_id == 0
        assert len(ds.boundaries.boundaries) == 1
        assert ds.boundaries.boundaries[0].id == b_id

        assert len(ds.boundaries.boundaries[0].curves) == 1
        assert ds.boundaries.boundaries[0].curves[0] == 1

        assert ds.points.points[0] == DSeriePoint.from_point(point1)
        assert ds.points.points[1] == DSeriePoint.from_point(point2)

        # add points from right to left and test sorting
        b_id = ds.add_boundary(
            [point4, point3],
            use_probabilistic_defaults=False,
            stdv=0.6,
            distribution_boundaries=DistributionType.Normal,
        )

        assert b_id == 1
        assert len(ds.boundaries.boundaries) == 2
        assert ds.boundaries.boundaries[1].id == b_id

        # add boundary below geometry, check if the newly added boundary is the first boundary
        ds.add_boundary([point5, point6])

        # 2. Verify initial expectations
        assert len(ds.boundaries.boundaries) == 3

        # 3. Sort
        ds.datastructure.geometry_data.sort_boundaries()

        # 4. Verify final expectations.
        assert ds.boundaries.boundaries[0].id == 0
        assert ds.boundaries.boundaries[1].id == 1
        assert (
            ds.datastructure.geometry_data.distribution_boundaries.distributionboundaries
            == [
                DistributionType.Undefined,
                DistributionType.Normal,
                DistributionType.Normal,
            ]
        )
        assert ds.datastructure.geometry_data.stdv_boundaries.stdvboundaries == [
            0.0,
            0.05,
            0.6,
        ]

    @pytest.mark.integrationtest
    def test_boundaries_with_error_raised(self):
        # Set up test data.
        point1 = Point(x=0.0, y=0.0, z=0.0)
        point2 = Point(x=100.0, y=0.0, z=0.0)
        point3 = Point(x=0.0, y=0.0, z=1.0)
        point4 = Point(x=100.0, y=0.0, z=1.0)
        point5 = Point(x=0.0, y=0.0, z=-1.0)
        point6 = Point(x=100.0, y=0.0, z=-1.0)
        # Set up model
        ds = DSettlementModel()
        ds.datastructure = DSettlementStructure()
        expected_error = "Enumeration member <DistributionType.LogNormal: 3> is not supported for probabilistic boundary, please select Normal Distribution"
        # Check expectations
        with pytest.raises(ValueError, match=expected_error):
            ds.add_boundary(
                [point1, point2],
                use_probabilistic_defaults=False,
                stdv=0.05,
                distribution_boundaries=DistributionType.LogNormal,
            )

    @pytest.mark.integrationtest
    def test_parse_probabilistic_data(self):
        # todo work in progress
        test_filepath = Path(
            TestUtils.get_local_test_data_dir("dsettlement/benchmarks/bm3-15c.sli")
        )
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_parse_probabilistic_data.sli"
        )
        ds = DSettlementModel()
        ds.parse(test_filepath)
        assert ds.datastructure.probabilistic_data.is_reliability_calculation.value == 1
        assert ds.datastructure.probabilistic_data.maximum_drawings == 1000
        assert ds.datastructure.probabilistic_data.maximum_iterations == 30
        assert ds.datastructure.probabilistic_data.reliability_x_co__ordinate == 0.0
        assert (
            ds.datastructure.probabilistic_data.reliability_type
            == InternalProbabilisticCalculationType.FOSMOrDeterministic
        )

    @pytest.mark.integrationtest
    def test_add_boundary_with_probabilistic_serialize(self):
        # todo work in progress
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_boundaries_with_probabilistic_serialize.sli"
        )
        ds = DSettlementModel()
        ds.parse(test_filepath)

        # initialize geometry
        ds.datastructure.geometry_data = GeometryData()
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)

        # set up the verical locations
        point1 = Point(id=1, x=0.0, y=0.0, z=0.0)
        point2 = Point(id=2, x=100.0, y=0.0, z=0.0)

        # call function
        ds.add_boundary(
            [point1, point2],
            use_probabilistic_defaults=False,
            stdv=0.05,
            distribution_boundaries=DistributionType.Normal,
        )
        ds.serialize(test_output_filepath)
        f = open(test_output_filepath, "r")
        contents = f.read()
        expected_values = (
            "\n[USE PROBABILISTIC DEFAULTS BOUNDARIES]\n  1 - Number of boundaries -\n"
            "  0\n[END OF USE PROBABILISTIC DEFAULTS BOUNDARIES]\n\n[STDV BOUNDARIES]\n  1 - Number of boundaries"
            " -\n   0.05\n[END OF STDV BOUNDARIES]\n\n[DISTRIBUTION BOUNDARIES]\n  1 - Number of boundaries -\n  2\n[END OF DISTRIBUTION BOUNDARIES]"
        )
        assert expected_values in contents

    @pytest.mark.integrationtest
    def test_add_boundary_serialize(self):
        # todo work in progress
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_boundaries.sli"
        )
        ds = DSettlementModel()
        ds.parse(test_filepath)

        # initialize geometry
        ds.datastructure.geometry_data = GeometryData()
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)

        # set up the verical locations
        point1 = Point(id=1, x=0.0, y=0.0, z=0.0)
        point2 = Point(id=2, x=100.0, y=0.0, z=0.0)

        # call function
        ds.add_boundary([point1, point2])
        ds.serialize(test_output_filepath)

    @pytest.mark.integrationtest
    def test_add_layer(self):
        # todo work in progress
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        ds = DSettlementModel()
        ds.parse(test_filepath)

        # initialize geometry
        ds.datastructure.geometry_data = GeometryData()
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)

        # set up the verical locations
        point1 = Point(id=1, x=0.0, y=0.0, z=0.0)
        point2 = Point(id=2, x=100.0, y=0.0, z=0.0)
        point3 = Point(id=3, x=0.0, y=1.0, z=0.0)
        point4 = Point(id=4, x=100.0, y=1.0, z=0.0)

        # call function
        a = ds.add_boundary([point1, point2])
        b = ds.add_boundary([point4, point3])
        id_a = ds.add_layer(
            material_name="a",
            head_line_top=0,
            head_line_bottom=1,
            boundary_top=a,
            boundary_bottom=b,
        )
        id_b = ds.add_layer(
            material_name="b",
            head_line_top=99,
            head_line_bottom=99,
            boundary_top=a,
            boundary_bottom=b,
        )
        assert id_a == id_b

    @pytest.mark.integrationtest
    def test_parse_soil_name_spaces(self):
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        ds = DSettlementModel()
        ds.parse(test_filepath)

        # Assert correct parsing of soil name with spaces
        assert (
            ds.datastructure.soil_collection.soil[0].name
            == ds.datastructure.geometry_data.layers.layers[0].material
        )

    @pytest.mark.systemtest
    def test_add_layer_serialize(self):
        # setup data
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "test_layers.sli"
        )
        ds = DSettlementModel()
        ds.parse(test_filepath)

        # initialize geometry
        ds.datastructure.geometry_data.points = Points()
        ds.datastructure.geometry_data.curves = Curves()
        ds.datastructure.geometry_data.boundaries = Boundaries()
        ds.datastructure.geometry_data.layers = Layers()

        # set up the vertical locations
        point1 = Point(id=1, x=0.0, y=0.0, z=0.0)
        point2 = Point(id=2, x=100.0, y=0.0, z=0.0)
        point3 = Point(id=3, x=0.0, y=0.0, z=1.0)
        point4 = Point(id=4, x=100.0, y=0.0, z=1.0)

        # call function
        a = ds.add_boundary([point1, point2])
        b = ds.add_boundary([point4, point3])
        ds.add_layer(
            material_name="test",
            head_line_top=0,
            head_line_bottom=1,
            boundary_top=a,
            boundary_bottom=b,
        )
        ds.serialize(test_output_filepath)

        assert os.path.exists(test_output_filepath), "No file was generated."

    @pytest.mark.integrationtest
    def test_non_uniform_loads(self):
        ds = self.setup_dsettlement_model()
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "test_loads.sli"
        )

        # set up the point list
        point1 = Point(label="1", x=0.0, y=1.0, z=0.0)
        point2 = Point(label="2", x=2.0, y=3.0, z=0.0)
        pointlist = [point1, point2]

        # Add first uniform load
        ds.add_non_uniform_load(
            name="My First Load",
            points=pointlist,
            time_start=timedelta(days=0),
            time_end=timedelta(days=100),
            gamma_dry=10.001,
            gamma_wet=11.002,
        )

        ds.add_non_uniform_load(
            name="My Second Load",
            points=pointlist,
            time_start=timedelta(days=0),
            time_end=timedelta(days=100),
            gamma_dry=10.001,
            gamma_wet=11.002,
        )

        ds.serialize(test_output_filepath)

        # Verify expectations
        assert len(ds.non_uniform_loads.loads) == 2
        assert list(ds.non_uniform_loads.loads.values())[0].endtime == 100

    @pytest.mark.unittest
    def test_given_long_name_when_add_non_uniform_load_raises_pydantic_error(self):
        # 1. Set up test data.
        test_model = DSettlementModel()
        point1 = Point(label="1", x=0.0, y=1.0, z=0.0)
        point2 = Point(label="2", x=2.0, y=3.0, z=0.0)
        pointlist = [point1, point2]
        long_name = "My Second Load has a really, really big name"

        # 2. Run test and verify expectation.
        # character length is outside bounds.
        with pytest.raises(pydantic.ValidationError):
            test_model.add_non_uniform_load(
                name=long_name,
                points=pointlist,
                time_start=timedelta(days=0),
                time_end=timedelta(days=100),
                gamma_dry=10.001,
                gamma_wet=11.002,
            )

    @pytest.mark.integrationtest
    def test_given_existing_load_when_add_non_uniform_loads_raises_valueerror(self):
        # 1. Set up test data.
        expected_error = "Load with name 'My First Load' already exists."
        test_model = self.setup_dsettlement_model()
        # set up the point list
        point1 = Point(label="1", x=0.0, y=1.0, z=0.0)
        point2 = Point(label="2", x=2.0, y=3.0, z=0.0)
        pointlist = [point1, point2]
        # Add first uniform load
        test_model.add_non_uniform_load(
            name="My First Load",
            points=pointlist,
            time_start=timedelta(days=0),
            time_end=timedelta(days=100),
            gamma_dry=10.001,
            gamma_wet=11.002,
        )

        # 2. Run and verify etest
        with pytest.raises(ValueError, match=expected_error):
            test_model.add_non_uniform_load(
                name="My First Load",
                points=pointlist,
                time_start=timedelta(days=0),
                time_end=timedelta(days=100),
                gamma_dry=10.001,
                gamma_wet=11.002,
            )

    @pytest.mark.integrationtest
    def test_other_loads_trapeziform(self):
        # setup test data
        ds = self.setup_dsettlement_model()
        name = "Load 1"
        time = timedelta(days=1)
        point = Point(x=0.4, z=0.5)
        olt = loads.TrapeziformLoad(gamma=10, height=2, xl=0.1, xm=0.2, xr=0.3,)
        ds.add_other_load(name, time, point, olt)
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_otherloads.sli"
        )

        ds.serialize(test_output_filepath)

        # Verify data
        assert list(ds.other_loads.loads.keys())[0] == "Load 1"
        assert list(ds.other_loads.loads.values())[0].time == 1
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.gamma == 10
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.height == 2
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.xl == 0.1
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.xm == 0.2
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.xr == 0.3
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.Xp == 0.4
        assert list(ds.other_loads.loads.values())[0].load_values_trapeziform.Yp == 0.5

    @pytest.mark.integrationtest
    def test_other_loads_circular(self):
        ds = self.setup_dsettlement_model()
        name = "Load 1"
        time = timedelta(days=1)
        point = Point(x=0.2, z=0.3, y=0.4)
        otc = loads.CircularLoad(weight=10.1, alpha=0.1, R=0.5,)
        ds.add_other_load(name, time, point, otc)
        assert list(ds.other_loads.loads.keys())[0] == "Load 1"
        assert list(ds.other_loads.loads.values())[0].time == 1
        assert list(ds.other_loads.loads.values())[0].load_values_circular.weight == 10.1
        assert list(ds.other_loads.loads.values())[0].load_values_circular.alpha == 0.1
        assert list(ds.other_loads.loads.values())[0].load_values_circular.Xcp == 0.2
        assert list(ds.other_loads.loads.values())[0].load_values_circular.Ycp == 0.3
        assert list(ds.other_loads.loads.values())[0].load_values_circular.Zcp == 0.4
        assert list(ds.other_loads.loads.values())[0].load_values_circular.R == 0.5

    @pytest.mark.integrationtest
    def test_other_loads_rectangular(self):
        ds = self.setup_dsettlement_model()
        name = "Load 1"
        time = timedelta(days=1)
        point = Point(x=0.2, z=0.3, y=0.4)
        olr = loads.RectangularLoad(weight=10.1, alpha=0.1, xwidth=0.5, zwidth=0.6,)
        ds.add_other_load(name, time, point, olr)
        assert list(ds.other_loads.loads.keys())[0] == "Load 1"
        assert list(ds.other_loads.loads.values())[0].time == 1
        assert (
            list(ds.other_loads.loads.values())[0].load_values_rectangular.weight == 10.1
        )
        assert list(ds.other_loads.loads.values())[0].load_values_rectangular.alpha == 0.1
        assert list(ds.other_loads.loads.values())[0].load_values_rectangular.Xcp == 0.2
        assert list(ds.other_loads.loads.values())[0].load_values_rectangular.Ycp == 0.3
        assert list(ds.other_loads.loads.values())[0].load_values_rectangular.Zcp == 0.4
        assert (
            list(ds.other_loads.loads.values())[0].load_values_rectangular.xwidth == 0.5
        )
        assert (
            list(ds.other_loads.loads.values())[0].load_values_rectangular.zwidth == 0.6
        )

    @pytest.mark.integrationtest
    def test_other_loads_tank(self):
        ds = self.setup_dsettlement_model()
        point = Point(x=0.2, z=0.3, y=0.4)
        time = timedelta(days=1)
        name = "Load 1"
        olt = loads.TankLoad(
            wallweight=10.1, internalweight=10.2, alpha=0.1, Rintern=0.5, dWall=0.6,
        )
        ds.add_other_load(name, time, point, olt)
        assert list(ds.other_loads.loads.keys())[0] == "Load 1"
        assert list(ds.other_loads.loads.values())[0].time == 1
        assert list(ds.other_loads.loads.values())[0].load_values_tank.wallweight == 10.1
        assert (
            list(ds.other_loads.loads.values())[0].load_values_tank.internalweight == 10.2
        )
        assert list(ds.other_loads.loads.values())[0].load_values_tank.alpha == 0.1
        assert list(ds.other_loads.loads.values())[0].load_values_tank.Xcp == 0.2
        assert list(ds.other_loads.loads.values())[0].load_values_tank.Ycp == 0.3
        assert list(ds.other_loads.loads.values())[0].load_values_tank.Zcp == 0.4
        assert list(ds.other_loads.loads.values())[0].load_values_tank.Rintern == 0.5
        assert list(ds.other_loads.loads.values())[0].load_values_tank.dWall == 0.6

    @pytest.mark.integrationtest
    def test_other_loads_uniform(self):
        ds = self.setup_dsettlement_model()
        name = "Load 1"
        time = timedelta(days=1)
        p = Point(z=0.2)
        olu = loads.UniformLoad(unit_weight=2, height=0.1, gamma=0.3)
        ds.add_other_load(name, time, p, olu)
        assert list(ds.other_loads.loads.keys())[0] == "Load 1"
        assert list(ds.other_loads.loads.values())[0].time == 1
        assert list(ds.other_loads.loads.values())[0].load_values_uniform.unit_weight == 2
        assert list(ds.other_loads.loads.values())[0].load_values_uniform.height == 0.1
        assert (
            list(ds.other_loads.loads.values())[0].load_values_uniform.y_application
            == 0.2
        )
        assert list(ds.other_loads.loads.values())[0].load_values_uniform.gamma == 0.3

    @pytest.mark.integrationtest
    def test_piezo_lines(self):
        # Setup date
        ds = self.setup_dsettlement_model()
        ds.datastructure.geometry_data = GeometryData()
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "test_piezo.sli"
        )

        point1 = Point(id=1, x=0.0, y=0.0, z=0.0)
        point2 = Point(id=2, x=100.0, y=0.0, z=0.0)
        point3 = Point(id=3, x=0.0, y=0.0, z=1.0)
        point4 = Point(id=4, x=100.0, y=0.0, z=1.0)
        point5 = Point(id=5, x=0.0, y=0.0, z=1.0)
        point6 = Point(id=6, x=100.0, y=0.0, z=1.0)
        list1 = [point1, point2]
        list2 = [point3, point4]
        list3 = [point5, point6]

        # Verify defaults
        assert ds.datastructure.geometry_data.phreatic_line.phreatic_line == 0

        # Verify add_head_line
        h_id = ds.add_head_line(points=list1, is_phreatic=True)
        assert ds.points[
            ds.datastructure.geometry_data.curves[
                ds.headlines.piezolines[0].curves[0]
            ].points[0]
        ] == DSeriePoint.from_point(point1)
        assert ds.datastructure.geometry_data.phreatic_line.phreatic_line == h_id
        assert ds.datastructure.geometry_data.points[
            ds.datastructure.geometry_data.curves[
                ds.datastructure.geometry_data.piezo_lines.piezolines[0].curves[0]
            ].points[1]
        ] == DSeriePoint.from_point(point2)

        # Add another headline, verify phreatic line changed
        h_id2 = ds.add_head_line(points=list2, is_phreatic=True)
        assert h_id2 != h_id
        assert ds.datastructure.geometry_data.phreatic_line.phreatic_line == h_id2

        # Add another headline with duplicate points, should still be added
        h_id3 = ds.add_head_line(points=list3)
        assert h_id3 != h_id2
        assert ds.datastructure.geometry_data.phreatic_line.phreatic_line == h_id2
        assert len(ds.points.points) == 6

        # Serialize resulting structure
        ds.serialize(test_output_filepath)

    @pytest.mark.integrationtest
    def test_add_soil_to_layer(self):
        # step 1: set up test model
        ds = self.setup_dsettlement_model()
        # step 2: set up soil inputs
        soil_input = Soil(name="MyNewSoil")
        soil_input.soil_classification_parameters = SoilClassificationParameters()
        soil_input.soil_weight_parameters = soil_external.SoilWeightParameters()

        soil_input.soil_weight_parameters.saturated_weight = soil_external.StochasticParameter(
            mean=20
        )
        soil_input.soil_weight_parameters.unsaturated_weight = soil_external.StochasticParameter(
            mean=30
        )
        soil_input.soil_classification_parameters.initial_void_ratio = soil_external.StochasticParameter(
            mean=0.1
        )

        soil_input.koppejan_parameters = soil_external.KoppejanParameters(
            precon_koppejan_type=StateType.YIELD_STRESS
        )
        soil_input.soil_state = soil_external.SoilState(
            use_equivalent_age=True, equivalent_age=2
        )
        soil_input.koppejan_parameters.preconsolidation_pressure = soil_external.StochasticParameter(
            mean=10
        )
        # step 3: run test
        ds.add_soil(soil_input)
        # step 4: verify final expectations
        assert ds.input.soil_collection.soil[-1].dict()["name"] == "MyNewSoil"
        assert ds.input.soil_collection.soil[-1].dict()["soilgamdry"] == 30
        assert ds.input.soil_collection.soil[-1].dict()["soilgamwet"] == 20
        assert ds.input.soil_collection.soil[-1].dict()["soilinitialvoidratio"] == 0.1

    @pytest.mark.integrationtest
    def test_add_soil_name_already_defined(self):
        # step 1: set up test model
        ds = self.setup_dsettlement_model()
        expected_error_str = "Soil with name MyNewSoil already exists."
        # step 2: set up soil inputs
        soil_input = Soil(name="MyNewSoil")
        ds.add_soil(soil_input)
        soil_input_second = Soil(name="MyNewSoil")
        # step 3: run test
        with pytest.raises(Exception) as e_info:
            ds.add_soil(soil_input_second)
        # step 4: verify final expectations
        assert not (soil_input_second in ds.input.soil_collection)
        assert str(e_info.value) == expected_error_str

    def test_set_model(self):
        ds = self.setup_dsettlement_model()
        ds.datastructure.model = Model()
        ds.set_model(
            SoilModel.ISOTACHE,
            ConsolidationModel.TERZAGHI,
            True,
            StrainType.LINEAR,
            True,
            True,
            True,
            True,
            True,
            True,
        )

        # Check if all options are in data structure
        assert ds.datastructure.model.soil_model == SoilModel.ISOTACHE
        assert ds.datastructure.model.consolidation_model == ConsolidationModel.TERZAGHI
        assert ds.datastructure.model.dimension == Dimension.TWO_D
        assert ds.datastructure.model.strain_type == StrainType.LINEAR
        assert ds.datastructure.model.is_vertical_drains == Bool.TRUE
        assert ds.datastructure.model.is_probabilistic == Bool.TRUE
        assert ds.datastructure.model.is_horizontal_displacements == Bool.TRUE
        assert ds.datastructure.model.is_secondary_swelling == Bool.TRUE
        assert ds.datastructure.model.is_waspan == Bool.TRUE

    @pytest.mark.systemtest
    def test_serialize_model(self):
        ds = self.setup_dsettlement_model()

        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement")) / "test_model.sli"
        )

        ds.datastructure.model = Model()
        ds.serialize(test_output_filepath)

    @pytest.mark.integrationtest
    def test_set_any_calculation_options_initial_value(self):
        ds = self.setup_dsettlement_model()

        ds.set_any_calculation_options()
        calculation_options = ds.datastructure.calculation_options

        assert (
            calculation_options.precon_pressure_within_layer
            == PreconPressureWithinLayer.CONSTANT_NO_CORRECTION
        )
        assert calculation_options.is_imaginary_surface == Bool.FALSE
        assert calculation_options.imaginary_surface_layer is None
        assert calculation_options.is_submerging == Bool.FALSE
        assert calculation_options.use_end_time_for_fit == Bool.FALSE
        assert calculation_options.is_maintain_profile == Bool.FALSE
        assert calculation_options.maintain_profile_material_name == "Superelevation"
        assert calculation_options.maintain_profile_time == 0
        assert calculation_options.maintain_profile_gamma_dry == 10
        assert calculation_options.maintain_profile_gamma_wet == 10
        assert (
            calculation_options.dispersion_conditions_layer_boundaries_top
            == DispersionConditionLayerBoundary.DRAINED
        )
        assert (
            calculation_options.dispersion_conditions_layer_boundaries_bottom
            == DispersionConditionLayerBoundary.DRAINED
        )
        assert (
            calculation_options.stress_distribution_soil == StressDistributionSoil.BUISMAN
        )
        assert (
            calculation_options.stress_distribution_loads
            == StressDistributionLoads.SIMULATE
        )
        assert calculation_options.iteration_stop_criteria_submerging == 0.0
        assert calculation_options.iteration_stop_criteria_submerging_layer_height == 0
        assert calculation_options.maximum_iteration_steps_for_submerging == 1
        assert calculation_options.iteration_stop_criteria_desired_profile == 0.1
        assert calculation_options.load_column_width_imaginary_surface == 1
        assert calculation_options.load_column_width_non_uniform_loads == 1
        assert calculation_options.load_column_width_trapeziform_loads == 1
        assert calculation_options.end_of_consolidation == 100000
        assert calculation_options.number_of_subtime_steps == 2
        assert calculation_options.reference_time == 1
        assert calculation_options.dissipation == Bool.FALSE
        assert calculation_options.x_coord_dissipation == 0.0
        assert calculation_options.use_fit_factors == Bool.FALSE
        assert calculation_options.x_coord_fit == 0.0
        assert (
            calculation_options.is_predict_settlements_omitting_additional_load_steps
            == Bool.FALSE
        )

    @pytest.mark.integrationtest
    def test_set_any_calculation_options_changed_value(self):
        ds = self.setup_dsettlement_model()

        ds.set_any_calculation_options(
            precon_pressure_within_layer=PreconPressureWithinLayer.CONSTANT_CORRECTION_ALL_T,
            is_imaginary_surface=Bool.TRUE,
            imaginary_surface_layer=1,
            is_submerging=Bool.TRUE,
            use_end_time_for_fit=Bool.TRUE,
            is_maintain_profile=Bool.TRUE,
            maintain_profile_material_name="test",
            maintain_profile_time=1,
            maintain_profile_gamma_dry=20,
            maintain_profile_gamma_wet=20,
            dispersion_conditions_layer_boundaries_top=DispersionConditionLayerBoundary.UNDRAINED,
            dispersion_conditions_layer_boundaries_bottom=DispersionConditionLayerBoundary.UNDRAINED,
            stress_distribution_soil=StressDistributionSoil.BOUSSINESQ,
            stress_distribution_loads=StressDistributionLoads.NONE,
            iteration_stop_criteria_submerging=1.0,
            iteration_stop_criteria_submerging_layer_height=1,
            maximum_iteration_steps_for_submerging=2,
            iteration_stop_criteria_desired_profile=0.2,
            load_column_width_imaginary_surface=2,
            load_column_width_non_uniform_loads=2,
            load_column_width_trapeziform_loads=2,
            end_of_consolidation=1000,
            number_of_subtime_steps=3,
            reference_time=2,
            dissipation=Bool.TRUE,
            x_coord_dissipation=1.0,
            use_fit_factors=Bool.TRUE,
            x_coord_fit=1.0,
            is_predict_settlements_omitting_additional_load_steps=Bool.TRUE,
        )

        calculation_options = ds.datastructure.calculation_options

        assert (
            calculation_options.precon_pressure_within_layer
            == PreconPressureWithinLayer.CONSTANT_CORRECTION_ALL_T
        )
        assert calculation_options.is_imaginary_surface == Bool.TRUE
        assert calculation_options.imaginary_surface_layer == 1
        assert calculation_options.is_submerging == Bool.TRUE
        assert calculation_options.use_end_time_for_fit == Bool.TRUE
        assert calculation_options.is_maintain_profile == Bool.TRUE
        assert calculation_options.maintain_profile_material_name == "test"
        assert calculation_options.maintain_profile_time == 1
        assert calculation_options.maintain_profile_gamma_dry == 20
        assert calculation_options.maintain_profile_gamma_wet == 20
        assert (
            calculation_options.dispersion_conditions_layer_boundaries_top
            == DispersionConditionLayerBoundary.UNDRAINED
        )
        assert (
            calculation_options.dispersion_conditions_layer_boundaries_bottom
            == DispersionConditionLayerBoundary.UNDRAINED
        )
        assert (
            calculation_options.stress_distribution_soil
            == StressDistributionSoil.BOUSSINESQ
        )
        assert (
            calculation_options.stress_distribution_loads == StressDistributionLoads.NONE
        )
        assert calculation_options.iteration_stop_criteria_submerging == 1.0
        assert calculation_options.iteration_stop_criteria_submerging_layer_height == 1
        assert calculation_options.maximum_iteration_steps_for_submerging == 2
        assert calculation_options.iteration_stop_criteria_desired_profile == 0.2
        assert calculation_options.load_column_width_imaginary_surface == 2
        assert calculation_options.load_column_width_non_uniform_loads == 2
        assert calculation_options.load_column_width_trapeziform_loads == 2
        assert calculation_options.end_of_consolidation == 1000
        assert calculation_options.number_of_subtime_steps == 3
        assert calculation_options.reference_time == 2
        assert calculation_options.dissipation == Bool.TRUE
        assert calculation_options.x_coord_dissipation == 1.0
        assert calculation_options.use_fit_factors == Bool.TRUE
        assert calculation_options.x_coord_fit == 1.0
        assert (
            calculation_options.is_predict_settlements_omitting_additional_load_steps
            == Bool.TRUE
        )

    @pytest.mark.integrationtest
    def test_set_any_calculation_options_is_imaginary_surface(self):
        ds = self.setup_dsettlement_model()

        # Check if imaginary surface layer is initialized
        ds.set_any_calculation_options(is_imaginary_surface=True)

        assert ds.datastructure.calculation_options.is_imaginary_surface == Bool.TRUE
        assert ds.datastructure.calculation_options.imaginary_surface_layer == 1

        # Check if imaginary surface layer is not overwritten with default value
        ds.set_any_calculation_options(imaginary_surface_layer=3)

        assert ds.datastructure.calculation_options.imaginary_surface_layer == 3

        # Check if imaginary surface layer is removed
        ds.set_any_calculation_options(is_imaginary_surface=False)

        assert ds.datastructure.calculation_options.is_imaginary_surface == Bool.FALSE
        assert ds.datastructure.calculation_options.imaginary_surface_layer is None

    @pytest.mark.systemtest
    def test_serialize_calculation_options(self):
        ds = self.setup_dsettlement_model()

        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_calculation_options.sli"
        )

        ds.set_any_calculation_options()
        ds.serialize(test_output_filepath)

    @pytest.mark.acceptance
    @only_teamcity
    class TestDSettlementAcceptance:
        def test_dsettlement_acceptance(self):
            """ Acceptance test for D-Settlement serialisation"""
            test_output_filepath = Path(
                TestUtils.get_output_test_data_dir("dsettlement/acceptance")
            )
            dm = DSettlementModel()
            dm.set_model(
                constitutive_model=SoilModel.ISOTACHE,
                consolidation_model=ConsolidationModel.DARCY,
                is_two_dimensional=True,
                strain_type=StrainType.LINEAR,
                is_vertical_drain=True,
                is_fit_for_settlement_plate=False,
                is_probabilistic=False,
                is_horizontal_displacements=False,
                is_secondary_swelling=False,
                is_waspan=True,
            )
            p1 = Point(x=-50, z=0.0)
            p2 = Point(x=-10, z=0.0)
            p3 = Point(x=0, z=2)
            p4 = Point(x=10, z=2)
            p5 = Point(x=30, z=0.0)
            p6 = Point(x=50, z=0.0)
            p7 = Point(x=-50, z=-5)
            p8 = Point(x=50, z=-5)
            p9 = Point(x=-50, z=-10)
            p10 = Point(x=50, z=-10)
            p11 = Point(x=-50, z=-20)
            p12 = Point(x=50, z=-20)

            p15 = Point(x=-50, z=-30)
            p16 = Point(x=-20, z=-30)
            p17 = Point(x=-10, z=-30)
            p18 = Point(x=0, z=-30)
            p19 = Point(x=10, z=-30)
            p20 = Point(x=20, z=-30)
            p21 = Point(x=25, z=-30)
            p22 = Point(x=30, z=-30)
            p23 = Point(x=35, z=-30)
            p24 = Point(x=40, z=-30)
            p25 = Point(x=45, z=-30)
            p26 = Point(x=50, z=-30)

            # headline
            p13 = Point(x=-50, z=-2)
            p14 = Point(x=50, z=-2)

            pl_id = dm.add_head_line([p13, p14], is_phreatic=True)

            dm.set_verticals([p21])

            b6 = dm.add_boundary(
                [p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26]
            )
            b1 = dm.add_boundary([p11, p12])
            b2 = dm.add_boundary([p9, p10])
            b3 = dm.add_boundary([p7, p8])
            b4 = dm.add_boundary([p1, p2, p5, p6])
            b5 = dm.add_boundary([p1, p2, p3, p4, p5, p6])

            soil = Soil(name="Sand")
            soil.soil_weight_parameters.saturated_weight.mean = 17
            soil.soil_weight_parameters.unsaturated_weight.mean = 15
            soil.soil_weight_parameters.saturated_weight.standard_deviation = 0.7
            soil.soil_weight_parameters.unsaturated_weight.standard_deviation = 0.8
            soil.storage_parameters.vertical_consolidation_coefficient.mean = 1.00e-12
            soil.storage_parameters.vertical_consolidation_coefficient.standard_deviation = (
                5.00e-13
            )
            soil.soil_state.pop_layer.mean = 5
            soil.isotache_parameters.precon_isotache_type = StateType.POP
            soil.isotache_parameters.reloading_swelling_constant_a = StochasticParameter(
                mean=1.000e-02, standard_deviation=2.500e-03, correlation_coefficient=0.01
            )
            soil.isotache_parameters.primary_compression_constant_b = StochasticParameter(
                mean=1.000e-01, standard_deviation=2.500e-03
            )
            soil.isotache_parameters.secondary_compression_constant_c = StochasticParameter(
                mean=5.000e-03,
                standard_deviation=1.250e-03,
                correlation_coefficient=0.01,
            )
            s1 = dm.add_soil(soil)

            l1 = dm.add_layer(
                material_name="Sand",
                head_line_top=pl_id,
                head_line_bottom=pl_id,
                boundary_top=b1,
                boundary_bottom=b2,
            )
            l2 = dm.add_layer(
                # material_name="H_Ro_z&k",
                material_name="Sand",
                head_line_top=pl_id,
                head_line_bottom=pl_id,
                boundary_top=b2,
                boundary_bottom=b3,
            )
            l3 = dm.add_layer(
                # material_name="HV",
                material_name="Sand",
                head_line_top=pl_id,
                head_line_bottom=pl_id,
                boundary_top=b3,
                boundary_bottom=b4,
            )
            l4 = dm.add_layer(
                # material_name="H_Aa_ht_old",
                material_name="Sand",
                head_line_top=pl_id,
                head_line_bottom=pl_id,
                boundary_top=b4,
                boundary_bottom=b5,
            )
            l5 = dm.add_layer(
                # material_name="H_Aa_ht_old",
                material_name="Sand",
                head_line_top=pl_id,
                head_line_bottom=pl_id,
                boundary_top=b5,
                boundary_bottom=b6,
            )

            test_drain = VerticalDrain(
                drain_type=DrainType.COLUMN,
                range_from=-15,
                range_to=20,
                bottom_position=-10,
                center_to_center=4,
                diameter=0.1,
                grid=DrainGridType.RECTANGULAR,
                schedule=ScheduleValuesSimpleInput(
                    start_of_drainage=timedelta(days=0.1),
                    phreatic_level_in_drain=2,
                    begin_time=1,
                    end_time=100,
                    underpressure=55,
                    tube_pressure_during_dewatering=10,
                    water_head_during_dewatering=12,
                ),
            )
            # set vertical drains
            dm.set_vertical_drain(test_drain)

            # set up the point list
            point3 = Point(label="1", x=-50, y=0, z=0)
            point4 = Point(label="2", x=-50, y=0, z=2)
            point5 = Point(label="3", x=-10, y=0, z=2)
            point6 = Point(label="4", x=-10, y=0, z=0)
            pointlist = [point3, point4, point5, point6]

            # Add first uniform load
            dm.add_non_uniform_load(
                name="My First Load",
                points=pointlist,
                time_start=timedelta(days=0),
                time_end=timedelta(days=100),
                gamma_dry=20.02,
                gamma_wet=21.02,
            )

            path = test_output_filepath / "test_acceptance.sli"
            dm.serialize(path)

            # Verify output has been parsed
            dm.execute()

    @pytest.mark.integrationtest
    def test_add_vertical_drain_ScheduleValues_Off(self):
        # parse file
        ds = self.setup_dsettlement_model()
        ds.set_model(
            constitutive_model=SoilModel.ISOTACHE,
            consolidation_model=ConsolidationModel.TERZAGHI,
            is_two_dimensional=True,
            strain_type=StrainType.LINEAR,
            is_vertical_drain=True,
            is_fit_for_settlement_plate=True,
            is_probabilistic=True,
            is_horizontal_displacements=True,
            is_secondary_swelling=True,
            is_waspan=True,
        )
        test_schedule = ScheduleValuesOff(
            start_of_drainage=timedelta(days=1), phreatic_level_in_drain=2
        )
        test_drain = VerticalDrain(
            drain_type=DrainType.STRIP,
            range_from=0.1,
            range_to=1.5,
            bottom_position=-10,
            center_to_center=4,
            width=0.1,
            grid=DrainGridType.UNDERDETERMINED,
            schedule=test_schedule,
        )
        # set vertical drains
        ds.set_vertical_drain(test_drain)
        # check final expectations
        assert ds.datastructure.vertical_drain.drain_type == test_drain.drain_type
        assert ds.datastructure.vertical_drain.range_from == test_drain.range_from
        assert ds.datastructure.vertical_drain.range_to == test_drain.range_to
        assert (
            ds.datastructure.vertical_drain.bottom_position == test_drain.bottom_position
        )
        assert (
            ds.datastructure.vertical_drain.center_to_center
            == test_drain.center_to_center
        )
        assert ds.datastructure.vertical_drain.width == test_drain.width
        assert ds.datastructure.vertical_drain.diameter == 0.1
        assert ds.datastructure.vertical_drain.thickness == 0.003
        assert ds.datastructure.vertical_drain.grid == test_drain.grid
        assert (
            ds.datastructure.vertical_drain.start_of_drainage
            == test_drain.schedule.start_of_drainage.days
        )

    @pytest.mark.integrationtest
    def test_add_vertical_drain_ScheduleValues_SIMPLE_INPUT(self):
        # parse file
        ds = self.setup_dsettlement_model()
        ds.set_model(
            SoilModel.ISOTACHE,
            ConsolidationModel.TERZAGHI,
            True,
            StrainType.LINEAR,
            True,
            True,
            True,
            True,
            True,
            True,
        )
        test_drain = VerticalDrain(
            drain_type=DrainType.COLUMN,
            range_from=0.1,
            range_to=1.5,
            bottom_position=-10,
            center_to_center=4,
            diameter=0.1,
            grid=DrainGridType.RECTANGULAR,
            schedule=ScheduleValuesSimpleInput(
                start_of_drainage=timedelta(days=0.1),
                phreatic_level_in_drain=2,
                begin_time=1,
                end_time=100,
                underpressure=55,
                tube_pressure_during_dewatering=10,
                water_head_during_dewatering=12,
            ),
        )
        # set vertical drains
        ds.set_vertical_drain(test_drain)
        # check final expectations
        assert ds.datastructure.vertical_drain.drain_type == test_drain.drain_type
        assert ds.datastructure.vertical_drain.range_from == test_drain.range_from
        assert ds.datastructure.vertical_drain.range_to == test_drain.range_to
        assert (
            ds.datastructure.vertical_drain.bottom_position == test_drain.bottom_position
        )
        assert (
            ds.datastructure.vertical_drain.center_to_center
            == test_drain.center_to_center
        )
        assert ds.datastructure.vertical_drain.diameter == test_drain.diameter
        assert ds.datastructure.vertical_drain.width == 0.1
        assert ds.datastructure.vertical_drain.thickness == 0.003
        assert ds.datastructure.vertical_drain.grid == test_drain.grid
        assert (
            ds.datastructure.vertical_drain.start_of_drainage
            == test_drain.schedule.start_of_drainage.days
        )
        assert (
            ds.datastructure.vertical_drain.begin_time == test_drain.schedule.begin_time
        )
        assert ds.datastructure.vertical_drain.end_time == test_drain.schedule.end_time
        assert (
            ds.datastructure.vertical_drain.under_pressure_for_strips_and_columns
            == test_drain.schedule.underpressure
        )
        assert (
            ds.datastructure.vertical_drain.tube_pressure_during_dewatering
            == test_drain.schedule.tube_pressure_during_dewatering
        )

    @pytest.mark.integrationtest
    def test_add_vertical_drain_ScheduleValues_DETAILED_INPUT(self):
        # parse file
        ds = self.setup_dsettlement_model()
        ds.set_model(
            SoilModel.ISOTACHE,
            ConsolidationModel.TERZAGHI,
            True,
            StrainType.LINEAR,
            True,
            True,
            True,
            True,
            True,
            True,
        )
        time = [
            timedelta(days=0.1),
            timedelta(days=1),
            timedelta(days=4),
            timedelta(days=8),
        ]
        underpressure = [1.2, 1.6, 1, 0.1]
        water_level = [12, 8.5, 7.5, 6]
        test_drain = VerticalDrain(
            drain_type=DrainType.SANDWALL,
            range_from=0.1,
            range_to=1.5,
            bottom_position=-10,
            center_to_center=4,
            width=0.1,
            thickness=0.005,
            grid=DrainGridType.RECTANGULAR,
            schedule=ScheduleValuesDetailedInput(
                time=time, underpressure=underpressure, water_level=water_level
            ),
        )
        # set vertical drains
        ds.set_vertical_drain(test_drain)
        # check final expectations
        assert ds.datastructure.vertical_drain.drain_type == test_drain.drain_type
        assert ds.datastructure.vertical_drain.range_from == test_drain.range_from
        assert ds.datastructure.vertical_drain.range_to == test_drain.range_to
        assert (
            ds.datastructure.vertical_drain.bottom_position == test_drain.bottom_position
        )
        assert (
            ds.datastructure.vertical_drain.center_to_center
            == test_drain.center_to_center
        )
        assert ds.datastructure.vertical_drain.width == test_drain.width
        assert ds.datastructure.vertical_drain.thickness == test_drain.thickness
        assert ds.datastructure.vertical_drain.grid == test_drain.grid
        assert ds.datastructure.vertical_drain.time == [
            onetime.days for onetime in test_drain.schedule.time
        ]
        assert (
            ds.datastructure.vertical_drain.underpressure
            == test_drain.schedule.underpressure
        )
        assert (
            ds.datastructure.vertical_drain.water_level == test_drain.schedule.water_level
        )

    @pytest.mark.integrationtest
    def test_add_vertical_drain_serialize(self):
        # todo work in progress
        test_filepath = Path(TestUtils.get_local_test_data_dir("dsettlement/bm1-1.sli"))
        test_output_filepath = (
            Path(TestUtils.get_output_test_data_dir("dsettlement"))
            / "test_vertical_drain.sli"
        )
        ds = DSettlementModel()
        ds.parse(test_filepath)

        # initialize geometry
        ds.datastructure.geometry_data = GeometryData()
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)

        # Define vertical drain
        time = [
            timedelta(days=0.1),
            timedelta(days=1),
            timedelta(days=4),
            timedelta(days=8),
        ]
        underpressure = [1.2, 1.6, 1, 0.1]
        water_level = [12, 8.5, 7.5, 6]
        test_drain = VerticalDrain(
            drain_type=DrainType.SANDWALL,
            range_from=0.1,
            range_to=1.5,
            bottom_position=-10,
            center_to_center=4,
            width=0.1,
            thickness=0.005,
            grid=DrainGridType.RECTANGULAR,
            schedule=ScheduleValuesDetailedInput(
                time=time, underpressure=underpressure, water_level=water_level
            ),
        )
        # call function
        ds.set_model(
            SoilModel.ISOTACHE,
            ConsolidationModel.TERZAGHI,
            True,
            StrainType.LINEAR,
            True,
            True,
            True,
            True,
            True,
            True,
        )
        ds.set_vertical_drain(test_drain)
        ds.serialize(test_output_filepath)

    @pytest.mark.acceptance
    @only_teamcity
    def test_dsettlement_acceptance_probabilistic(self):
        """Setup base structure from parsed file while
        we can't initialize one from scratch yet."""
        test_output_filepath = Path(
            TestUtils.get_output_test_data_dir("dsettlement/acceptance")
        )
        dm = DSettlementModel()
        dm.set_model(
            constitutive_model=SoilModel.ISOTACHE,
            consolidation_model=ConsolidationModel.DARCY,
            is_two_dimensional=True,
            strain_type=StrainType.LINEAR,
            is_vertical_drain=False,
            is_fit_for_settlement_plate=False,
            is_probabilistic=True,
            is_horizontal_displacements=False,
            is_secondary_swelling=False,
            is_waspan=False,
        )
        p1 = Point(x=-50, z=0.0)
        p2 = Point(x=-10, z=0.0)
        p3 = Point(x=0, z=2)
        p4 = Point(x=10, z=2)
        p5 = Point(x=30, z=0.0)
        p6 = Point(x=50, z=0.0)
        p7 = Point(x=-50, z=-5)
        p8 = Point(x=50, z=-5)
        p9 = Point(x=-50, z=-10)
        p10 = Point(x=50, z=-10)
        p11 = Point(x=-50, z=-20)
        p12 = Point(x=50, z=-20)
        p15 = Point(x=-50, z=-30)
        p16 = Point(x=-20, z=-30)
        p17 = Point(x=-10, z=-30)
        p18 = Point(x=0, z=-30)
        p19 = Point(x=10, z=-30)
        p20 = Point(x=20, z=-30)
        p21 = Point(x=25, z=-30)
        p22 = Point(x=30, z=-30)
        p23 = Point(x=35, z=-30)
        p24 = Point(x=40, z=-30)
        p25 = Point(x=45, z=-30)
        p26 = Point(x=50, z=-30)

        # headline
        p13 = Point(x=-50, z=-2)
        p14 = Point(x=50, z=-2)
        pl_id = dm.add_head_line([p13, p14], is_phreatic=True)
        b6 = dm.add_boundary(
            [p15, p16, p17, p18, p19, p20, p21, p22, p23, p24, p25, p26],
            use_probabilistic_defaults=True,
        )
        b1 = dm.add_boundary([p11, p12], use_probabilistic_defaults=True)
        b2 = dm.add_boundary([p9, p10], use_probabilistic_defaults=True)
        b3 = dm.add_boundary([p7, p8], use_probabilistic_defaults=True)
        b4 = dm.add_boundary(
            [p1, p2, p5, p6],
            use_probabilistic_defaults=False,
            stdv=0.1,
            distribution_boundaries=DistributionType.Normal,
        )
        b5 = dm.add_boundary(
            [p1, p2, p3, p4, p5, p6],
            use_probabilistic_defaults=False,
            stdv=0.1,
            distribution_boundaries=DistributionType.Normal,
        )
        soil = Soil(name="Sand")
        soil.soil_weight_parameters.saturated_weight.mean = 17
        soil.soil_weight_parameters.unsaturated_weight.mean = 15
        soil.soil_weight_parameters.saturated_weight.standard_deviation = 0.7
        soil.soil_weight_parameters.unsaturated_weight.standard_deviation = 0.8
        soil.storage_parameters.vertical_consolidation_coefficient.mean = 1.00e-12
        soil.storage_parameters.vertical_consolidation_coefficient.standard_deviation = (
            5.00e-13
        )
        soil.soil_state.pop_layer.mean = 5
        soil.isotache_parameters.precon_isotache_type = StateType.POP
        soil.isotache_parameters.reloading_swelling_constant_a = StochasticParameter(
            mean=1.000e-02, standard_deviation=2.500e-03, correlation_coefficient=0.01
        )
        soil.isotache_parameters.primary_compression_constant_b = StochasticParameter(
            mean=1.000e-01, standard_deviation=2.500e-03
        )
        soil.isotache_parameters.secondary_compression_constant_c = StochasticParameter(
            mean=5.000e-03, standard_deviation=1.250e-03, correlation_coefficient=0.01
        )
        s1 = dm.add_soil(soil)
        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b1,
            boundary_bottom=b2,
        )
        l2 = dm.add_layer(
            # material_name="H_Ro_z&k",
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b3,
        )
        l3 = dm.add_layer(
            # material_name="HV",
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b4,
        )
        l4 = dm.add_layer(
            # material_name="H_Aa_ht_old",
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b4,
            boundary_bottom=b5,
        )
        l5 = dm.add_layer(
            # material_name="H_Aa_ht_old",
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b6,
        )

        # set up the vertical locations
        point1 = Point(label="1", x=-10.0, y=-50, z=0.0)
        point2 = Point(label="2", x=0.0, y=-50, z=0.0)
        locations = [point1, point2]
        # call function
        dm.set_verticals(locations=locations)

        # For a calculation at least one load should be defined
        # set up the point list
        point3 = Point(label="1", x=-50, y=0, z=0)
        point4 = Point(label="2", x=-50, y=0, z=2)
        point5 = Point(label="3", x=-10, y=0, z=2)
        point6 = Point(label="4", x=-10, y=0, z=0)
        pointlist = [point3, point4, point5, point6]

        # Add first uniform load
        dm.add_non_uniform_load(
            name="My First Load",
            points=pointlist,
            time_start=timedelta(days=0),
            time_end=timedelta(days=100),
            gamma_dry=20.02,
            gamma_wet=21.02,
        )
        dm.set_calculation_times(
            time_steps=[timedelta(days=d) for d in [10, 100, 1000, 2000, 3000, 4000]]
        )

        # calculation setting to probabilistic
        dm.set_probabilistic_data(
            point_of_vertical=Point(x=-10, y=0, z=0),
            residual_settlement=0.01,
            maximum_number_of_samples=10,
            maximum_iterations=15,
            reliability_type=ProbabilisticCalculationType.BandWidthOfSettlementsFOSM,
            is_reliability_calculation=True,
        )
        path = test_output_filepath / "test_acceptance_probabilistic.sli"
        dm.serialize(path)

        # Verify successfull run and parsing of output
        dm.execute()
