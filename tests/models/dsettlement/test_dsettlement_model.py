import pathlib
import pytest

from datetime import timedelta

from geolib.models import BaseModel
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import DSettlementStructure, Version, Verticals
from geolib.geometry.one import Point

from tests.utils import TestUtils
import os


class TestDSettlementModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DSettlementModel_instance(self):
        dsettlement_model = DSettlementModel()
        assert dsettlement_model is not None
        assert isinstance(dsettlement_model, BaseModel), (
            "" + "DSheetpilingModel does not instanciate BaseModel"
        )

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "filename",
        [
            pytest.param('bm1-1.sli', id="Input file")])
    def test_given_filepath_when_parse_then_does_not_raise(self, filename: str):
        # 1. Set up test data
        test_folder = TestUtils.get_local_test_data_dir('dsettlement')
        test_file = pathlib.Path(os.path.join(test_folder, filename))
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert os.path.exists(test_file)

        # 3. Run test.
        ds.parse(test_file)

        # 4. Verify final expectations.
        assert ds.datastructure, 'No data has been generated.'
        assert isinstance(ds.datastructure, DSettlementStructure)

    @pytest.mark.integrationtest
    def test_given_outputfilepath_when_parse_then_raises_notimplemented(self):
        # ToDo: Remove this test case and include it in the one where
        # datastructure is generated once we impelment the output file importer.
        # 1. Set up test data
        test_folder = TestUtils.get_local_test_data_dir('dsettlement')
        test_file = pathlib.Path(os.path.join(test_folder, 'bm1-1.sld'))
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert os.path.exists(test_file)

        # 3. Run test
        with pytest.raises(NotImplementedError):
            ds.parse(test_file)

        # 4. Verify final expectations.
        assert not ds.datastructure, 'Data has been generated but not expected.'

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        "filename",
        [
            pytest.param('bm1-1.sli', id="Input file")])
    def test_given_parsed_input_when_serialize_then_same_content(self, filename: str):
        # 1. Set up test data
        test_folder = TestUtils.get_local_test_data_dir('dsettlement')
        test_file = pathlib.Path(os.path.join(test_folder, filename))
        output_test_folder = TestUtils.get_output_test_data_dir('dsettlement')
        output_test_file = pathlib.Path(os.path.join(output_test_folder, 'generated' + filename))
        ds = DSettlementModel()

        # 2. Verify initial expectations
        assert os.path.exists(test_file)
        if os.path.exists(output_test_file):
            os.remove(output_test_file)

        # 3. Run test.
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4.1. Verify final expectations.
        assert ds.datastructure, 'No data has been generated.'
        assert isinstance(ds.datastructure, DSettlementStructure)
        input_datastructure = dict(ds.datastructure)

        # 4.2. Read the generated data.
        assert os.path.exists(output_test_file)
        output_datastructure = dict(DSettlementModel().parse(output_test_file))
        assert not (input_datastructure is output_datastructure), 'Both references are the same.'

        # 4.3. Compare values
        output_keys = output_datastructure.keys()
        errors = []
        for ds_key, ds_value in input_datastructure.items():
            if not (ds_key in output_keys):
                errors.append(f'Key {ds_key} not serialized!')
                continue
            if not (ds_value == output_datastructure[ds_key]):
                errors.append(
                    f'Values for key {ds_key} differ from parsed to serialized')
        if errors:
            pytest.fail(f'Failed with the following {errors}')
        ds.serialize("test2.sli")

    @pytest.mark.integrationtest
    def test_set_calculation_times(self):

        # parse file
        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)

        # set time steps
        days = [0, 1, 1000]
        time_steps = [timedelta(days=day) for day in days]
        ds.set_calculation_times(time_steps=time_steps)
        ds.serialize("test.sli")

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
        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)

        # set up the verical locations
        point1 = Point(label="1", x=0.0, y=1.0, z=0.0)
        point2 = Point(label="2", x=2.0, y=3.0, z=0.0)
        locations = [point1, point2]
        # call function
        ds.set_verticals(locations=locations)
        ds.serialize("test.sli")
        # check if data were in datastructure
        assert ds.datastructure.verticals.total_mesh == 100
        assert ds.datastructure.verticals.locations[0].X == 0
        assert ds.datastructure.verticals.locations[0].Y == 0
        assert ds.datastructure.verticals.locations[0].Z == 1
        assert ds.datastructure.verticals.locations[1].X == 2
        assert ds.datastructure.verticals.locations[1].Y == 0
        assert ds.datastructure.verticals.locations[1].Z == 3
