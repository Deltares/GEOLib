import os
from pathlib import Path
from unittest import mock

import pytest
from fastapi.testclient import TestClient
from teamcity import is_running_under_teamcity

from geolib._compat import IS_PYDANTIC_V2
from geolib.models import BaseDataClass, DSettlementModel
from geolib.models.base_model import BaseModel, BaseModelList, MetaData
from geolib.models.dfoundations.dfoundations_model import DFoundationsModel
from geolib.models.dsheetpiling.dsheetpiling_model import DSheetPilingModel
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.internal import Bool
from geolib.service.main import app
from tests.utils import TestUtils, only_teamcity

client = TestClient(app)


class TestBaseModel:
    @pytest.fixture
    def default_base_model(self):
        return BaseModel()

    @pytest.mark.unittest
    def test_meta_init(self):
        # test loading from geolib.env
        m = MetaData()
        assert m.company == "Deltares"

    @pytest.mark.unittest
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_Model_initialize_createsfile_when_no_config_file_given(
        self, default_base_model
    ):
        # 1. Set initial test data.
        config_filename = None

        # 2. Define test action.
        try:
            inputfile_filename = default_base_model.initialize(
                config_file=config_filename
            )
        # 3. Verify final expectations.
        except Exception as e_info:
            pytest.fail("Exception thrown but not expected {}".format(e_info))
        assert inputfile_filename, "No filename was generated"
        assert os.path.exists(
            inputfile_filename
        ), "" + "No file was created at {}".format(inputfile_filename)

    @pytest.mark.unittest
    @pytest.mark.skip(reason="no way of currently testing this")
    def test_Model_execute_timeout_after_giventime(self, default_base_model):
        # 1. Set initial test data.
        timeout = 2
        expected_error = "The execution timed out, a log can be seen in ..."

        # 2. Define test action.
        with pytest.raises(TimeoutError) as e_info:
            default_base_model.execute(timeout)

        # 3. Verify final expectations.
        error_message = str(e_info.value)
        assert error_message == expected_error, (
            ""
            + "Expected exception message {},".format(expected_error)
            + "retrieved {}".format(error_message)
        )

    @pytest.mark.acceptance
    @only_teamcity
    @pytest.mark.parametrize(
        "model,filename,modelname",
        [
            (DSettlementModel, "bm1-1.sli", "dsettlement/benchmarks"),
            (DStabilityModel, "Tutorial_v2023_1.stix", "dstability"),
            (DSheetPilingModel, "bm1-1.shi", "dsheetpiling/benchmarks"),
            (DFoundationsModel, "bm1-1a.foi", "dfoundations/benchmarks"),
        ],
    )
    def test_basemodellist_execute(self, model, filename, modelname):
        # Setup models
        a = model()
        b = model()
        input_folder = Path(TestUtils.get_local_test_data_dir(modelname))
        benchmark_fn = input_folder / filename

        output_folder = Path(TestUtils.get_output_test_data_dir(modelname)) / "multiple"

        ml = BaseModelList(models=[a, b])
        for i, modelinstance in enumerate(ml.models):
            modelinstance.parse(benchmark_fn)
        fn = "test"
        ml.models.append(model(filename=Path(fn)))

        # Execute
        output = ml.execute(output_folder, nprocesses=1)
        assert len(output.models) == 2
        for model in output.models:
            assert model.output

        assert len(output.errors) == 1
        assert fn in output.errors[-1]

    @pytest.mark.unittest
    def test_serialize_modellist(self):
        # 1. Set initial test data.
        a = DSettlementModel(filename="a.txt")
        b = DSettlementModel(filename="b.txt")
        ml = BaseModelList(models=[a, b])

        # 2. Define test action.
        if IS_PYDANTIC_V2:
            _dump = ml.model_dump()
        else:
            _dump = ml.dict()

        # 3. Verify final expectations.
        if IS_PYDANTIC_V2:
            assert _dump.get("models") == [a.model_dump(), b.model_dump()]
        else:
            assert _dump.get("models") == [a.dict(), b.dict()]
        for _model in _dump.get("models"):
            assert _model["datastructure"]

    @pytest.mark.acceptance
    @only_teamcity
    @mock.patch("geolib.models.base_model.requests.post", side_effect=client.post)
    @mock.patch(
        "geolib.models.base_model.requests.compat.urljoin",
        side_effect=lambda *x: "".join(x),  # override urljoin to work without http://x
    )
    @pytest.mark.parametrize(
        "model,filename,modelname",
        [
            (DSettlementModel, "bm1-1.sli", "dsettlement/benchmarks"),
            (DStabilityModel, "Tutorial_v2023_1.stix", "dstability"),
            (DSheetPilingModel, "bm1-1.shi", "dsheetpiling/benchmarks"),
            (DFoundationsModel, "bm1-1a.foi", "dfoundations/benchmarks"),
        ],
    )
    def test_basemodellist_execute_remote(self, _, __, model, filename, modelname):
        # Setup models
        a = model()
        b = model()
        input_folder = Path(TestUtils.get_local_test_data_dir(modelname))
        benchmark_fn = input_folder / filename

        ml = BaseModelList(models=[a, b])
        for i, modelinstance in enumerate(ml.models):
            modelinstance.parse(benchmark_fn)
        fn = "test"
        ml.models.append(model(filename=Path(fn)))

        # Execute and make sure output is available
        output = ml.execute_remote("/")  # no url is needed with the TestClient
        assert len(output.models) == 2
        for model in output.models:
            assert model.output

        assert len(output.errors) == 1
        assert fn in output.errors[-1]

    @pytest.mark.acceptance
    @only_teamcity
    @mock.patch("geolib.models.base_model.requests.post", side_effect=client.post)
    @mock.patch(
        "geolib.models.base_model.requests.compat.urljoin",
        side_effect=lambda *x: "".join(x),  # override urljoin to work without http://x
    )
    @pytest.mark.parametrize(
        "model,filename,modelname",
        [
            (DSettlementModel, "bm1-1.sli", "dsettlement/benchmarks"),
            (DStabilityModel, "Tutorial_v2023_1.stix", "dstability"),
            (DSheetPilingModel, "bm1-1.shi", "dsheetpiling/benchmarks"),
            (DFoundationsModel, "bm1-1a.foi", "dfoundations/benchmarks"),
        ],
    )
    def test_basemodel_execute_remote(self, _, __, model, filename, modelname):
        # Setup models
        modelinstance = model()
        input_folder = Path(TestUtils.get_local_test_data_dir(modelname))
        benchmark_fn = input_folder / filename
        modelinstance.parse(benchmark_fn)

        # Execute and make sure there's output
        model = modelinstance.execute_remote("/")  # no url is needed with the TestClient
        assert model.output


class TestBool:
    @pytest.mark.unittest
    def test_init(self):
        assert Bool(1) == Bool.TRUE
        assert Bool(0) == Bool.FALSE
        assert Bool(True) == Bool.TRUE
        assert Bool(False) == Bool.FALSE
        assert bool(Bool(True)) is True
        assert bool(Bool(False)) is False

    @pytest.mark.unittest
    def test_class(self):
        class A(BaseDataClass):
            a: Bool = True

        assert A().a == Bool.TRUE
        assert A(a="1").a == Bool.TRUE
        assert A(a="0").a == Bool.FALSE
        assert A(a=True).a == Bool.TRUE
        assert A(a=False).a == Bool.FALSE
        assert A(a=Bool.TRUE).a == Bool.TRUE
        assert A(a=Bool.FALSE).a == Bool.FALSE
        assert bool(A(a=Bool.FALSE).a) is False
        assert bool(A(a=Bool.TRUE).a) is True
