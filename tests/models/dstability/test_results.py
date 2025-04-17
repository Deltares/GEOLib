import pytest

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import (
    AnalysisType,
    BishopBruteForceReliabilityResult,
    BishopBruteForceResult,
    BishopReliabilityResult,
    BishopResult,
    BishopSlipCircleResult,
    CalculationSettings,
    CalculationType,
    PersistableCalculation,
    PersistableCircle,
    PersistablePoint,
    Scenario,
    SpencerGeneticAlgorithmReliabilityResult,
    SpencerGeneticAlgorithmResult,
    SpencerReliabilityResult,
    SpencerResult,
    SpencerSlipPlaneResult,
    UpliftVanParticleSwarmReliabilityResult,
    UpliftVanParticleSwarmResult,
    UpliftVanReliabilityResult,
    UpliftVanResult,
    UpliftVanSlipCircleResult,
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


def _slip_plane() -> list[PersistablePoint]:
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


def _uplift_van_particle_swarm_reliability_result(
    result_id: str,
) -> UpliftVanParticleSwarmReliabilityResult:
    return UpliftVanParticleSwarmReliabilityResult(
        Id=result_id,
        FailureProbability=_failure_probability,
        LeftCenter=_left_center_persistable_point(),
        RightCenter=_right_center_persistable_point(),
        TangentLine=_z_tangent_line,
    )


def _spencer_result(result_id: str) -> SpencerResult:
    return SpencerResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, SlipPlane=_slip_plane()
    )


def _spencer_genetic_algorithm_result(result_id: str) -> SpencerGeneticAlgorithmResult:
    return SpencerGeneticAlgorithmResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, SlipPlane=_slip_plane()
    )


def _spencer_genetic_algorithm_reliability_result(
    result_id: str,
) -> SpencerGeneticAlgorithmReliabilityResult:
    return SpencerGeneticAlgorithmReliabilityResult(
        Id=result_id, FailureProbability=_failure_probability, SlipPlane=_slip_plane()
    )


