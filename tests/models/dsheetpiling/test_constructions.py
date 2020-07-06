import pytest
from geolib.models.dsheetpiling.constructions import (
    Sheet,
    SheetPileProperties
)
from geolib.models.dsheetpiling.settings import SheetPilingElementMaterialType


class TestInternal:
    @pytest.mark.integrationtest
    def test_sheet_piling_to_internal_sheet_pile(self):
        # Define the external sheet pile class
        external_sheet_pile = Sheet(name="My sheet pile")
        external_sheet_pile.sheet_pile_properties = SheetPileProperties(
            material_type=SheetPilingElementMaterialType.Steel,
            elastic_stiffness_ei=100.05,
        )
        # Run the test
        internal_sheet_pile = external_sheet_pile._to_internal()
        # verify initial expectation
        internal_sheet_pile = dict(internal_sheet_pile)
        assert internal_sheet_pile
        # Test defined values
        assert internal_sheet_pile["name"] == "My sheet pile"
        assert (
            internal_sheet_pile["sheetpilingelementmaterialtype"]
            == SheetPilingElementMaterialType.Steel
        )
        assert internal_sheet_pile["sheetpilingelementei"] == 100.05
        # Test defaults
        assert internal_sheet_pile["sheetpilingelementkmod"] == 0.01
        assert internal_sheet_pile["diaphragmwallposeielastoplastic2"] == 0
        assert internal_sheet_pile["woodensheetpilingelementmaterialfactor"] == 1.3
