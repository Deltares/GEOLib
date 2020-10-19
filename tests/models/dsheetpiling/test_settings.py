import pytest

from geolib.models.dsheetpiling.dsheetpiling_model import (
    DiaphragmModelType,
    SheetModelType,
    SinglePileModelType,
    WoodenSheetPileModelType,
)
from geolib.models.dsheetpiling.internal import Model
from geolib.models.dsheetpiling.settings import (
    LateralEarthPressureMethod,
    LateralEarthPressureMethodStage,
    LoadTypeFavourableUnfavourable,
    LoadTypeFavourableUnfavourableMoment,
)


class TestSettings:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "model,model_value",
        [
            pytest.param(SheetModelType, 0, id="Sheet model"),
            pytest.param(WoodenSheetPileModelType, 0, id="Wooden sheet model"),
            pytest.param(SinglePileModelType, 1, id="Single pile model"),
            pytest.param(DiaphragmModelType, 2, id="Diaphragm model"),
        ],
    )
    def test_set_model(self, model, model_value):
        m = model()
        assert isinstance(m, model)
        kwargs = {k: v for k, v in dict(m, model=m.model).items() if v is not None}
        internal_model = Model(**kwargs)
        assert isinstance(internal_model, Model)

    def test_type_favourable_unfavourable_have_similar_values(self):
        """ This tests checks that these two different Enums have the same value."""
        assert (
            LoadTypeFavourableUnfavourable.FAVOURABLE.value
            == LoadTypeFavourableUnfavourableMoment.FAVOURABLE.value
        )
        assert (
            LoadTypeFavourableUnfavourable.UNFAVOURABLE.value
            == LoadTypeFavourableUnfavourableMoment.UNFAVOURABLE.value
        )

    def test_lateral_earth_pressure_methods_have_similar_names(self):
        """ This tests checks that these two different Enums have the same name."""
        assert (
            LateralEarthPressureMethod.KA_KO_KP.name
            == LateralEarthPressureMethodStage.KA_KO_KP.name
        )
        assert (
            LateralEarthPressureMethod.C_PHI_DELTA.name
            == LateralEarthPressureMethodStage.C_PHI_DELTA.name
        )
