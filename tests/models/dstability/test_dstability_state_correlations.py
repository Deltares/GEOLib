import pytest

from geolib.geometry import Point
from geolib.models import DStabilityModel
from geolib.models.dstability.internal import StateCorrelation
from geolib.models.dstability.states import DStabilityStatePoint, DStabilityStress


class TestDStabilityStates:
    def setup_class(self):
        self.dm = DStabilityModel(filename=None)
        layer_1 = [
            Point(x=-50, z=-10),
            Point(x=50, z=-10),
            Point(x=50, z=-20),
            Point(x=-50, z=-20),
        ]

        layer_2 = [
            Point(x=-50, z=-5),
            Point(x=50, z=-5),
            Point(x=50, z=-10),
            Point(x=-50, z=-10),
        ]

        layers_and_soils = [
            (layer_1, "Sand"),
            (layer_2, "H_Ro_z&k"),
        ]
        layer_ids = []

        for layer, soil in layers_and_soils:
            layer_id = self.dm.add_layer(layer, soil)
            layer_ids.append(layer_id)

        # add state point
        self.id_state_one = self.dm.add_state_point(
            DStabilityStatePoint(
                layer_id=layer_ids[0],  # HV layer
                point=Point(x=0, z=-7.5),
                stress=DStabilityStress(pop=10.0),
            )
        )
        self.id_state_two = self.dm.add_state_point(
            DStabilityStatePoint(
                layer_id=layer_ids[1],  # Sand layer
                point=Point(x=0, z=-15),
                stress=DStabilityStress(pop=10.0),
            )
        )

    @pytest.mark.unittest
    def test_dstability_add_state_correlation_is_instance(self):
        _ = self.dm.add_state_correlation([self.id_state_one, self.id_state_two])

        assert isinstance(self.dm.datastructure.statecorrelations[0], StateCorrelation)

    @pytest.mark.unittest
    def test_dstability_add_state_correlation_wrong_layer_id(self):
        with pytest.raises(ValueError):
            _ = self.dm.add_state_correlation([self.id_state_one, -1])
