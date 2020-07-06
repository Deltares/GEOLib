import pytest

from geolib.models.dsheetpiling.dsheetpiling_model import (
    SheetModelType,
    WoodenSheetPileModelType,
    SinglePileModelType,
    DiaphragmModelType,
)
from geolib.models.dsheetpiling.internal import Model


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
