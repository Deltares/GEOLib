import pytest
from typing import List

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    Stage,
    CalculationSettings,
    AnalysisType,
    CalculationType,
    UpliftVanResult,
    UpliftVanParticleSwarmResult,
    UpliftVanReliabilityResult,
    SpencerGeneticAlgorithmResult,
    SpencerReliabilityResult,
    SpencerResult,
    BishopBruteForceResult,
    BishopReliabilityResult,
    BishopResult,
    PersistableCircle,
    PersistablePoint,
    BishopSlipCircleResult,
    UpliftVanSlipCircleResult,
    SpencerSlipPlaneResult,
)


_valid_safety_factor = 1.2
_failure_probability = 0.8
_z_tangent_line = -10


def _left_center_persistable_point() -> PersistablePoint:
    return PersistablePoint(X=0, Z=10)


def _right_center_persistable_point() -> PersistablePoint:
    return PersistablePoint(X=10, Z=0)


def _persistable_circle() -> PersistableCircle:
    return PersistableCircle(Center=_left_center_persistable_point(), Radius=5)


def _slip_pane() -> List[PersistablePoint]:
    x_z_coordinates = [(0, 10), (2.5, 8), (5, 4), (2.5, 2), (10, 0)]
    return [PersistablePoint(X=x, Z=z) for x, z in x_z_coordinates]


def _uplift_van_result(result_id: str) -> UpliftVanResult:
    return UpliftVanResult(
        Id=result_id,
        FactorOfSafety=_valid_safety_factor,
        LeftCenter=_left_center_persistable_point(),
        RightCenter=_right_center_persistable_point(),
        TangentLine=_z_tangent_line,
    )


def _uplift_van_reliability_result(result_id: str) -> UpliftVanReliabilityResult:
    return UpliftVanReliabilityResult(
        Id=result_id,
        FailureProbability=_failure_probability,
        LeftCenter=_left_center_persistable_point(),
        RightCenter=_right_center_persistable_point(),
        TangentLine=_z_tangent_line,
    )


def _uplift_van_particle_swarm_result(result_id: str) -> UpliftVanParticleSwarmResult:
    return UpliftVanParticleSwarmResult(
        Id=result_id,
        FactorOfSafety=_valid_safety_factor,
        LeftCenter=_left_center_persistable_point(),
        RightCenter=_right_center_persistable_point(),
        TangentLine=_z_tangent_line,
    )


def _spencer_result(result_id: str) -> SpencerResult:
    return SpencerResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, SlipPlane=_slip_pane()
    )


def _spencer_genetic_algorithm_result(result_id: str) -> SpencerGeneticAlgorithmResult:
    return SpencerGeneticAlgorithmResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, SlipPlane=_slip_pane()
    )


def _spencer_reliability_result(result_id: str) -> SpencerReliabilityResult:
    return SpencerReliabilityResult(
        Id=result_id, FailureProbability=_failure_probability, SlipPlane=_slip_pane()
    )


def _bishop_result(result_id: str) -> BishopResult:
    return BishopResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, Circle=_persistable_circle()
    )


def _bishop_reliability_result(result_id: str) -> BishopReliabilityResult:
    return BishopReliabilityResult(
        Id=result_id,
        FailureProbability=_failure_probability,
        Circle=_persistable_circle(),
    )


def _bishop_bruce_force_result(result_id: str) -> BishopBruteForceResult:
    return BishopBruteForceResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, Circle=_persistable_circle()
    )


@pytest.fixture
def _get_dstability_model():
    model = DStabilityModel(filename=None)

    test_cases = [
        (
            AnalysisType.UPLIFT_VAN,
            CalculationType.DETERMINISTIC,
            "uplift_van_results",
            _uplift_van_result,
        ),
        (
            AnalysisType.UPLIFT_VAN,
            CalculationType.PROBABILISTIC,
            "uplift_van_reliability_results",
            _uplift_van_reliability_result,
        ),
        (
            AnalysisType.UPLIFT_VAN_PARTICLE_SWARM,
            CalculationType.DETERMINISTIC,
            "uplift_van_particle_swarm_results",
            _uplift_van_particle_swarm_result,
        ),
        (
            AnalysisType.SPENCER,
            CalculationType.DETERMINISTIC,
            "spencer_results",
            _spencer_result,
        ),
        (
            AnalysisType.SPENCER,
            CalculationType.PROBABILISTIC,
            "spencer_reliability_results",
            _spencer_reliability_result,
        ),
        (
            AnalysisType.SPENCER_GENETIC,
            CalculationType.DETERMINISTIC,
            "spencer_genetic_algorithm_results",
            _spencer_genetic_algorithm_result,
        ),
        (
            AnalysisType.BISHOP,
            CalculationType.DETERMINISTIC,
            "bishop_results",
            _bishop_result,
        ),
        (
            AnalysisType.BISHOP,
            CalculationType.PROBABILISTIC,
            "bishop_reliability_results",
            _bishop_reliability_result,
        ),
        (
            AnalysisType.BISHOP_BRUTE_FORCE,
            CalculationType.DETERMINISTIC,
            "bishop_bruteforce_results",
            _bishop_bruce_force_result,
        ),
    ]

    # Set stages and calculationsettings to empty lists since to overwrite the defaults.
    model.datastructure.stages = []
    model.datastructure.calculationsettings = []

    for i, (analysis_type, calculation_type, result_attribute, result_class) in enumerate(
        test_cases
    ):
        stage_id = str(i)
        result_id = str(
            100 + i
        )  # This way result id's and stage id's don't overlap.  # TODO research if that matters.
        model.datastructure.stages.append(Stage(Id=stage_id, ResultId=result_id))
        model.datastructure.calculationsettings.append(
            CalculationSettings(
                AnalysisType=analysis_type, CalculationType=calculation_type
            )
        )
        getattr(model.datastructure, result_attribute).append(
            result_class(result_id=result_id)
        )

    return model


class TestDStabilityResults:
    @pytest.mark.unittest
    def test_stage_not_available_raises_value_error(self, _get_dstability_model):
        model = _get_dstability_model

        amount_of_stages = len(model.datastructure.stages)
        with pytest.raises(ValueError):
            model.get_result(amount_of_stages + 1)

    @pytest.mark.unittest
    def test_get_result(self, _get_dstability_model):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.stages):
            result = model.get_result(stage_id=i)

            assert isinstance(result, dict)

    @pytest.mark.unittest
    def test_get_slipcircle_result(self, _get_dstability_model):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.stages):

            result_substructure = model._get_result_substructure(stage_id=i)

            if isinstance(
                result_substructure,
                (SpencerReliabilityResult, SpencerResult, SpencerGeneticAlgorithmResult),
            ):
                with pytest.raises(AttributeError):
                    model.get_slipcircle_result(stage_id=i)
            else:
                slipplane_result = model.get_slipcircle_result(stage_id=i)

                assert isinstance(
                    slipplane_result, (BishopSlipCircleResult, UpliftVanSlipCircleResult)
                )

    @pytest.mark.unittest
    def test_get_slipplane_result(self, _get_dstability_model):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.stages):

            result_substructure = model._get_result_substructure(stage_id=i)

            if not isinstance(
                result_substructure,
                (SpencerReliabilityResult, SpencerResult, SpencerGeneticAlgorithmResult),
            ):
                with pytest.raises(AttributeError):
                    model.get_slipplane_result(stage_id=i)
            else:
                slipplane_result = model.get_slipplane_result(stage_id=i)

                assert isinstance(slipplane_result, SpencerSlipPlaneResult)
