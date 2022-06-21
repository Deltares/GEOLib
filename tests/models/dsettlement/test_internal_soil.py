from pathlib import Path

import pytest

import geolib.soils as soil_external
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import DSettlementStructure
from geolib.models.dsettlement.internal_soil import PreconType
from geolib.soils import Soil, SoilClassificationParameters, StateType


class TestSoil_Internal:
    @pytest.fixture
    def default_soil(self):
        # 1. Set up test data.
        p = Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        # 2. Verify initial expectations.
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        # 3. Set up second part of test data.
        soil_input = Soil(name="MyNewSoil")
        soil_input.soil_classification_parameters = SoilClassificationParameters()

        soil_input.soil_weight_parameters.saturated_weight = (
            soil_external.StochasticParameter(mean=14)
        )
        soil_input.soil_weight_parameters.unsaturated_weight = (
            soil_external.StochasticParameter(mean=15)
        )
        soil_input.soil_classification_parameters.initial_void_ratio = (
            soil_external.StochasticParameter(mean=0.1)
        )
        soil_input.koppejan_parameters = soil_external.KoppejanParameters(
            precon_koppejan_type=StateType.OCR
        )
        soil_input.soil_state = soil_external.SoilState(
            use_equivalent_age=True, equivalent_age=2
        )
        soil_input.bjerrum_parameters = soil_external.BjerrumParameters(
            input_type_is_comp_ratio=False
        )

        assert soil_input.soil_weight_parameters.saturated_weight.mean == 14
        assert soil_input.soil_weight_parameters.unsaturated_weight.mean == 15
        assert soil_input.soil_classification_parameters.initial_void_ratio.mean == 0.1
        assert soil_input.koppejan_parameters.precon_koppejan_type == StateType.OCR
        assert soil_input.soil_state.use_equivalent_age
        assert soil_input.bjerrum_parameters.input_type_is_comp_ratio == False

        # 4. Verify expectations.
        return soil_input

    @pytest.mark.integrationtest
    def test_when_convert_from_external_to_internal_then_result_expected(
        self, default_soil
    ):
        # 1. Set up test data.
        # 2. Verify initial expectations.
        assert default_soil
        # 3. Run test.
        test_soil = default_soil._to_dsettlement()
        # 4. Verify final expectations.
        assert test_soil.name == "MyNewSoil"
        assert test_soil.soilgamdry == 15
        assert test_soil.soilgamwet == 14
        assert test_soil.soilinitialvoidratio == 0.1
        assert test_soil.soilpreconkoppejantype == PreconType.OCR
        assert test_soil.soiluseequivalentage
        assert test_soil.soilcompratio == False
