import pytest

from geolib.models.dfoundations.internal import (
    Layer,
    Profile,
    Profiles,
)


class TestInternalDFoundations:

    @pytest.mark.integrationtest
    def test_given_single_layer_text_when_parse_then_structure_parsed(self):
        # 1. Define test data.
        layer_name = "Layer (1)"
        material = 9
        top_level = 0.5
        excess_top = 0
        excess_bottom = 0
        ocr = 1
        reduction = 0
        text_to_parse = "" + \
            f"{layer_name}\n" + \
            f"{material} : Material = Material (1)\n" + \
            f"{top_level} : Top level [m]\n" + \
            f"{excess_top} : Excess pore pressure at top [kN/m3]\n" + \
            f"{excess_bottom} : Excess pore pressure at bottom [kN/m3]\n" + \
            f"{ocr} : OCR value [-]\n" + \
            f"{reduction} : Reduction of cone resistance [%]"

        # 2. Run test.
        parsed_layer = Layer.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_layer
        assert parsed_layer.name == "Layer"
        assert parsed_layer.material == material
        assert parsed_layer.top_level == top_level
        assert parsed_layer.excess_pore_pressure_top == excess_top
        assert parsed_layer.excess_pore_pressure_bottom == excess_bottom
        assert parsed_layer.ocr_value == ocr
        assert parsed_layer.reduction_core_resistance == reduction

    @pytest.mark.integrationtest
    def test_given_single_profile_text_when_parse_then_structure_parsed(self):
        # 1. Define test data.
        text_to_parse = "" + \
            "FUGBEN1\n" + \
            "0 : Matching CPT = FUGBEN1\n" + \
            "2.50 : X coordinate [m]\n" + \
            "15.00 : Y coordinate [m]\n" + \
            "-1.00 : Phreatic level [m]\n" + \
            "-24.00 : Pile tip level [m]\n" + \
            "1.00 : Overconsolidation ratio of bearing layer [m]\n" + \
            "-17.00 : Top of positive skin friction zone [m]\n" + \
            "-6.50 : Bottom of negative skin friction zone [m]\n" + \
            "0.00 : Expected ground level settlement [m]\n" + \
            "0.00 : Placement depth of foundation element [m]\n" + \
            "3 : Concentration value according to Frohlich [-]\n" + \
            "0.00 : Top of tension zone [m]\n" + \
            "2 : Reduction type of cone resistance = Manual\n" + \
            "-6.50 : Excavation level [m]\n" + \
            "1 : Excavation width infinite = TRUE\n" + \
            "1 : Excavation length infinite = TRUE\n" + \
            "0.00 : Distance edge pile to excavation boundary [m]\n" + \
            "1 : Number of layers\n" + \
            "Layer (1)\n" + \
            "9 : Material = Material (1)\n" + \
            "0.500 : Top level [m]\n" + \
            "0.00 : Excess pore pressure at top [kN/m3]\n" + \
            "0.00 : Excess pore pressure at bottom [kN/m3]\n" + \
            "1.00 : OCR value [-]\n" + \
            "0 : Reduction of cone resistance [%]"

        # 2. Run test.
        parsed_profile = Profile.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_profile
        assert len(parsed_profile.layers) == 1

    @pytest.mark.integrationtest
    def test_given_single_profile_text_when_parse_profiles_then_structure_parsed(self):
        # 1. Define test data.
        text_to_parse = "" + \
            "1 = number of items\n" + \
            "FUGBEN1\n" + \
            "0 : Matching CPT = FUGBEN1\n" + \
            "2.50 : X coordinate [m]\n" + \
            "15.00 : Y coordinate [m]\n" + \
            "-1.00 : Phreatic level [m]\n" + \
            "-24.00 : Pile tip level [m]\n" + \
            "1.00 : Overconsolidation ratio of bearing layer [m]\n" + \
            "-17.00 : Top of positive skin friction zone [m]\n" + \
            "-6.50 : Bottom of negative skin friction zone [m]\n" + \
            "0.00 : Expected ground level settlement [m]\n" + \
            "0.00 : Placement depth of foundation element [m]\n" + \
            "3 : Concentration value according to Frohlich [-]\n" + \
            "0.00 : Top of tension zone [m]\n" + \
            "2 : Reduction type of cone resistance = Manual\n" + \
            "-6.50 : Excavation level [m]\n" + \
            "1 : Excavation width infinite = TRUE\n" + \
            "1 : Excavation length infinite = TRUE\n" + \
            "0.00 : Distance edge pile to excavation boundary [m]\n" + \
            "1 : Number of layers\n" + \
            "Layer (1)\n" + \
            "9 : Material = Material (1)\n" + \
            "0.500 : Top level [m]\n" + \
            "0.00 : Excess pore pressure at top [kN/m3]\n" + \
            "0.00 : Excess pore pressure at bottom [kN/m3]\n" + \
            "1.00 : OCR value [-]\n" + \
            "0 : Reduction of cone resistance [%]"

        # 2. Run test.
        parsed_profiles = Profiles.parse_text(text_to_parse)

        # 3. Verify final expectations.
        assert parsed_profiles
        assert len(parsed_profiles.profiles) == 1
        profile = parsed_profiles.profiles[0]
        assert len(profile.layers) == 1
