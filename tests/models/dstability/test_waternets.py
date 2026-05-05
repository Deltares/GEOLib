import pytest

from geolib.geometry import Point
from geolib.models.dstability.dstability_model import DStabilityModel


class TestDStabilityHeadLine:
    @pytest.mark.unittest
    def test_add_head_line(self):
        dsm = DStabilityModel()
        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]
        headline_id = dsm.add_head_line(
            label="TestHL", points=points, is_phreatic_line=True
        )
        headline = dsm.datastructure.waternets[0].get_head_line(str(headline_id))
        assert isinstance(headline_id, str)
        assert pytest.approx(headline.Points[0].X) == -20.0
        assert dsm.waternets[0].PhreaticLineId == headline.Id


class TestDStabilityReferenceLine:
    @pytest.mark.unittest
    def test_add(self):
        dsm = DStabilityModel()

        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]
        head_line_1_id = dsm.add_head_line(
            label="TestHL_1", points=points, is_phreatic_line=True
        )
        head_line_2_id = dsm.add_head_line(
            label="TestHL_2", points=points, is_phreatic_line=False
        )

        # adding valid reference line
        reference_line_id = dsm.add_reference_line(
            label="TestRL",
            points=points,
            bottom_headline_id=head_line_1_id,
            top_head_line_id=head_line_2_id,
        )
        reference_line = dsm.datastructure.waternets[0].get_reference_line(
            str(reference_line_id)
        )
        assert isinstance(reference_line_id, int)
        assert len(dsm.waternets[0].ReferenceLines) == 1
        assert pytest.approx(reference_line.Points[-1].Z) == -2.0

        # add ref line with invalid headline id
        with pytest.raises(ValueError):
            dsm.add_reference_line(
                label="TestRL",
                points=points,
                bottom_headline_id=-1,
                top_head_line_id=head_line_2_id,
            )

    @pytest.mark.unittest
    def test_add_interpolation(self):
        dsm = DStabilityModel()

        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]
        _ = dsm.add_head_line(label="TestHL_1", points=points, is_phreatic_line=True)
        head_line_2_id = dsm.add_head_line(
            label="TestHL_2", points=points, is_phreatic_line=False
        )

        # adding valid reference line with interpolation
        _ = dsm.add_reference_line(
            label="TestRL",
            points=points,
            top_head_line_id=head_line_2_id,
        )
        assert dsm.waternets[0].ReferenceLines[0].BottomHeadLineId is None
        assert dsm.waternets[0].ReferenceLines[0].TopHeadLineId == head_line_2_id
