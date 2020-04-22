import pathlib
from devtools import debug
import pytest

from geolib.models import BaseModel
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import DSettlementStructure, Version, Verticals
from geolib.geometry.one import Point


class TestDSettlementModel:
    @pytest.mark.unittest
    @pytest.mark.workinprogress
    def test_DSettlementModel_instance(self):
        dsettlement_model = DSettlementModel()
        assert dsettlement_model is not None
        assert isinstance(dsettlement_model, BaseModel), (
            "" + "DSheetpilingModel does not instanciate BaseModel"
        )

    @pytest.mark.integrationtest
    def test_parse(self):
        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        ds.datastructure.version = Version(geometry=9999)
        ds.serialize("test.sli")

        p = pathlib.Path("tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        ds.serialize("test2.sli")

    @pytest.mark.integrationtest
    def test_feature_verticals(self):
        p = pathlib.Path(r"../../../tests/test_data/dsettlement/bm1-1.sli")
        ds = DSettlementModel()
        ds.parse(p)
        assert ds.datastructure is not None
        assert isinstance(ds.datastructure, DSettlementStructure)
        # set up the verical locations
        point1 = Point(label='1', x=0., y=1., z=0.)
        point2 = Point(label='2', x=2., y=3., z=0.)
        locations = [point1, point2]
        # call function
        ds.set_verticals(locations=locations)
        ds.serialize("test.sli")
        # check if data were in datastructure
        assert ds.datastructure.verticals.total_mesh == 100
        assert ds.datastructure.verticals.locations[0].X == 0
        assert ds.datastructure.verticals.locations[0].Y == 0
        assert ds.datastructure.verticals.locations[0].Z == 1
        assert ds.datastructure.verticals.locations[1].X == 2
        assert ds.datastructure.verticals.locations[1].Y == 0
        assert ds.datastructure.verticals.locations[1].Z == 3

