from typing import Optional
from enum import Enum, IntEnum
from geolib.models.dseries_parser import DSeriesNameKeyValueSubStructure
from geolib.soils import Soil, DistributionType, HorizontalBehaviourType
from geolib.soils import PreconType
from geolib.soils import StorageTypes


class Soil_Internal(DSeriesNameKeyValueSubStructure):
    """Representation of [SOIL] group."""

    name: Optional[str] = ""
    soilcolor: Optional[int] = 9764853
    soilgamdry: Optional[float] = 14
    soilgamwet: Optional[float] = 14
    soilinitialvoidratio: Optional[float] = 0
    soilcohesion: Optional[float] = 10  # fixed value cannot be modified
    soilphi: Optional[float] = 30  # fixed value cannot be modified
    soilpreconisotachetype: Optional[PreconType]
    soilpreconkoppejantype: Optional[PreconType]
    soiluseequivalentage: Optional[bool] = False
    soilequivalentage: Optional[float] = 19800
    soilpc: Optional[float] = 0
    soilocr: Optional[float] = 1
    soilpop: Optional[float] = 0
    soillimitstress: Optional[float] = 0  # fixed value
    soildrained: Optional[bool] = False
    soilapasapproximationbycpcs: Optional[bool] = False
    soilcv: Optional[float] = 1e-12
    soilpermeabilityver: Optional[float] = 0.00000001
    soilpermeabilityhorfactor: Optional[float] = 1
    soilstoragetype: Optional[StorageTypes]
    soilpermeabilitystrainmodulus: Optional[float] = 1e15
    soiluseprobdefaults: Optional[bool] = False
    soilstdgamdry: Optional[float] = 0
    soilstdgamwet: Optional[float] = 0
    soilstdcv: Optional[float] = 0
    soilstdpc: Optional[float] = 0
    soilstdpricompindex: Optional[float] = 0.01  # SoilPriCompIndex
    soilstdseccompindex: Optional[float] = 0.1  # SoilSecCompIndex
    soilstdseccomprate: Optional[float] = 0.005  # SoilSecCompRate
    soilstdocr: Optional[float] = 0
    soilstdpermeabilityver: Optional[float] = 0
    soilstdpop: Optional[float] = 0
    soilstdpermeabilityhorfactor: Optional[float] = 0
    soilstdinitialvoidratio: Optional[float] = 0
    soilstdpermeabilitystrainmodulus: Optional[float] = 0  # fixed value
    soilstdlimitstress: Optional[float] = 0  # fixed value
    soilstdcp: Optional[float] = 0
    soilstdcp1: Optional[float] = 0
    soilstdcs: Optional[float] = 0
    soilstdcs1: Optional[float] = 0
    soilstdap: Optional[float] = 0
    soilstdasec: Optional[float] = 0
    soilstdcar: Optional[float] = 0
    soilstdca: Optional[float] = 0
    soilstdrratio: Optional[float] = 0
    soilstdcratio: Optional[float] = 0
    soilstdsratio: Optional[float] = 0  # fixed value
    soilstdcrindex: Optional[float] = 0
    soilstdccindex: Optional[float] = 0
    soilstdcswindex: Optional[float] = 0  # fixed value
    soildistgamdry: Optional[DistributionType] = DistributionType.Normal
    soildistgamwet: Optional[DistributionType] = DistributionType.Normal
    soildistcv: Optional[DistributionType] = DistributionType.Normal
    soildistdpc: Optional[DistributionType] = DistributionType.Normal
    soildistpricompindex: Optional[DistributionType] = DistributionType.Normal
    soildistseccompindex: Optional[DistributionType] = DistributionType.Normal
    soildistseccomprate: Optional[DistributionType] = DistributionType.Normal
    soildistocr: Optional[DistributionType] = DistributionType.Normal
    soildistpermeabilityver: Optional[DistributionType] = DistributionType.Normal
    soildistpop: Optional[DistributionType] = DistributionType.Normal
    soildistpermeabilityhorfactor: Optional[DistributionType] = DistributionType.Normal
    soildistinitialvoidratio: Optional[DistributionType] = DistributionType.Normal
    soildistpermeabilitystrainmodulus: Optional[
        DistributionType
    ] = DistributionType.Normal  # fixed value
    soildistlimitstress: Optional[
        DistributionType
    ] = DistributionType.Normal  # fixed value
    soildistcp: Optional[DistributionType] = DistributionType.Normal
    soildistcp1: Optional[DistributionType] = DistributionType.Normal
    soildistcs: Optional[DistributionType] = DistributionType.Normal
    soildistcs1: Optional[DistributionType] = DistributionType.Normal
    soildistap: Optional[DistributionType] = DistributionType.Normal
    soildistasec: Optional[DistributionType] = DistributionType.Normal
    soildistcar: Optional[DistributionType] = DistributionType.Normal
    soildistca: Optional[DistributionType] = DistributionType.Normal
    soildistrratio: Optional[DistributionType] = DistributionType.Normal
    soildistcratio: Optional[DistributionType] = DistributionType.Normal
    soildistsratio: Optional[DistributionType] = DistributionType.Normal  # fixed value
    soildistcrindex: Optional[DistributionType] = DistributionType.Normal
    soildistccindex: Optional[DistributionType] = DistributionType.Normal
    soildistcswindex: Optional[DistributionType] = DistributionType.Normal  # fixed value
    soilcorcpcp1: Optional[float] = 0
    soilcorcscp1: Optional[float] = 0
    soilcorcs1cp1: Optional[float] = 0
    soilcorapcp1: Optional[float] = 0
    soilcoraseccp1: Optional[float] = 0
    soilcorcrindexccindex: Optional[float] = 0
    soilcorrratiocratio: Optional[float] = 0
    soilcorcaccindexorcratio: Optional[float] = 0
    soilcorpricompindexseccompindex: Optional[float] = 0  # SoilPriCompIndex
    soilcorseccomprateseccompindex: Optional[float] = 0  # SoilSecCompRate
    soilcp: Optional[float] = 1
    soilcp1: Optional[float] = 1
    soilcs: Optional[float] = 1
    soilcs1: Optional[float] = 1
    soilap: Optional[float] = 1
    soilasec: Optional[float] = 1
    soilcar: Optional[float] = 10
    soilca: Optional[float] = 1
    soilcompratio: Optional[float] = 0  # fixed value
    soilrratio: Optional[float] = 1
    soilcratio: Optional[float] = 1
    soilsratio: Optional[float] = 0  # fixed value
    soilcrindex: Optional[float] = 1
    soilccindex: Optional[float] = 1
    soilcswindexfixed: Optional[float] = 0  # fixed value
    soilpricompindex: Optional[float] = 0.01  # SoilPriCompIndex
    soilseccompindex: Optional[float] = 0.1  # SoilSecCompIndex
    soilseccomprate: Optional[float] = 0.005  # SoilSecCompRate
    soilhorizontalbehaviourtype: Optional[
        HorizontalBehaviourType
    ] = HorizontalBehaviourType.Elastic
    soilelasticity: Optional[float] = 1000
    soildefaultelasticity: Optional[bool] = True

    @classmethod
    def convert_from_external_to_internal(cls, soil_external: Soil):
        mapping_dictionary = {
            "name": "name",
            "soilcolor": "color",
            "soilgamdry": "soil_parameters\\soil_weight_parameters\\unsaturated_weight\\mean",
            "soilgamwet": "soil_parameters\\soil_weight_parameters\\saturated_weight\\mean",
            "soilinitialvoidratio": "soil_parameters\\soil_classification_parameters\\initial_void_ratio\\mean",
            "soilcohesion": "",
            "soilphi": "",
            "soilpreconisotachetype": "soil_parameters\\isotache_parameters\\precon_isotache_type",
            "soilpreconkoppejantype": "soil_parameters\\koppejan_parameters\\precon_koppejan_type",
            "soiluseequivalentage": "soil_state\\use_equivalent_age",
            "soilequivalentage": "soil_state\\equivalent_age",
            "soilpc": "soil_parameters\\koppejan_parameters\\preconsolidation_pressure\\mean",
            "soilocr": "soil_parameters\\compression_parameters\\OCR\\mean",
            "soilpop": "soil_parameters\\compression_parameters\\POP\\mean",
            "soillimitstress": "",
            "soildrained": "is_drained",
            "soilapasapproximationbycpcs": "soil_parameters\\koppejan_parameters\\soil_ap_as_approximation_by_Cp_Cs",
            "soilcv": "soil_parameters\\undrained_parameters\\vertical_consolidation_coefficient\\mean",
            "soilpermeabilityver": "soil_parameters\\storage_parameters\\vertical_permeability\\mean",
            "soilpermeabilityhorfactor": "soil_parameters\\storage_parameters\\permeability_horizontal_factor\\mean",
            "soilstoragetype": "soil_parameters\\storage_parameters\\storage_type",
            "soilpermeabilitystrainmodulus": "soil_parameters\\storage_parameters\\permeability_strain_type",
            "soiluseprobdefaults": "use_probabilistic_defaults",
            "soilstdgamdry": "soil_parameters\\soil_weight_parameters\\unsaturated_weight\\standard_deviation",
            "soilstdgamwet": "soil_parameters\\soil_weight_parameters\\saturated_weight\\standard_deviation",
            "soilstdcv": "soil_parameters\\undrained_parameters\\vertical_consolidation_coefficient\\standard_deviation",
            "soilstdpc": "soil_parameters\\koppejan_parameters\\preconsolidation_pressure\\standard_deviation",
            "soilstdpricompindex": "soil_parameters\\isotache_parameters\\reloading_swelling_constant_a\\standard_deviation",
            "soilstdseccompindex": "soil_parameters\\isotache_parameters\\primary_compression_constant_b\\standard_deviation",
            "soilstdseccomprate": "soil_parameters\\isotache_parameters\\secondary_compression_constant_c\\standard_deviation",
            "soilstdocr": "soil_parameters\\compression_parameters\\OCR\\standard_deviation",
            "soilstdpermeabilityver": "soil_parameters\\storage_parameters\\vertical_permeability\\standard_deviation",
            "soilstdpop": "soil_parameters\\compression_parameters\\POP\\standard_deviation",
            "soilstdpermeabilityhorfactor": "soil_parameters\\storage_parameters\\permeability_horizontal_factor\\standard_deviation",
            "soilstdinitialvoidratio": "soil_parameters\\soil_classification_parameters\\initial_void_ratio\\standard_deviation",
            "soilstdpermeabilitystrainmodulus": "",
            "soilstdlimitstress": "",
            "soilstdcp": "soil_parameters\\koppejan_parameters\\primary_Cp\\standard_deviation",
            "soilstdcp1": "soil_parameters\\koppejan_parameters\\primary_Cp_point\\standard_deviation",
            "soilstdcs": "soil_parameters\\koppejan_parameters\\secular_Cs\\standard_deviation",
            "soilstdcs1": "soil_parameters\\koppejan_parameters\\secular_Cs_point\\standard_deviation",
            "soilstdap": "soil_parameters\\koppejan_parameters\\primary_Ap\\standard_deviation",
            "soilstdasec": "soil_parameters\\koppejan_parameters\\primary_Asec\\standard_deviation",
            "soilstdcar": "",
            "soilstdca": "soil_parameters\\bjerrum_parameters\\coef_secondary_compression_Ca\\standard_deviation",
            "soilstdrratio": "soil_parameters\\bjerrum_parameters\\reloading_swelling_RR\\standard_deviation",
            "soilstdcratio": "soil_parameters\\bjerrum_parameters\\compression_ratio_CR\\standard_deviation",
            "soilstdsratio": "",
            "soilstdcrindex": "soil_parameters\\bjerrum_parameters\\reloading_swelling_index_Cr\\standard_deviation",
            "soilstdccindex": "soil_parameters\\bjerrum_parameters\\compression_index_Cc\\standard_deviation",
            "soilstdcswindex": "",
            "soildistgamdry": "soil_parameters\\soil_weight_parameters\\unsaturated_weight\\distribution_type",
            "soildistgamwet": "soil_parameters\\soil_weight_parameters\\saturated_weight\\distribution_type",
            "soildistcv": "soil_parameters\\undrained_parameters\\vertical_consolidation_coefficient\\distribution_type",
            "soildistdpc": "soil_parameters\\koppejan_parameters\\preconsolidation_pressure\\distribution_type",
            "soildistpricompindex": "soil_parameters\\isotache_parameters\\reloading_swelling_constant_a\\distribution_type",
            "soildistseccompindex": "soil_parameters\\isotache_parameters\\primary_compression_constant_b\\distribution_type",
            "soildistseccomprate": "soil_parameters\\isotache_parameters\\secondary_compression_constant_c\\distribution_type",
            "soildistocr": "soil_parameters\\compression_parameters\\OCR\\distribution_type",
            "soildistpermeabilityver": "soil_parameters\\storage_parameters\\vertical_permeability\\distribution_type",
            "soildistpop": "soil_parameters\\compression_parameters\\POP\\distribution_type",
            "soildistpermeabilityhorfactor": "soil_parameters\\storage_parameters\\permeability_horizontal_factor\\distribution_type",
            "soildistinitialvoidratio": "soil_parameters\\soil_classification_parameters\\initial_void_ratio\\distribution_type",
            "soildistpermeabilitystrainmodulus": "soil_parameters\\storage_parameters\\permeability_strain_type",
            "soildistlimitstress": "",
            "soildistcp": "soil_parameters\\koppejan_parameters\\primary_Cp\\distribution_type",
            "soildistcp1": "soil_parameters\\koppejan_parameters\\primary_Cp_point\\distribution_type",
            "soildistcs": "soil_parameters\\koppejan_parameters\\secular_Cs\\distribution_type",
            "soildistcs1": "soil_parameters\\koppejan_parameters\\secular_Cs_point\\distribution_type",
            "soildistap": "soil_parameters\\koppejan_parameters\\primary_Ap\\distribution_type",
            "soildistasec": "soil_parameters\\koppejan_parameters\\primary_Asec\\distribution_type",
            "soildistcar": "",
            "soildistca": "soil_parameters\\bjerrum_parameters\\coef_secondary_compression_Ca\\distribution_type",
            "soildistrratio": "soil_parameters\\bjerrum_parameters\\reloading_swelling_RR\\distribution_type",
            "soildistcratio": "soil_parameters\\bjerrum_parameters\\compression_ratio_CR\\distribution_type",
            "soildistsratio": "",
            "soildistcrindex": "soil_parameters\\bjerrum_parameters\\reloading_swelling_index_Cr\\distribution_type",
            "soildistccindex": "soil_parameters\\bjerrum_parameters\\compression_index_Cc\\distribution_type",
            "soildistcswindex": "",
            "soilcorcpcp1": "soil_parameters\\koppejan_parameters\\primary_Cp\\correlation_coefficient",
            "soilcorcscp1": "soil_parameters\\koppejan_parameters\\secular_Cs\\correlation_coefficient",
            "soilcorcs1cp1": "soil_parameters\\koppejan_parameters\\secular_Cs_point\\correlation_coefficient",
            "soilcorapcp1": "soil_parameters\\koppejan_parameters\\primary_Ap\\correlation_coefficient",
            "soilcoraseccp1": "soil_parameters\\koppejan_parameters\\primary_Asec\\correlation_coefficient",
            "soilcorcrindexccindex": "soil_parameters\\bjerrum_parameters\\reloading_swelling_index_Cr\\correlation_coefficient",
            "soilcorrratiocratio": "soil_parameters\\bjerrum_parameters\\reloading_swelling_RR\\correlation_coefficient",
            "soilcorcaccindexorcratio": "soil_parameters\\bjerrum_parameters\\coef_secondary_compression_Ca\\correlation_coefficient",
            "soilcorpricompindexseccompindex": "soil_parameters\\isotache_parameters\\reloading_swelling_constant_a\\correlation_coefficient",
            "soilcorseccomprateseccompindex": "soil_parameters\\isotache_parameters\\secondary_compression_constant_c\\correlation_coefficient",
            "soilcp": "soil_parameters\\koppejan_parameters\\primary_Cp\\mean",
            "soilcp1": "soil_parameters\\koppejan_parameters\\primary_Cp_point\\mean",
            "soilcs": "soil_parameters\\koppejan_parameters\\secular_Cs\\mean",
            "soilcs1": "soil_parameters\\koppejan_parameters\\secular_Cs_point\\mean",
            "soilap": "soil_parameters\\koppejan_parameters\\primary_Ap\\mean",
            "soilasec": "soil_parameters\\koppejan_parameters\\primary_Asec\\mean",
            "soilcar": "",
            "soilca": "soil_parameters\\bjerrum_parameters\\coef_secondary_compression_Ca\\mean",
            "soilcompratio": "",
            "soilrratio": "soil_parameters\\bjerrum_parameters\\reloading_swelling_RR\\mean",
            "soilcratio": "soil_parameters\\bjerrum_parameters\\compression_ratio_CR\\mean",
            "soilsratio": "",
            "soilcrindex": "soil_parameters\\bjerrum_parameters\\reloading_swelling_index_Cr\\mean",
            "soilccindex": "soil_parameters\\bjerrum_parameters\\compression_index_Cc\\mean",
            "soilcswindexfixed": "",
            "soilpricompindex": "soil_parameters\\isotache_parameters\\reloading_swelling_constant_a\\mean",
            "soilseccompindex": "soil_parameters\\isotache_parameters\\primary_compression_constant_b\\mean",
            "soilseccomprate": "soil_parameters\\isotache_parameters\\secondary_compression_constant_c\\mean",
            "soilhorizontalbehaviourtype": "horizontal_behavior\\soil_elasticity",
            "soilelasticity": "horizontal_behavior\\soil_default_elasticity",
            "soildefaultelasticity": "soil_external\\horizontal_behavior\\soil_default_elasticity",
        }
        # EleniSmyrniou_2020: Initialise the class so that we can retrieve the default values,
        # if there is a beter way to do please refactor this code.
        converted_dict = {}
        default_class_values = dict(cls())
        external_dict = dict(soil_external)
        for internal_key, external_key in mapping_dictionary.items():
            default_value = default_class_values[internal_key]
            paths = external_key.split("\\")
            my_dict = external_dict
            for path in paths:
                if path != paths[-1]:
                    # check if the key exists or if it is initialised
                    if not (path in my_dict.keys()) or not (my_dict.get(path)):
                        converted_dict[internal_key] = default_value
                        break
                    my_dict = dict(my_dict.get(path))
                else:
                    converted_dict[internal_key] = my_dict.get(path, default_value)
        return cls(**converted_dict)
