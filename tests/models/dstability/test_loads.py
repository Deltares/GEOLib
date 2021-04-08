from typing import List

import pytest
from pydantic import ValidationError

from geolib.geometry.one import Point
from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    PersistableLayerLoad,
    PersistableLineLoad,
    PersistableSoilLayer,
    PersistableUniformLoad,
)
from geolib.models.dstability.loads import Consolidation, LineLoad, UniformLoad


@pytest.fixture
def _get_uniform_load() -> UniformLoad:
    return UniformLoad(
        label="this is a uniform load",
        start=0,
        end=1,
        magnitude=10,
        angle_of_distribution=45,
    )


@pytest.fixture
def _get_line_load() -> LineLoad:
    return LineLoad(
        label="this is a line load",
        location=Point(x=0, z=0),
        magnitude=10,
        angle=0,
        angle_of_distribution=45,
    )


@pytest.fixture
def _get_consolidations() -> List[Consolidation]:
    return [Consolidation(degree=100, layer_id=15)]


class TestConsolidation:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "degree",
        [
            pytest.param(0, id="inclusive lower bound"),
            pytest.param(0, id="between bounds"),
            pytest.param(90, id="inclusive upper bound"),
        ],
    )
    def test_create_consolidation_with_valid_paramters(self, degree):
        consolidation = Consolidation(degree=degree, layer_id=1,)

        assert isinstance(consolidation, Consolidation)

    @pytest.mark.unittest
    def test_get_consolidations_fixture_is_valid(self, _get_consolidations):

        consolidations = _get_consolidations

        assert isinstance(consolidations, List)
        assert len(consolidations) > 0
        for consolidation in consolidations:
            assert isinstance(consolidation, Consolidation)

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "degree",
        [
            pytest.param(-1, id="exceeds lower bound"),
            pytest.param(101, id="exceeds upper bound"),
        ],
    )
    def test_create_consolidation_with_invalid_degree_raises_validation_error(
        self, degree
    ):
        with pytest.raises(ValidationError):
            Consolidation(
                degree=degree, layer_id=1,
            )


class TestUniformLoad:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "magnitude",
        [
            pytest.param(0, id="inlcusive lower bound"),
            pytest.param(100, id="bigger than lower bound"),
        ],
    )
    @pytest.mark.parametrize(
        "angle_of_distribution",
        [
            pytest.param(0, id="inclusive lower bound"),
            pytest.param(90, id="inclusive upper bound"),
        ],
    )
    def test_create_uniform_load_with_valid_paramters(
        self, magnitude, angle_of_distribution
    ):
        uniform_load = UniformLoad(
            start=0,
            end=1,
            magnitude=magnitude,
            angle_of_distribution=angle_of_distribution,
        )

        assert isinstance(uniform_load, UniformLoad)

    @pytest.mark.unittest
    def test_get_uniform_load_fixture_is_valid(self, _get_uniform_load):

        uniform_load = _get_uniform_load

        assert isinstance(uniform_load, UniformLoad)

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "end",
        [
            pytest.param(0, id="equal to start"),
            pytest.param(-10, id="smaller than start"),
        ],
    )
    def test_create_uniform_load_with_invalid_end_relative_to_start_raises_validation_error(
        self, end
    ):
        with pytest.raises(ValidationError):
            UniformLoad(start=0, end=end, magnitude=5, angle_of_distribution=45)

    @pytest.mark.unittest
    def test_create_uniform_load_with_invalid_magnitude_raises_validation_error(self):
        with pytest.raises(ValidationError):
            UniformLoad(start=0, end=1, magnitude=-5, angle_of_distribution=45)

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "angle_of_distribution",
        [
            pytest.param(-10, id="exceeds lower bound"),
            pytest.param(100, id="exceeds upper bound"),
        ],
    )
    def test_create_uniform_load_with_invalid_angle_of_distribution_raises_validation_error(
        self, angle_of_distribution
    ):
        with pytest.raises(ValidationError):
            UniformLoad(
                start=0, end=1, magnitude=5, angle_of_distribution=angle_of_distribution
            )

    @pytest.mark.unittest
    def test_non_uniform_load_to_internal_datastructure(self, _get_uniform_load):
        uniform_load = _get_uniform_load

        internal_datastructure = uniform_load.to_internal_datastructure()

        assert isinstance(internal_datastructure, PersistableUniformLoad)

        assert uniform_load.label == internal_datastructure.Label
        assert uniform_load.start == internal_datastructure.Start
        assert uniform_load.end == internal_datastructure.End
        assert uniform_load.magnitude == internal_datastructure.Magnitude
        assert uniform_load.angle_of_distribution == internal_datastructure.Spread


