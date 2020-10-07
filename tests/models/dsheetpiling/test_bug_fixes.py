import geolib as gl
import pytest
from pathlib import Path
from tests.utils import TestUtils


class TestDsheetPilingBugFixes:
    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "file",
        [
            pytest.param("bm4-5a.shd"),
            pytest.param("bm4-17a.shd"),
            pytest.param("bm3-1b.shd"),
            pytest.param("bm3-1d.shd"),
        ],
    )
    def test_geolib_173(self, file: str):
        # In this case the following structure can be seen in the dumpfile.
        #
        model = gl.DSheetPilingModel()
        test_folder = Path(TestUtils.get_local_test_data_dir("dsheetpiling/benchmarks"))
        test_file = test_folder / Path(file)

        model.parse(filename=test_file)
        outputdict = dict(model.output)

        if outputdict["calculation_type"] == "Standard":
            assert len(outputdict["construction_stage"]) == 3
        elif (
            outputdict["calculation_type"]
            == "Verify Sheet Piling according to CUR Method B"
        ):
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_deformation.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_moment_high_angle_of_subgr_reac.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_moment_low_angle_of_subgr_reac.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_high_mod_with_alt_passive_waterlevel.construction_stage
                )
                == 1
            )
            assert (
                len(
                    model.output.verify_sheetpile_data[
                        0
                    ].verify_low_mod_with_alt_passive_waterlevel.construction_stage
                )
                == 1
            )
        elif outputdict["calculation_type"] == "Allowable Anchor Force":
            assert len(outputdict["construction_stage"]) == 1
        elif (
            outputdict["calculation_type"]
            == "Verify Sheet Piling according to CUR Method A"
        ):
            assert len(model.output.verify_deformation.construction_stage) == 1
            assert (
                len(
                    model.output.verify_moment_high_angle_of_subgr_reac.construction_stage
                )
                == 1
            )
            assert (
                len(model.output.verify_moment_low_angle_of_subgr_reac.construction_stage)
                == 1
            )
