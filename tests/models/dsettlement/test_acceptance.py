import logging
import os
import pathlib
from datetime import timedelta
from pathlib import Path
from typing import List
from warnings import warn

import pydantic
import pytest
from pydantic.color import Color
from teamcity import is_running_under_teamcity

import geolib.models.dsettlement.loads as loads
import geolib.soils as soil_external
from geolib.geometry.one import Point
from geolib.models import BaseModel
from geolib.models.dsettlement.dsettlement_model import DSettlementModel
from geolib.models.dsettlement.internal import (
    Bool,
    Boundaries,
    Boundary,
    ConsolidationModel,
    Curve,
    Curves,
    Dimension,
    DispersionConditionLayerBoundary,
    DSeriePoint,
    DSettlementStructure,
    GeometryData,
    Layer,
    Layers,
    Model,
    Points,
    PreconPressureWithinLayer,
    SoilModel,
    StrainType,
    StressDistributionLoads,
    StressDistributionSoil,
    Version,
)
from geolib.models.dsettlement.loads import RectangularLoad
from geolib.soils import (
    IsotacheParameters,
    Soil,
    SoilClassificationParameters,
    SoilWeightParameters,
    StateType,
)
from tests.utils import TestUtils, only_teamcity


class TestDSettlementAcceptance:
    def setup_class(self):
        self.soils = [
            Soil(
                name="Sand",
                soil_weight_parameters=SoilWeightParameters(
                    saturated_weight=19.0, unsaturated_weight=17.0
                ),
            ),
            Soil(
                name="Peat",
                soil_weight_parameters=SoilWeightParameters(
                    saturated_weight=10.0, unsaturated_weight=10.0
                ),
            ),
            Soil(
                name="Clay",
                soil_weight_parameters=SoilWeightParameters(
                    saturated_weight=14.0, unsaturated_weight=14.0
                ),
            ),
            Soil(
                name="Embankement",
                soil_weight_parameters=SoilWeightParameters(
                    saturated_weight=16.0, unsaturated_weight=16.0
                ),
            ),
        ]

        self.points = [
            Point(x=-50, z=0.0),  # 0 top layer
            Point(x=-10, z=0.0),  # 1
            Point(x=0, z=2),  # 2
            Point(x=10, z=2),  # 3
            Point(x=30, z=0.0),  # 4
            Point(x=50, z=0.0),  # 5
            Point(x=-50, z=-5),  # 6 second layer
            Point(x=50, z=-5),  # 7
            Point(x=-50, z=-10),  # 8 third layer
            Point(x=50, z=-10),  # 9
            Point(x=-50, z=-20),  # 10 fourth layer
            Point(x=50, z=-20),  # 11
            Point(x=-50, z=-2),  # 12 phreatic line
            Point(x=50, z=-2),  # 13
            Point(x=-50, z=1),  # 14 headline 1
            Point(x=50, z=1),  # 15
        ]

        dm = DSettlementModel()
        self.outputdir = Path(
            TestUtils.get_output_test_data_dir("dsettlement/acceptancetest/")
        )
        self.inputfile = Path(
            TestUtils.get_test_data_dir("test_data/dsettlement", "2dgeom_with10.sld")
        )

    @pytest.mark.systemtest
    def test_dsettlement_empty(self):
        dm = DSettlementModel()
        path = self.outputdir / "test_empty.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_add_soils(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)
        path = self.outputdir / "test_add_soils.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_add_soil_koppejan(self):
        dm = DSettlementModel()

        # TODO adding soils is too complex
        # should be something like
        # Soil(
        #    soilcp = 100.,
        #    soilcp1 = 10.,
        #    etc.
        # )

        soil_input = Soil(name="MyNewSoil")
        soil_input.soil_classification_parameters = SoilClassificationParameters()
        soil_input.soil_weight_parameters = soil_external.SoilWeightParameters()

        soil_input.soil_weight_parameters.saturated_weight = (
            soil_external.StochasticParameter(mean=20)
        )
        soil_input.soil_weight_parameters.unsaturated_weight = (
            soil_external.StochasticParameter(mean=30)
        )
        soil_input.soil_classification_parameters.initial_void_ratio = (
            soil_external.StochasticParameter(mean=0.1)
        )

        soil_input.koppejan_parameters = soil_external.KoppejanParameters(
            precon_koppejan_type=StateType.YIELD_STRESS
        )
        soil_input.soil_state = soil_external.SoilState(
            use_equivalent_age=True, equivalent_age=2
        )
        soil_input.koppejan_parameters.preconsolidation_pressure = (
            soil_external.StochasticParameter(mean=10)
        )

        dm.add_soil(soil_input)
        path = self.outputdir / "test_add_soil_koppejan.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_add_simple_geometry(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(
            points=[self.points[12], self.points[13]], is_phreatic=True
        )

        b1 = dm.add_boundary(points=[self.points[10], self.points[11]])
        b2 = dm.add_boundary(points=[self.points[8], self.points[9]])
        b3 = dm.add_boundary(points=[self.points[6], self.points[7]])
        b4 = dm.add_boundary(
            points=[self.points[0], self.points[1], self.points[4], self.points[5]]
        )
        b5 = dm.add_boundary(
            points=[
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
                self.points[4],
                self.points[5],
            ]
        )

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b1,
        )
        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b2,
        )
        l3 = dm.add_layer(
            material_name="Peat",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b4,
            boundary_bottom=b3,
        )
        l4 = dm.add_layer(
            material_name="Embankement",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b4,
        )

        path = self.outputdir / "test_simple_geometry.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_add_headlines(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(
            points=[self.points[12], self.points[13]], is_phreatic=True
        )
        hl_id = dm.add_head_line(
            points=[self.points[14], self.points[15]], is_phreatic=False
        )

        b1 = dm.add_boundary(points=[self.points[10], self.points[11]])
        b2 = dm.add_boundary(points=[self.points[8], self.points[9]])
        b3 = dm.add_boundary(points=[self.points[6], self.points[7]])
        b4 = dm.add_boundary(
            points=[self.points[0], self.points[1], self.points[4], self.points[5]]
        )
        b5 = dm.add_boundary(
            points=[
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
                self.points[4],
                self.points[5],
            ]
        )

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=hl_id,
            head_line_bottom=hl_id,
            boundary_top=b2,
            boundary_bottom=b1,
        )
        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=99,
            head_line_bottom=hl_id,
            boundary_top=b3,
            boundary_bottom=b2,
        )
        l3 = dm.add_layer(
            material_name="Peat",
            head_line_top=pl_id,
            head_line_bottom=99,
            boundary_top=b4,
            boundary_bottom=b3,
        )
        l4 = dm.add_layer(
            material_name="Embankement",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b4,
        )

        path = self.outputdir / "test_headlines.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_add_load(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(
            points=[self.points[12], self.points[13]], is_phreatic=True
        )

        b1 = dm.add_boundary(points=[self.points[10], self.points[11]])
        b2 = dm.add_boundary(points=[self.points[8], self.points[9]])
        b3 = dm.add_boundary(points=[self.points[6], self.points[7]])
        b4 = dm.add_boundary(
            points=[self.points[0], self.points[1], self.points[4], self.points[5]]
        )
        b5 = dm.add_boundary(
            points=[
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
                self.points[4],
                self.points[5],
            ]
        )

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b1,
        )
        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b2,
        )
        l3 = dm.add_layer(
            material_name="Peat",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b4,
            boundary_bottom=b3,
        )
        l4 = dm.add_layer(
            material_name="Embankement",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b4,
        )

        dm.add_non_uniform_load(
            "traffic",
            points=[self.points[2], Point(x=1, z=3), Point(x=9, z=3), self.points[3]],
            gamma_wet=25.0,
            gamma_dry=25.0,
            time_start=timedelta(days=0),
            time_end=timedelta(days=1000),
        )

        path = self.outputdir / "test_add_load.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_add_verticals(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(
            points=[self.points[12], self.points[13]], is_phreatic=True
        )

        b1 = dm.add_boundary(points=[self.points[10], self.points[11]])
        b2 = dm.add_boundary(points=[self.points[8], self.points[9]])
        b3 = dm.add_boundary(points=[self.points[6], self.points[7]])
        b4 = dm.add_boundary(
            points=[self.points[0], self.points[1], self.points[4], self.points[5]]
        )
        b5 = dm.add_boundary(
            points=[
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
                self.points[4],
                self.points[5],
            ]
        )

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b1,
        )
        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b2,
        )
        l3 = dm.add_layer(
            material_name="Peat",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b4,
            boundary_bottom=b3,
        )
        l4 = dm.add_layer(
            material_name="Embankement",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b4,
        )

        dm.set_verticals(locations=[Point(x=-10), Point(x=0), Point(x=10)])

        path = self.outputdir / "test_set_verticals.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_set_model(self):
        # koppejan, natural strain, darcy, vertical drains
        dm = DSettlementModel()

        dm.set_model(
            constitutive_model=SoilModel.NEN_KOPPEJAN,
            consolidation_model=ConsolidationModel.DARCY,
            is_vertical_drain=True,
            strain_type=StrainType.NATURAL,
            is_two_dimensional=True,
            is_fit_for_settlement_plate=False,
            is_probabilistic=False,
            is_horizontal_displacements=False,
            is_secondary_swelling=True,  # TODO document this parameter
            is_waspan=False,  # TODO document this parameter
        )

        path = self.outputdir / "test_set_model.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_set_residualtimes(self):
        # koppejan, natural strain, darcy, vertical drains

        dm = DSettlementModel()

        dm.set_calculation_times(
            time_steps=[timedelta(days=d) for d in [10, 100, 1000, 2000, 3000, 4000]]
        )

        path = self.outputdir / "test_set_residualtimes.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_layerload(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(
            points=[self.points[12], self.points[13]], is_phreatic=True
        )

        b1 = dm.add_boundary(points=[self.points[10], self.points[11]])
        b2 = dm.add_boundary(points=[self.points[8], self.points[9]])
        b3 = dm.add_boundary(points=[self.points[6], self.points[7]])
        b4 = dm.add_boundary(
            points=[self.points[0], self.points[1], self.points[4], self.points[5]]
        )
        b5 = dm.add_boundary(
            points=[
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
                self.points[4],
                self.points[5],
            ]
        )

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b1,
        )
        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b2,
        )
        l3 = dm.add_layer(
            material_name="Peat",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b4,
            boundary_bottom=b3,
        )
        l4 = dm.add_layer(
            material_name="Embankement",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b4,
        )

        path = self.outputdir / "test_layerload.sli"
        dm.serialize(path)

    @pytest.mark.systemtest
    def test_other_load(self):
        dm = DSettlementModel()
        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(
            points=[self.points[12], self.points[13]], is_phreatic=True
        )

        b1 = dm.add_boundary(points=[self.points[10], self.points[11]])
        b2 = dm.add_boundary(points=[self.points[8], self.points[9]])
        b3 = dm.add_boundary(points=[self.points[6], self.points[7]])
        b4 = dm.add_boundary(
            points=[self.points[0], self.points[1], self.points[4], self.points[5]]
        )
        b5 = dm.add_boundary(
            points=[
                self.points[0],
                self.points[1],
                self.points[2],
                self.points[3],
                self.points[4],
                self.points[5],
            ]
        )

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b1,
        )
        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b2,
        )
        l3 = dm.add_layer(
            material_name="Peat",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b4,
            boundary_bottom=b3,
        )
        l4 = dm.add_layer(
            material_name="Embankement",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b5,
            boundary_bottom=b4,
        )

        dm.add_other_load(
            name="rectangle",
            time=timedelta(days=100),
            point=Point(x=5.0, y=10.0, z=2.0),
            other_load=RectangularLoad(weight=25, alpha=0, xwidth=5.0, zwidth=10.0),
        )

        path = self.outputdir / "test_other_load.sli"
        dm.serialize(path)

    @pytest.mark.acceptance
    @pytest.mark.xfail  #   Wrong soils for now
    @only_teamcity
    def test_sorting_vertical_layer_boundaries(self):
        """
        Test sorting boundaries with 2 vertical layer boundaries
        Returns:

        """

        points = [
            Point(x=-50, z=-10),  # 0
            Point(x=50, z=-10),  # 1
            Point(x=-50, z=0.0),  # 2
            Point(x=0, z=0.0),  # 3
            Point(x=0.0, z=-10.0),  # 4
            Point(x=-50, z=-20),  # 5
            Point(x=50, z=-20),  # 6
            Point(x=50, z=0.0),  # 7
        ]

        dm = DSettlementModel()

        for soil in self.soils:
            dm.add_soil(soil)

        pl_id = dm.add_head_line(points=[points[0], points[1]], is_phreatic=True)

        b1 = dm.add_boundary(points=[points[0], points[4], points[1]])
        b2 = dm.add_boundary(points=[points[2], points[3], points[7]])
        b3 = dm.add_boundary(points=[points[0], points[4], points[3], points[7]])
        b4 = dm.add_boundary(points=[points[5], points[6]])

        l1 = dm.add_layer(
            material_name="Sand",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b1,
            boundary_bottom=b4,
        )

        l2 = dm.add_layer(
            material_name="Clay",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b3,
            boundary_bottom=b1,
        )

        l3 = dm.add_layer(
            material_name="peat",
            head_line_top=pl_id,
            head_line_bottom=pl_id,
            boundary_top=b2,
            boundary_bottom=b3,
        )

        dm.set_verticals(locations=[Point(x=-10), Point(x=0), Point(x=10)])

        dm.add_other_load(
            name="rectangle",
            time=timedelta(days=100),
            point=Point(x=-5.0, y=-5.0, z=0.0),
            other_load=RectangularLoad(weight=25, alpha=0, xwidth=5.0, zwidth=10.0),
        )

        # For manual checks
        path = self.outputdir / "test_sort_vertical_layer_boundaries.sli"
        dm.serialize(path)

        # Verify geometry is correct and we can parse output
        dm.execute()  # will raise on execution error
        assert dm.datastructure