class TestLineLoad:
    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "magnitude",
        [
            pytest.param(0, id="inlcusive lower bound"),
            pytest.param(100, id="bigger than lower bound"),
        ],
    )
    @pytest.mark.parametrize(
        "angle",
        [
            pytest.param(-360, id="inclusive lower bound"),
            pytest.param(0, id="between bounds"),
            pytest.param(360, id="inclusive upper bound"),
        ],
    )
    @pytest.mark.parametrize(
        "angle_of_distribution",
        [
            pytest.param(0, id="inclusive lower bound"),
            pytest.param(45, id="between bounds"),
            pytest.param(90, id="inclusive upper bound"),
        ],
    )
    def test_create_line_load_with_valid_paramters(
        self, magnitude, angle, angle_of_distribution
    ):
        line_load = LineLoad(
            location=Point(x=0, z=0),
            magnitude=magnitude,
            angle=angle,
            angle_of_distribution=angle_of_distribution,
        )

        assert isinstance(line_load, LineLoad)

    @pytest.mark.unittest
    def test_get_line_load_fixture_is_valid(self, _get_line_load):

        line_load = _get_line_load

        assert isinstance(line_load, LineLoad)

    @pytest.mark.unittest
    def test_create_line_load_with_invalid_magnitude_raises_validation_error(self):
        with pytest.raises(ValidationError):
            LineLoad(
                location=Point(x=0, z=0), magnitude=-5, angle=0, angle_of_distribution=0
            )

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "angle",
        [
            pytest.param(-400, id="exceeds lower bound"),
            pytest.param(400, id="exceeds upper bound"),
        ],
    )
    def test_create_line_load_with_invalid_angle_raises_validation_error(self, angle):
        with pytest.raises(ValidationError):
            LineLoad(
                location=Point(x=0, z=0),
                magnitude=5,
                angle=angle,
                angle_of_distribution=45,
            )

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "angle_of_distribution",
        [
            pytest.param(-10, id="exceeds lower bound"),
            pytest.param(100, id="exceeds upper bound"),
        ],
    )
    def test_create_line_load_with_invalid_angle_of_distribution_raises_validation_error(
        self, angle_of_distribution
    ):
        with pytest.raises(ValidationError):
            LineLoad(
                location=Point(x=0, z=0),
                magnitude=5,
                angle=0,
                angle_of_distribution=angle_of_distribution,
            )

    @pytest.mark.unittest
    def test_line_load_to_internal_datastructure(self, _get_line_load):
        line_load = _get_line_load

        internal_datastructure = line_load.to_internal_datastructure()

        assert isinstance(internal_datastructure, PersistableLineLoad)

        assert line_load.label == internal_datastructure.Label
        assert line_load.location.x == internal_datastructure.Location.X
        assert line_load.location.z == internal_datastructure.Location.Z
        assert line_load.magnitude == internal_datastructure.Magnitude
        assert line_load.angle == internal_datastructure.Angle
        assert line_load.angle_of_distribution == internal_datastructure.Spread


