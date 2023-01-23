import pytest

from geolib.models.dgeoflow.dgeoflow_model import DGeoFlowModel
from geolib.soils import Soil
from geolib.soils.soil import StorageParameters


class TestDGeoFlowSoil:
    @pytest.mark.unittest
    def test_dgeoflow_add_soil(self):
        dgeoflow_model = DGeoFlowModel(filename=None)
        soil_1 = Soil(name="Test", code="Test")

        dgeoflow_model.add_soil(soil_1)
        assert dgeoflow_model.soils.has_soilcode("Test") is True

        with pytest.raises(ValueError) as _:
            soil_2 = Soil(name="AnotherTest", code="Test")
            dgeoflow_model.add_soil(soil_2)

    def test_dgeoflow_edit_soil_by_code(self):
        dgeoflow_model = DGeoFlowModel(filename=None)
        storage_parameters = StorageParameters(
            horizontal_permeability=10.0, vertical_permeability=20.0
        )
        soil_1 = Soil(name="TestName", code="Test", storage_parameters=storage_parameters)
        id = dgeoflow_model.add_soil(soil_1)

        assert id == "18"
        assert soil_1.storage_parameters.horizontal_permeability.mean == 10.0
        assert soil_1.storage_parameters.vertical_permeability.mean == 20.0

        dgeoflow_model.edit_soil(
            code=soil_1.code, horizontal_permeability=2.0, vertical_permeability=35.0
        )
        assert (
            pytest.approx(
                dgeoflow_model.soils.get_soil(
                    "Test"
                ).storage_parameters.horizontal_permeability
            )
            == 2.0
        )
        assert (
            pytest.approx(
                dgeoflow_model.soils.get_soil(
                    "Test"
                ).storage_parameters.vertical_permeability
            )
            == 35.0
        )

    def test_dgeoflow_edit_soil_by_name(self):
        dgeoflow_model = DGeoFlowModel(filename=None)
        storage_parameters = StorageParameters(
            horizontal_permeability=10.0, vertical_permeability=20.0
        )
        soil_1 = Soil(name="TestName", code="Test", storage_parameters=storage_parameters)
        id = dgeoflow_model.add_soil(soil_1)

        assert id == "18"
        assert soil_1.storage_parameters.horizontal_permeability.mean == 10.0
        assert soil_1.storage_parameters.vertical_permeability.mean == 20.0

        dgeoflow_model.edit_soil_by_name(
            name=soil_1.name, horizontal_permeability=2.0, vertical_permeability=35.0
        )
        assert (
            pytest.approx(
                dgeoflow_model.soils.get_soil(
                    "Test"
                ).storage_parameters.horizontal_permeability
            )
            == 2.0
        )
        assert (
            pytest.approx(
                dgeoflow_model.soils.get_soil(
                    "Test"
                ).storage_parameters.vertical_permeability
            )
            == 35.0
        )

    def test_has_10_default_soils(self):
        dgeoflow_model = DGeoFlowModel(filename=None)
        assert len(dgeoflow_model.soils.Soils) == 12

    def test_has_default_soil_codes(self):
        dgeoflow_model = DGeoFlowModel(filename=None)
        expected_soilcodes = {
            "H_Aa_ht_new",
            "H_Aa_ht_old",
            "H_Rk_k_shallow",
            "H_Rk_k_deep",
            "H_Rk_ko",
            "H_vhv_v",
            "H_vbv_v",
            "P_Rk_k&s",
            "Sand",
            "H_Ro_z&k",
            "Sand, less permeable",
            "Sand, permeable",
        }
        default_soilcodes = {soil.Code for soil in dgeoflow_model.soils.Soils}
        assert expected_soilcodes == default_soilcodes
