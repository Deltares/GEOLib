import pathlib
from devtools import debug
import pytest

from geolib.models import BaseModel
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import DSettlementStructure, Version

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
    def test_parse(self):
        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        ds.datastructure.version = Version(geometry=9999)
        ds.serialize("test.sli")

        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        ds.serialize("test2.sli")

    @pytest.mark.systemtest
    @pytest.mark.parametrize(
        'filename',
        [('bm1-1.sli'), ('bm1-1.sld')])
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

        # 3.1. Generate data
        ds.parse(test_file)
        ds.serialize(output_test_file)

        # 4. Verify final expectations.
        assert os.path.exists(output_test_file)
