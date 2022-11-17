import pytest
from pydantic import ValidationError

from geolib.geometry import Point
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    PersistableHeadLine,
    PersistablePoint,
    PersistableReferenceLine,
    Waternet,
)


class TestDStabilityHeadLine:
    @pytest.mark.unittest
    def test_add_head_line(self):
        dsm = DStabilityModel()
        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]
        head_line_id = dsm.add_head_line(
            label="TestHL", points=points, is_phreatic_line=True
        )
        head_line = dsm.datastructure.waternets[0].get_head_line(str(head_line_id))
        assert isinstance(head_line_id, int)
        assert pytest.approx(head_line.Points[0].X) == -20.0
        assert dsm.waternets[0].PhreaticLineId == head_line.Id

    @pytest.mark.unittest
    def test_edit_head_line(self):
        dsm = DStabilityModel()
        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]
        dsm.add_head_line(
            label="TestHL", points=points, is_phreatic_line=True
        )
        head_line_id_2 = dsm.add_head_line(
            label="TestHL", points=points, is_phreatic_line=True
        )
        head_line_2 = dsm.datastructure.waternets[0].get_head_line(str(head_line_id_2))
        points_2 = [Point(x=-25.0, z=-3.0), Point(x=55.0, z=-3.0)]
        dsm.edit_head_line(head_line_id=head_line_id_2, points=points_2)
        assert pytest.approx(head_line_2.Points[0].Z) == -3.0
        assert dsm.waternets[0].PhreaticLineId == head_line_id_2


class TestDStabilityReferenceLine:
    @pytest.mark.unittest
    def test_add_reference_line(self):
        dsm = DStabilityModel()

        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]

        # add head lines
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
    def test_edit_reference_line(self):
        dsm = DStabilityModel()

        points = [Point(x=-20.0, z=-2.0), Point(x=50.0, z=-2.0)]
        points_v2 = [Point(x=-25.0, z=-3.0), Point(x=55.0, z=-3.0)]

        # add head lines
        head_line_1_id = dsm.add_head_line(
            label="TestHL_1", points=points, is_phreatic_line=True
        )
        head_line_2_id = dsm.add_head_line(
            label="TestHL_2", points=points, is_phreatic_line=False
        )
        head_line_3_id = dsm.add_head_line(
            label="TestHL_2", points=points, is_phreatic_line=False
        )

        # adding valid reference line
        dsm.add_reference_line(
            label="TestRL",
            points=points,
            bottom_headline_id=head_line_1_id,
            top_head_line_id=head_line_2_id,
        )
        reference_line_id_2 = dsm.add_reference_line(
            label="TestRL",
            points=points,
            bottom_headline_id=head_line_1_id,
            top_head_line_id=head_line_2_id,
        )

        # add new points, edit reference line with existing reference line id
        dsm.edit_reference_line(reference_line_id=reference_line_id_2,
                                points=points_v2,
                                bottom_head_line_id=head_line_3_id)
        assert pytest.approx(reference_line_id_2.Points[0].Z) == -3.0
        assert dsm.waternets[0].ReferenceLines[1].BottomHeadLineId == head_line_3_id

        # edit ref line with invalid headline id
        with pytest.raises(ValueError):
            dsm.edit_reference_line(
                reference_line_id=reference_line_id_2,
                label="TestRL",
                points=points,
                bottom_head_line_id=-1,
                top_head_line_id=head_line_2_id,
            )