class TestDStabilityModelAddLoad:
    @pytest.mark.unittest
    def test_add_invalid_load_raises_value_error(self):
        dstability_model = DStabilityModel()

        class NotaDStabilityLoad:
            pass

        load = NotaDStabilityLoad()

        with pytest.raises(ValueError):
            dstability_model.add_load(load=load, stage_id=0)

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "stage_id",
        [
            pytest.param(0, id="default stage id"),
            pytest.param(None, id="no stage_id argument"),
        ],
    )
    @pytest.mark.parametrize(
        "use_consolidations",
        [
            pytest.param(True, id="pass consolidations argument"),
            pytest.param(False, id="no consolidations argument"),
        ],
    )
    def test_add_valid_uniform_load(
        self, _get_uniform_load, _get_consolidations, use_consolidations, stage_id
    ):
        dstability_model = DStabilityModel()
        if stage_id is None:
            # TODO Fix this logic in the model itself?
            stage_id = dstability_model.current_stage
        loads_id = 10
        soil_layer_id = 15
        soil_layers_id = 20

        dstability_model.datastructure.stages[stage_id].LoadsId = str(loads_id)
        dstability_model.datastructure.stages[stage_id].SoilLayersId = str(soil_layers_id)
        dstability_model.datastructure.loads[stage_id].Id = str(loads_id)
        dstability_model.datastructure.soillayers[stage_id].Id = str(soil_layers_id)
        dstability_model.datastructure.soillayers[stage_id].SoilLayers.append(
            PersistableSoilLayer(LayerId=str(soil_layer_id))
        )

        uniform_load = _get_uniform_load
        consolidations = _get_consolidations if use_consolidations else None

        dstability_model.add_load(
            load=uniform_load, consolidations=consolidations, stage_id=stage_id
        )

        uniformloads = dstability_model.datastructure.loads[stage_id].UniformLoads
        assert len(uniformloads) == 1
        assert isinstance(uniformloads[0], PersistableUniformLoad,)
        if use_consolidations:
            assert len(uniformloads[0].Consolidations) == 1
            assert uniformloads[0].Consolidations[0].LayerId == str(soil_layer_id)

    @pytest.mark.integrationtest
    def test_add_valid_line_load(self):
        pass

    @pytest.mark.integrationtest
    def test_add_load_invalid_stage_id_raises_value_error(self):
        pass

    @pytest.mark.integrationtest
    def test_add_load_has_no_loads_raises_value_error(self):
        pass


class TestDStabilityModelAddSoilLayerConsolidations:
    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "stage_id",
        [
            pytest.param(0, id="default stage id"),
            pytest.param(None, id="no stage_id argument"),
        ],
    )
    @pytest.mark.parametrize(
        "use_consolidations",
        [
            pytest.param(True, id="pass consolidations argument"),
            pytest.param(False, id="no consolidations argument"),
        ],
    )
    def test_add_valid_layer_load(
        self, _get_consolidations, use_consolidations, stage_id
    ):
        dstability_model = DStabilityModel()
        stage_id = stage_id or 0
        loads_id = 10
        soil_layer_id_a = 15
        soil_layer_id_b = 16
        soil_layers_id = 20

        dstability_model.datastructure.stages[stage_id].LoadsId = str(loads_id)
        dstability_model.datastructure.stages[stage_id].SoilLayersId = str(soil_layers_id)
        dstability_model.datastructure.loads[stage_id].Id = str(loads_id)
        dstability_model.datastructure.soillayers[stage_id].Id = str(soil_layers_id)
        dstability_model.datastructure.soillayers[stage_id].SoilLayers.append(
            PersistableSoilLayer(LayerId=str(soil_layer_id_a))
        )
        dstability_model.datastructure.soillayers[stage_id].SoilLayers.append(
            PersistableSoilLayer(LayerId=str(soil_layer_id_b))
        )

        consolidations = _get_consolidations if use_consolidations else None
        dstability_model.add_soil_layer_consolidations(
            soil_layer_id=soil_layer_id_b,
            consolidations=consolidations,
            stage_id=stage_id,
        )

        assert len(dstability_model.datastructure.loads[stage_id].LayerLoads) == 1
        assert isinstance(
            dstability_model.datastructure.loads[stage_id].LayerLoads[0],
            PersistableLayerLoad,
        )

    @pytest.mark.unittest
    def test_add_layer_load_invalid_stage_id_raises_value_error(self):
        pass

    @pytest.mark.unittest
    def test_add_layer_load_has_no_loads_raises_value_error(self):
        pass