def _spencer_reliability_result(result_id: str) -> SpencerReliabilityResult:
    return SpencerReliabilityResult(
        Id=result_id, FailureProbability=_failure_probability, SlipPlane=_slip_plane()
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


def _bishop_brute_force_result(result_id: str) -> BishopBruteForceResult:
    return BishopBruteForceResult(
        Id=result_id, FactorOfSafety=_valid_safety_factor, Circle=_persistable_circle()
    )


def _bishop_brute_force_reliability_result(
    result_id: str,
) -> BishopBruteForceReliabilityResult:
    return BishopBruteForceReliabilityResult(
        Id=result_id,
        FailureProbability=_failure_probability,
        Circle=_persistable_circle(),
    )


@pytest.fixture
def _get_dstability_model() -> DStabilityModel:
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
            AnalysisType.UPLIFT_VAN_PARTICLE_SWARM,
            CalculationType.PROBABILISTIC,
            "uplift_van_particle_swarm_reliability_results",
            _uplift_van_particle_swarm_reliability_result,
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
            AnalysisType.SPENCER_GENETIC,
            CalculationType.PROBABILISTIC,
            "spencer_genetic_algorithm_reliability_results",
            _spencer_genetic_algorithm_reliability_result,
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
            _bishop_brute_force_result,
        ),
        (
            AnalysisType.BISHOP_BRUTE_FORCE,
            CalculationType.PROBABILISTIC,
            "bishop_bruteforce_reliability_results",
            _bishop_brute_force_reliability_result,
        ),
    ]

    # Set stages and calculationsettings to empty lists since to overwrite the defaults.
    model.datastructure.scenarios = [Scenario(Id=str(999))]
    model.datastructure.calculationsettings = []

    for i, (analysis_type, calculation_type, result_attribute, result_class) in enumerate(
        test_cases
    ):
        calculation_id = str(i)
        result_id = str(100 + i)
        calculation_settings_id = str(200 + i)
        model.datastructure.scenarios[0].Calculations.append(
            PersistableCalculation(
                Id=calculation_id,
                CalculationSettingsId=calculation_settings_id,
                ResultId=result_id,
            )
        )
        model.datastructure.calculationsettings.append(
            CalculationSettings(
                Id=calculation_settings_id,
                AnalysisType=analysis_type,
                CalculationType=calculation_type,
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

        amount_of_calculations = len(model.datastructure.scenarios[0].Calculations)
        with pytest.raises(ValueError):
            model.get_result(
                scenario_index=0, calculation_index=amount_of_calculations + 1
            )

    @pytest.mark.unittest
    def test_get_result(self, _get_dstability_model: DStabilityModel):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.scenarios[0].Calculations):
            result = model.get_result(scenario_index=0, calculation_index=i)

            assert isinstance(
                result,
                (
                    UpliftVanParticleSwarmResult,
                    UpliftVanParticleSwarmReliabilityResult,
                    UpliftVanReliabilityResult,
                    UpliftVanResult,
                    SpencerResult,
                    SpencerReliabilityResult,
                    SpencerGeneticAlgorithmResult,
                    SpencerGeneticAlgorithmReliabilityResult,
                    BishopResult,
                    BishopReliabilityResult,
                    BishopBruteForceResult,
                    BishopBruteForceReliabilityResult,
                ),
            )

    @pytest.mark.unittest
    def test_get_slipcircle_result(self, _get_dstability_model):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.scenarios[0].Calculations):
            result_substructure = model._get_result_substructure(
                scenario_index=0, calculation_index=i
            )

            if isinstance(
                result_substructure,
                (
                    SpencerReliabilityResult,
                    SpencerResult,
                    SpencerGeneticAlgorithmResult,
                    SpencerGeneticAlgorithmReliabilityResult,
                ),
            ):
                with pytest.raises(AttributeError):
                    model.get_slipcircle_result(scenario_index=0, calculation_index=i)
            else:
                slipplane_result = model.get_slipcircle_result(
                    scenario_index=0, calculation_index=i
                )

                assert isinstance(
                    slipplane_result, (BishopSlipCircleResult, UpliftVanSlipCircleResult)
                )

    @pytest.mark.unittest
    def test_get_slipplane_result(self, _get_dstability_model):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.scenarios[0].Calculations):
            result_substructure = model._get_result_substructure(
                scenario_index=0, calculation_index=i
            )

            if not isinstance(
                result_substructure,
                (
                    SpencerReliabilityResult,
                    SpencerResult,
                    SpencerGeneticAlgorithmResult,
                    SpencerGeneticAlgorithmReliabilityResult,
                ),
            ):
                with pytest.raises(AttributeError):
                    model.get_slipplane_result(scenario_index=0, calculation_index=i)
            else:
                slipplane_result = model.get_slipplane_result(
                    scenario_index=0, calculation_index=i
                )

                assert isinstance(slipplane_result, SpencerSlipPlaneResult)

    @pytest.mark.unittest
    def test_output_isinstance_list(self, _get_dstability_model: DStabilityModel):
        model = _get_dstability_model

        model.datastructure.scenarios[0].Calculations.append(
            PersistableCalculation(Id="200", ResultId=None)
        )

        output = model.output
        assert isinstance(output, list)
        assert len(output) == 13

        assert isinstance(output[0], UpliftVanResult)
        assert isinstance(output[1], UpliftVanReliabilityResult)
        assert isinstance(output[2], UpliftVanParticleSwarmResult)
        assert output[12] is None

    @pytest.mark.unittest
    def test_get_result_with_none_is_current_calculation_result(
        self, _get_dstability_model: DStabilityModel
    ):
        model = _get_dstability_model
        model.current_scenario = 0
        model.current_calculation = 2

        output = model.get_result()
        assert isinstance(output, UpliftVanParticleSwarmResult)

    @pytest.mark.unittest
    def test_get_result_with_id_is_expected_spencer_result(
        self, _get_dstability_model: DStabilityModel
    ):
        model = _get_dstability_model
        output = model.get_result(0, 3)
        assert isinstance(output, UpliftVanParticleSwarmReliabilityResult)
