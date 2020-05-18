from typing import Optional
from enum import Enum, IntEnum
from geolib.models.dseries_parser import DSeriesNameKeyValueSubStructure
from geolib.soils import Soil, DistributionType, HorizontalBehaviourType
from geolib.soils import PreconType
from geolib.soils import StorageTypes
from datetime import timedelta


class Bool(IntEnum):
    FALSE = 0
    TRUE = 1

    def __getattribute__(self, name):
        if isinstance(name, bool):
            if name:
                name = "TRUE"
            else:
                name = "FALSE"
        return super().__getattribute__(name)


class Soil_Internal(DSeriesNameKeyValueSubStructure):
    """Representation of [SOIL] group."""

    name: str = ""
    soilcolor: int = 9764853
    soilgamdry: float = 14
    soilgamwet: float = 14
    soilinitialvoidratio: float = 0
    soilcohesion: float = 10  # fixed value cannot be modified
    soilphi: float = 30  # fixed value cannot be modified
    soilpreconisotachetype: PreconType = PreconType.PreoverburdenPressure
    soilpreconkoppejantype: PreconType = PreconType.OverconsolidationRatio
    soiluseequivalentage: Bool = False
    soilequivalentage: float = 19800
    soilpc: float = 0
    soilocr: float = 1
    soilpop: float = 0
    soillimitstress: float = 0  # fixed value
    soildrained: Bool = False
    soilapasapproximationbycpcs: Bool = False
    soilcv: float = 1e-12
    soilpermeabilityver: float = 0.00000001
    soilpermeabilityhorfactor: float = 1
    soilstoragetype: StorageTypes = StorageTypes.strain_dependent_permeability
    soilpermeabilitystrainmodulus: float = 1e15
    soiluseprobdefaults: Bool = False
    soilstdgamdry: float = 0
    soilstdgamwet: float = 0
    soilstdcv: float = 0
    soilstdpc: float = 0
    soilstdpricompindex: float = 0.01  # SoilPriCompIndex
    soilstdseccompindex: float = 0.1  # SoilSecCompIndex
    soilstdseccomprate: float = 0.005  # SoilSecCompRate
    soilstdocr: float = 0
    soilstdpermeabilityver: float = 0
    soilstdpop: float = 0
    soilstdpermeabilityhorfactor: float = 0
    soilstdinitialvoidratio: float = 0
    soilstdpermeabilitystrainmodulus: float = 0  # fixed value
    soilstdlimitstress: float = 0  # fixed value
    soilstdcp: float = 0
    soilstdcp1: float = 0
    soilstdcs: float = 0
    soilstdcs1: float = 0
    soilstdap: float = 0
    soilstdasec: float = 0
    soilstdcar: float = 0
    soilstdca: float = 0
    soilstdrratio: float = 0
    soilstdcratio: float = 0
    soilstdsratio: float = 0  # fixed value
    soilstdcrindex: float = 0
    soilstdccindex: float = 0
    soilstdcswindex: float = 0  # fixed value
    soildistgamdry: DistributionType = DistributionType.Normal
    soildistgamwet: DistributionType = DistributionType.Normal
    soildistcv: DistributionType = DistributionType.Normal
    soildistdpc: DistributionType = DistributionType.Normal
    soildistpricompindex: DistributionType = DistributionType.Normal
    soildistseccompindex: DistributionType = DistributionType.Normal
    soildistseccomprate: DistributionType = DistributionType.Normal
    soildistocr: DistributionType = DistributionType.Normal
    soildistpermeabilityver: DistributionType = DistributionType.Normal
    soildistpop: DistributionType = DistributionType.Normal
    soildistpermeabilityhorfactor: DistributionType = DistributionType.Normal
    soildistinitialvoidratio: DistributionType = DistributionType.Normal
    soildistpermeabilitystrainmodulus: DistributionType = DistributionType.Normal  # fixed value
    soildistlimitstress: DistributionType = DistributionType.Normal  # fixed value
    soildistcp: DistributionType = DistributionType.Normal
    soildistcp1: DistributionType = DistributionType.Normal
    soildistcs: DistributionType = DistributionType.Normal
    soildistcs1: DistributionType = DistributionType.Normal
    soildistap: DistributionType = DistributionType.Normal
    soildistasec: DistributionType = DistributionType.Normal
    soildistcar: DistributionType = DistributionType.Normal
    soildistca: DistributionType = DistributionType.Normal
    soildistrratio: DistributionType = DistributionType.Normal
    soildistcratio: DistributionType = DistributionType.Normal
    soildistsratio: DistributionType = DistributionType.Normal  # fixed value
    soildistcrindex: DistributionType = DistributionType.Normal
    soildistccindex: DistributionType = DistributionType.Normal
    soildistcswindex: DistributionType = DistributionType.Normal  # fixed value
    soilcorcpcp1: float = 0
    soilcorcscp1: float = 0
    soilcorcs1cp1: float = 0
    soilcorapcp1: float = 0
    soilcoraseccp1: float = 0
    soilcorcrindexccindex: float = 0
    soilcorrratiocratio: float = 0
    soilcorcaccindexorcratio: float = 0
    soilcorpricompindexseccompindex: float = 0  # SoilPriCompIndex
    soilcorseccomprateseccompindex: float = 0  # SoilSecCompRate
    soilcp: float = 1
    soilcp1: float = 1
    soilcs: float = 1
    soilcs1: float = 1
    soilap: float = 1
    soilasec: float = 1
    soilcar: float = 10
    soilca: float = 1
    soilcompratio: float = 0  # fixed value
    soilrratio: float = 1
    soilcratio: float = 1
    soilsratio: float = 0  # fixed value
    soilcrindex: float = 1
    soilccindex: float = 1
    soilcswindexfixed: float = 0  # fixed value
    soilpricompindex: float = 0.01  # SoilPriCompIndex
    soilseccompindex: float = 0.1  # SoilSecCompIndex
    soilseccomprate: float = 0.005  # SoilSecCompRate
    soilhorizontalbehaviourtype: HorizontalBehaviourType = HorizontalBehaviourType.Elastic
    soilelasticity: float = 1000
    soildefaultelasticity: Bool = True

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
                    value = my_dict.get(path, default_value)
                    if value is None:
                        value = default_value
                    converted_dict[internal_key] = value
        return cls(**converted_dict)
