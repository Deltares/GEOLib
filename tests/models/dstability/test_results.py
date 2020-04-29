import pytest

from geolib.models.dstability.dstability_model import DStabilityModel
from geolib.models.dstability.internal import Stage, CalculationSettings, AnalysisType, CalculationType, UpliftVanResult, UpliftVanParticleSwarmResult, UpliftVanReliabilityResult, SpencerGeneticAlgorithmResult, SpencerReliabilityResult, SpencerResult, BishopBruteForceResult, BishopReliabilityResult, BishopResult


@pytest.fixture
def _get_dstability_model():
    model = DStabilityModel(inputfn=None)

    test_cases = [
        (AnalysisType.UPLIFT_VAN, CalculationType.DETERMINISTIC, 'uplift_van_results', UpliftVanResult),
        (AnalysisType.UPLIFT_VAN_PARTICLE_SWARM, CalculationType.DETERMINISTIC, 'uplift_van_particle_swarm_results', UpliftVanParticleSwarmResult),
        (AnalysisType.UPLIFT_VAN, CalculationType.PROBABILISTIC, 'uplift_van_reliability_results', UpliftVanReliabilityResult),
        (AnalysisType.SPENCER_GENETIC, CalculationType.DETERMINISTIC, 'spencer_genetic_algorithm_results', SpencerGeneticAlgorithmResult),
        (AnalysisType.SPENCER_GENETIC, CalculationType.PROBABILISTIC, 'spencer_reliability_results', SpencerReliabilityResult),
        (AnalysisType.SPENCER, CalculationType.DETERMINISTIC, 'spencer_results', SpencerResult),
        (AnalysisType.BISHOP_BRUTE_FORCE, CalculationType.DETERMINISTIC, 'bishop_bruteforce_results', BishopBruteForceResult),
        (AnalysisType.BISHOP, CalculationType.PROBABILISTIC, 'bishop_reliability_results', BishopReliabilityResult),
        (AnalysisType.BISHOP, CalculationType.DETERMINISTIC, 'bishop_results', BishopResult),
    ]

    # Set stages and calculationsettings to empty lists since to overwrite the defaults.
    model.datastructure.stages = []
    model.datastructure.calculationsettings = []

    for i, (analysis_type, calculation_type, result_attribute, result_class) in enumerate(test_cases):
        stage_id = str(i)
        result_id = str(100 + i)  # This way result id's and stage id's don't overlap.  # TODO research if that matters.
        model.datastructure.stages.append(Stage(Id=stage_id, ResultId=result_id))
        model.datastructure.calculationsettings.append(CalculationSettings(AnalysisType=analysis_type, CalculationType=calculation_type))
        getattr(model.datastructure, result_attribute).append(result_class(Id=result_id))

    return model


class TestDStabilityResults:

    @pytest.mark.unittest
    def test_stage_not_available_raises_value_error(self, _get_dstability_model):
        model = _get_dstability_model

        with pytest.raises(ValueError):
            model.results(10)

    @pytest.mark.unittest
    def test_get_result(self, _get_dstability_model):
        model = _get_dstability_model

        for i, _ in enumerate(model.datastructure.stages):
            result = model.results(stage_id=i)

            assert isinstance(result, dict)
