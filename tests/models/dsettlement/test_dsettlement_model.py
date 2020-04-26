import logging
import os
import pathlib
from datetime import timedelta
from pathlib import Path
from typing import List

import pydantic
import pytest
from teamcity import is_running_under_teamcity
from tests.utils import TestUtils

import geolib.models.dsettlement.loads as loads
from geolib.geometry.one import Point
from geolib.soils import Soil
from geolib.models import BaseModel
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import (
    Accuracy,
    Boundary,
    Boundaries,
    Curve,
    Curves,
    DSeriePoint,
    DSettlementStructure,
    GeometryData,
    Layer,
    Layers,
    OtherLoad,
    Points,
    TypeOtherLoads,
    Version,
    Verticals,
)


class TestDSettlementModel:
    def setup_dsettlement_model(self):
        """Setup base structure from parsed file while
        we can't initialize one from scratch yet."""
        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
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
        assert isinstance(dsettlement_model, BaseModel), (
            "" + "DSheetpilingModel does not instanciate BaseModel"
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize("filename", [pytest.param("bm1-1.sli", id="Input file")])
    def test_given_filepath_when_parse_then_does_not_raise(self, filename: str):
        # 1. Set up test data
        test_folder = TestUtils.get_local_test_data_dir("dsettlement")
        test_file = pathlib.Path(os.path.join(test_folder, filename))
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert os.path.exists(test_file)

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert ds.datastructure, "No data has been generated."
        assert isinstance(ds.datastructure, DSettlementStructure)

    @pytest.mark.integrationtest
    def test_given_outputfilepath_when_parse_then_raises_notimplemented(self):
        # ToDo: Remove this test case and include it in the one where
        # datastructure is generated once we impelment the output file importer.
        # 1. Set up test data
        test_folder = TestUtils.get_local_test_data_dir("dsettlement")
        test_file = pathlib.Path(os.path.join(test_folder, "bm1-1.sld"))
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert os.path.exists(test_file)

        # 3. Run test
        with pytest.raises(NotImplementedError):
            ds.parse(test_file)

        # 4. Verify final expectations.
        assert not ds.datastructure, "Data has been generated but not expected."

    @pytest.mark.systemtest
    @pytest.mark.parametrize("filename", [pytest.param("bm1-1.sli", id="Input file")])
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: str):
        # 1. Set up test data
        test_folder = TestUtils.get_local_test_data_dir("dsettlement")
        test_file = pathlib.Path(os.path.join(test_folder, filename))
        output_test_folder = TestUtils.get_output_test_data_dir("dsettlement")
        output_test_file = pathlib.Path(
            os.path.join(output_test_folder, "generated" + filename)
        )
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert os.path.exists(test_file)
        if os.path.exists(output_test_file):
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure, "No data has been generated."
        assert isinstance(ds.datastructure, DSettlementStructure)
        input_datastructure = dict(ds.datastructure)

        # 4.2. Read the generated data.
        assert os.path.exists(output_test_file)
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
                logging.warning(f"{ds_value} != {output_datastructure[ds_key]}")
                errors.append(f"Values for key {ds_key} differ from parsed to serialized")
        if errors:
            pytest.fail(f"Failed with the following {errors}")
        ds.serialize("test2.sli")

    @pytest.mark.systemtest
    @pytest.mark.skipif(
        not is_running_under_teamcity(), reason="Console test only installed on TC."
    )
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
        assert os.path.exists(test_output_filepath)

        # 3. Run test.
        dm.input_fn = test_output_filepath
        status = dm.execute()

        # 3. Verify return code of 0 (indicates succesfull run)
        assert status.returncode == 0

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

        # check if value error is raised when a time step lower than 0 is added
        with pytest.raises(
            ValueError, match="ensure this value is greater than or equal to 0"
        ):
            ds.set_calculation_times(time_steps=[timedelta(days=-1)])

        # check if attribute error is raised when a time_step is not a list of timedeltas
        with pytest.raises(AttributeError):
            ds.set_calculation_times(time_steps=[""])

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
        curve1 = Curve(id=1, points=[point1, point2])
        curve2 = Curve(id=2, points=[point1, point2])

        # Test equality
        assert curve1 == curve2

    @pytest.mark.unittest
    def test_boundaries_equals(self):
        # Setup data
        point1 = DSeriePoint(id=4, X=100.0, Y=-1.0, Z=0.0)
        point2 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)
        curve1 = Curve(id=1, points=[point1, point2])
        curve2 = Curve(id=2, points=[point1, point2])
        boundary1 = Boundary(id=1, curves=[curve1, curve2])
        boundary2 = Boundary(id=2, curves=[curve1, curve2])

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
    def test_add_boundary(self):

        point1 = DSeriePoint(id=1, X=0.0, Y=0.0, Z=0.0)
        point2 = DSeriePoint(id=2, X=100.0, Y=0.0, Z=0.0)
        point3 = DSeriePoint(id=3, X=0.0, Y=1.0, Z=0.0)
        point4 = DSeriePoint(id=4, X=100.0, Y=1.0, Z=0.0)

        point5 = DSeriePoint(id=5, X=0.0, Y=-1.0, Z=0.0)
        point6 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)

        ds = DSettlementModel()

        ds.datastructure = DSettlementStructure()

        ds.add_boundary([point1, point2])

        assert ds.boundaries.boundaries[0].curves[0].points[0] == point1
        assert ds.boundaries.boundaries[0].curves[0].points[1] == point2
        assert ds.boundaries.boundaries[0].id == 0

        # add points from right to left and test sorting
        ds.add_boundary([point4, point3])

        assert ds.boundaries.boundaries[1].curves[0].points[0] == point3
        assert ds.boundaries.boundaries[1].curves[0].points[1] == point4
        assert ds.boundaries.boundaries[1].id == 1

        # add boundary below geometry, check if the newly added boundary is the first boundary
        ds.add_boundary([point5, point6])
        ds.boundaries.sort()

        assert ds.boundaries.boundaries[0].curves[0].points[0] == point5
        assert ds.boundaries.boundaries[0].curves[0].points[1] == point6
        assert ds.boundaries.boundaries[0].id == 0

        assert ds.boundaries.boundaries[1].curves[0].points[0] == point1
        assert ds.boundaries.boundaries[1].curves[0].points[1] == point2
        assert ds.boundaries.boundaries[1].id == 1

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
        point1 = DSeriePoint(id=1, X=0.0, Y=0.0, Z=0.0)
        point2 = DSeriePoint(id=2, X=100.0, Y=0.0, Z=0.0)
        point3 = DSeriePoint(id=3, X=0.0, Y=1.0, Z=0.0)
        point4 = DSeriePoint(id=4, X=100.0, Y=1.0, Z=0.0)

        point5 = DSeriePoint(id=5, X=0.0, Y=-1.0, Z=0.0)
        point6 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)

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
        point1 = DSeriePoint(id=1, X=0.0, Y=0.0, Z=0.0)
        point2 = DSeriePoint(id=2, X=100.0, Y=0.0, Z=0.0)
        point3 = DSeriePoint(id=3, X=0.0, Y=1.0, Z=0.0)
        point4 = DSeriePoint(id=4, X=100.0, Y=1.0, Z=0.0)

        point5 = DSeriePoint(id=5, X=0.0, Y=-1.0, Z=0.0)
        point6 = DSeriePoint(id=6, X=100.0, Y=-1.0, Z=0.0)

        # call function
        a = ds.add_boundary([point1, point2])
        b = ds.add_boundary([point4, point3])
        id_a = ds.add_layer(
            material=Soil(name="a"),
            head_line_top=0,
            head_line_bottom=1,
            boundary_top=a,
            boundary_bottom=b,
        )
        id_b = ds.add_layer(
            material=Soil(name="b"),
            head_line_top=0,
            head_line_bottom=1,
            boundary_top=a,
            boundary_bottom=b,
        )
        assert id_a == id_b

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
        ds.datastructure.geometry_data.accuracy = Accuracy()
        ds.datastructure.geometry_data.points = Points()
        ds.datastructure.geometry_data.curves = Curves()
        ds.datastructure.geometry_data.boundaries = Boundaries()
        ds.datastructure.geometry_data.layers = Layers()

        # set up the verical locations
        point1 = DSeriePoint(id=1, X=0.0, Y=0.0, Z=0.0)
        point2 = DSeriePoint(id=2, X=100.0, Y=0.0, Z=0.0)
        point3 = DSeriePoint(id=3, X=0.0, Y=1.0, Z=0.0)
        point4 = DSeriePoint(id=4, X=100.0, Y=1.0, Z=0.0)

        # call function
        a = ds.add_boundary([point1, point2])
        b = ds.add_boundary([point4, point3])
        ds.add_layer(
            material=Soil(name="test"),
            head_line_top=0,
            head_line_bottom=1,
            boundary_top=a,
            boundary_bottom=b,
        )
        ds.serialize(test_output_filepath)

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

    @pytest.mark.integrationtest
    def test_non_uniform_loads_raises_errors(self):
        ds = self.setup_dsettlement_model()
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

        # character length is outside bounds.
        with pytest.raises(pydantic.ValidationError):
            ds.add_non_uniform_load(
                name="My Second Load has a really, really big name",
                points=pointlist,
                time_start=timedelta(days=0),
                time_end=timedelta(days=100),
                gamma_dry=10.001,
                gamma_wet=11.002,
            )

        # Name of load arleady exists.
        with pytest.raises(
            ValueError, match="Load with name 'My First Load' already exists.",
        ):
            ds.add_non_uniform_load(
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
        olr = loads.RectangularLoad(
            weight=10.1, alpha=0.1, Xcp=0.2, Ycp=0.3, Zcp=0.4, xwidth=0.5, zwidth=0.6,
        )
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
