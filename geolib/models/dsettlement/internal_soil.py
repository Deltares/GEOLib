from enum import Enum, IntEnum
from typing import Optional

from geolib.models.dseries_parser import DSeriesUnmappedNameProperties
from geolib.models.internal import Bool
from geolib.soils import DistributionType, HorizontalBehaviourType, StorageTypes


class PreconType(IntEnum):
    UNDEFINED = -1
    OCR = 0
    PRECONSOLIDATION_PRESSURE = 1
    POP = 2


class SoilInternal(DSeriesUnmappedNameProperties):
    """Representation of [SOIL] group."""

    name: str = ""
    soilcolor: int = 9764853
    soilgamdry: float = 14
    soilgamwet: float = 14
    soilinitialvoidratio: float = 0
    soilcohesion: float = 10  # fixed value cannot be modified
    soilphi: float = 30  # fixed value cannot be modified
    soilpreconisotachetype: PreconType = PreconType.POP
    soilpreconkoppejantype: PreconType = PreconType.OCR
    soiluseequivalentage: Bool = Bool.FALSE
    soilequivalentage: float = 19800
    soilpc: float = 0
    soilocr: float = 1
    soilpop: float = 0
    soillimitstress: float = 0  # fixed value
    soildrained: Bool = Bool.FALSE
    soilapasapproximationbycpcs: Bool = Bool.FALSE
    soilcv: float = 1e-12
    soilpermeabilityver: float = 0.00000001
    soilpermeabilityhorfactor: float = 1
    soilstoragetype: StorageTypes = StorageTypes.strain_dependent_permeability
    soilpermeabilitystrainmodulus: float = 1e15
    soiluseprobdefaults: Bool = Bool.FALSE
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
    soildistpermeabilitystrainmodulus: DistributionType = (
        DistributionType.Normal
    )  # fixed value
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
    soilcompratio: Bool = Bool.TRUE
    soilrratio: float = 1
    soilcratio: float = 1
    soilsratio: float = 0  # fixed value
    soilcrindex: float = 1
    soilccindex: float = 1
    soilcswindex: float = 0  # fixed value
    soilpricompindex: float = 0.01  # SoilPriCompIndex
    soilseccompindex: float = 0.1  # SoilSecCompIndex
    soilseccomprate: float = 0.005  # SoilSecCompRate
    soilhorizontalbehaviourtype: HorizontalBehaviourType = HorizontalBehaviourType.Elastic
    soilelasticity: float = 1000
    soildefaultelasticity: Bool = Bool.TRUE
