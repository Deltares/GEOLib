from geolib.models import BaseDataClass
from geolib.models.dseries_parser import DSeriesInlineMappedProperties


class PartialFactorsEurocodeDa1Set1(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 1.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    effectfactor: float = 1.35
    effectfactorvarunfav: float = 1.111
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.000
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    overallstabilityfactorcohesion: float = 1.00
    overallstabilityfactortgphi: float = 1.00
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.00


class PartialFactorsEurocodeDa1Set2(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.30
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 1.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.25
    materialfactortgphi: float = 1.250
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    overallstabilityfactorcohesion: float = 1.25
    overallstabilityfactortgphi: float = 1.25
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.30


class PartialFactorsEurocodeDa2(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 1.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    effectfactor: float = 1.35
    effectfactorvarunfav: float = 1.111
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.000
    resistancefactor: float = 1.40
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    overallstabilityfactorcohesion: float = 1.00
    overallstabilityfactortgphi: float = 1.00
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.10


class PartialFactorsEurocodeDa3(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.30
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 0.00
    constructloadfactorpermunfav: float = 1.35
    constructloadfactorvarunfav: float = 1.50
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.25
    materialfactortgphi: float = 1.250
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    overallstabilityfactorcohesion: float = 1.25
    overallstabilityfactortgphi: float = 1.25
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.00


class PartialFactorsEc7Nl0(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 0.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.050
    materialfactorsubgradereaction: float = 1.30
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometrydeltapassivephreaticline: float = 0.15
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactorcohesion: float = 1.30
    overallstabilityfactortgphi: float = 1.20
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 1.20
    verticalbalancegammamb: float = 1.20


class PartialFactorsEc7Nl1(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 0.90
    constructloadfactorvarfav: float = 0.00
    constructloadfactorpermunfav: float = 1.215
    constructloadfactorvarunfav: float = 1.35
    materialfactorcohesion: float = 1.15
    materialfactortgphi: float = 1.150
    materialfactorsubgradereaction: float = 1.30
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometrydeltapassivephreaticline: float = 0.20
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactorcohesion: float = 1.30
    overallstabilityfactortgphi: float = 1.20
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 1.20
    verticalbalancegammamb: float = 1.20


class PartialFactorsEc7Nl2(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.10
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 0.90
    constructloadfactorvarfav: float = 0.00
    constructloadfactorpermunfav: float = 1.35
    constructloadfactorvarunfav: float = 1.50
    materialfactorcohesion: float = 1.25
    materialfactortgphi: float = 1.175
    materialfactorsubgradereaction: float = 1.30
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometrydeltapassivephreaticline: float = 0.25
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactorcohesion: float = 1.45
    overallstabilityfactortgphi: float = 1.25
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 1.20
    verticalbalancegammamb: float = 1.20


class PartialFactorsEc7Nl3(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.25
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 0.90
    constructloadfactorvarfav: float = 0.00
    constructloadfactorpermunfav: float = 1.485
    constructloadfactorvarunfav: float = 1.65
    materialfactorcohesion: float = 1.40
    materialfactortgphi: float = 1.200
    materialfactorsubgradereaction: float = 1.30
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometrydeltapassivephreaticline: float = 0.25
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactorcohesion: float = 1.60
    overallstabilityfactortgphi: float = 1.30
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 1.35
    verticalbalancegammamb: float = 1.20


class PartialFactorsEc7BE1Set1(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    effectfactor: float = 1.2
    effectfactorvarunfav: float = 1.083
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.000
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryincretainingheightdry: float = 0.00
    overallstabilityfactorcohesion: float = 1.00
    overallstabilityfactortgphi: float = 1.00
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.00


class PartialFactorsEc7BE1Set2(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.10
    loadfactorvarfav: float = 0.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.10
    materialfactortgphi: float = 1.10
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometryincretainingheightdry: float = 0.30
    overallstabilityfactorcohesion: float = 1.10
    overallstabilityfactortgphi: float = 1.10
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.30


class PartialFactorsEc7BE2Set1(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    effectfactor: float = 1.35
    effectfactorvarunfav: float = 1.111
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.000
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryincretainingheightdry: float = 0.00
    overallstabilityfactorcohesion: float = 1.00
    overallstabilityfactortgphi: float = 1.00
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.00


class PartialFactorsEc7BE2Set2(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.10
    loadfactorvarfav: float = 0.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.25
    materialfactortgphi: float = 1.25
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometryincretainingheightdry: float = 0.30
    overallstabilityfactorcohesion: float = 1.25
    overallstabilityfactortgphi: float = 1.25
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.30


class PartialFactorsEc7BE3Set1(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    effectfactor: float = 1.50
    effectfactorvarunfav: float = 1.20
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.000
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryincretainingheightdry: float = 0.00
    overallstabilityfactorcohesion: float = 1.00
    overallstabilityfactortgphi: float = 1.00
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.00


class PartialFactorsEc7BE3Set2(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.20
    loadfactorvarfav: float = 0.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.40
    materialfactortgphi: float = 1.40
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 10.00
    geometrymaxincretainingheight: float = 0.50
    geometryincretainingheightdry: float = 0.30
    overallstabilityfactorcohesion: float = 1.40
    overallstabilityfactortgphi: float = 1.40
    overallstabilityfactorunitweight: float = 1.00
    verticalbalancegammamb: float = 1.30


class PartialFactorsCrowB1C0(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.150
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 1.500
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.330
    combiloadfactorvarunfav: float = 0.800
    combiloadfactorvarunfavwaterlevel: float = -0.300
    combiloadfactorconstructvarunfav: float = 0.700
    materialfactorcohesion: float = 1.070
    materialfactortgphi: float = 1.110
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.20
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.070
    overallstabilityfactortgphi: float = 1.110
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB1C1(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.200
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 2.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.400
    combiloadfactorvarunfav: float = 0.800
    combiloadfactorvarunfavwaterlevel: float = -0.200
    combiloadfactorconstructvarunfav: float = 0.650
    materialfactorcohesion: float = 1.140
    materialfactortgphi: float = 1.160
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.30
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.140
    overallstabilityfactortgphi: float = 1.160
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB1C2(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.220
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 2.500
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.500
    combiloadfactorvarunfav: float = 0.800
    combiloadfactorvarunfavwaterlevel: float = -0.100
    combiloadfactorconstructvarunfav: float = 0.650
    materialfactorcohesion: float = 1.230
    materialfactortgphi: float = 1.220
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.40
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.230
    overallstabilityfactortgphi: float = 1.220
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB1C3(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.260
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 3.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.600
    combiloadfactorvarunfav: float = 0.750
    combiloadfactorvarunfavwaterlevel: float = -0.050
    combiloadfactorconstructvarunfav: float = 0.600
    materialfactorcohesion: float = 1.310
    materialfactortgphi: float = 1.280
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.50
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.310
    overallstabilityfactortgphi: float = 1.280
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB2C0(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.120
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 1.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.200
    combiloadfactorvarunfav: float = 0.800
    combiloadfactorvarunfavwaterlevel: float = -0.500
    combiloadfactorconstructvarunfav: float = 0.750
    materialfactorcohesion: float = 1.000
    materialfactortgphi: float = 1.000
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.20
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB2C1(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.170
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 1.500
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.300
    combiloadfactorvarunfav: float = 0.800
    combiloadfactorvarunfavwaterlevel: float = -0.300
    combiloadfactorconstructvarunfav: float = 0.700
    materialfactorcohesion: float = 1.050
    materialfactortgphi: float = 1.040
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.30
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB2C2(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.220
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 2.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.400
    combiloadfactorvarunfav: float = 0.750
    combiloadfactorvarunfavwaterlevel: float = -0.200
    combiloadfactorconstructvarunfav: float = 0.700
    materialfactorcohesion: float = 1.180
    materialfactortgphi: float = 1.100
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.40
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB2C3(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.280
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 2.500
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.550
    combiloadfactorvarunfav: float = 0.750
    combiloadfactorvarunfavwaterlevel: float = -0.100
    combiloadfactorconstructvarunfav: float = 0.630
    materialfactorcohesion: float = 1.320
    materialfactortgphi: float = 1.170
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 10.00
    geometryminincretainingheight: float = 0.20
    geometrymaxincretainingheight: float = 0.50
    geometryfixedretainingheight: float = 0.20
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.000
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB3C0(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.000
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 0.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.000
    combiloadfactorvarunfav: float = 0.850
    combiloadfactorvarunfavwaterlevel: float = -0.700
    combiloadfactorconstructvarunfav: float = 0.850
    materialfactorcohesion: float = 1.000
    materialfactortgphi: float = 1.000
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 0.00
    geometryminincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryfixedretainingheight: float = 0.00
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.120
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB3C1(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.000
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 0.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.000
    combiloadfactorvarunfav: float = 0.850
    combiloadfactorvarunfavwaterlevel: float = -0.700
    combiloadfactorconstructvarunfav: float = 0.850
    materialfactorcohesion: float = 1.000
    materialfactortgphi: float = 1.000
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 0.00
    geometryminincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryfixedretainingheight: float = 0.00
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.210
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB3C2(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.000
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 0.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.000
    combiloadfactorvarunfav: float = 0.850
    combiloadfactorvarunfavwaterlevel: float = -0.700
    combiloadfactorconstructvarunfav: float = 0.850
    materialfactorcohesion: float = 1.000
    materialfactortgphi: float = 1.000
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 0.00
    geometryminincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryfixedretainingheight: float = 0.00
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.310
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCrowB3C3(DSeriesInlineMappedProperties):
    loadfactorvarunfav: float = 1.000
    loadfactorvarfav: float = 0.000
    loadfactorvarunfavwaterlevel: float = 0.000
    loadfactorperm: float = 1.000
    constructloadfactorvarunfav: float = 1.000
    combiloadfactorvarunfav: float = 0.850
    combiloadfactorvarunfavwaterlevel: float = -0.700
    combiloadfactorconstructvarunfav: float = 0.850
    materialfactorcohesion: float = 1.000
    materialfactortgphi: float = 1.000
    materialfactorunitweight: float = 1.000
    geometryincretainingheight: float = 0.00
    geometryminincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryfixedretainingheight: float = 0.00
    overallstabilityfactorcohesion: float = 1.000
    overallstabilityfactortgphi: float = 1.000
    overallstabilityfactorunitweight: float = 1.000
    factorrepvaluesmdplasticrotation: float = 1.430
    verticalbalancegammamb: float = 1.200
    modelfactoranchorforce: float = 1.150


class PartialFactorsCurI(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 1.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.050
    materialfactorsubgradereaction: float = 1.30
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryincretainingheightdry: float = 0.00
    geometrydeltapassivesurfacelevel: float = 0.20
    geometrydeltapassivephreaticline: float = 0.15
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactordrivingmoment: float = 0.90
    overallstabilityfactorcohesion: float = 1.50
    overallstabilityfactortgphi: float = 1.20
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 0.00
    verticalbalancegammamb: float = 1.25


class PartialFactorsCurIi(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.00
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 1.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.00
    materialfactortgphi: float = 1.150
    materialfactorsubgradereaction: float = 1.30
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryincretainingheightdry: float = 0.00
    geometrydeltapassivesurfacelevel: float = 0.30
    geometrydeltapassivephreaticline: float = 0.20
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactordrivingmoment: float = 1.00
    overallstabilityfactorcohesion: float = 1.50
    overallstabilityfactortgphi: float = 1.20
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 0.00
    verticalbalancegammamb: float = 1.25


class PartialFactorsCurIii(DSeriesInlineMappedProperties):
    loadfactorpermunfav: float = 1.00
    loadfactorpermfav: float = 1.00
    loadfactorvarunfav: float = 1.25
    loadfactorvarfav: float = 0.00
    constructloadfactorpermfav: float = 1.00
    constructloadfactorvarfav: float = 1.00
    constructloadfactorpermunfav: float = 1.00
    constructloadfactorvarunfav: float = 1.00
    effectfactor: float = 1.00
    effectfactorvarunfav: float = 1.00
    materialfactorcohesion: float = 1.10
    materialfactortgphi: float = 1.200
    materialfactorsubgradereaction: float = 1.30
    resistancefactor: float = 1.00
    geometryincretainingheight: float = 0.00
    geometrymaxincretainingheight: float = 0.00
    geometryincretainingheightdry: float = 0.00
    geometrydeltapassivesurfacelevel: float = 0.35
    geometrydeltapassivephreaticline: float = 0.25
    geometrydeltaactivephreaticline: float = 0.05
    overallstabilityfactordrivingmoment: float = 1.10
    overallstabilityfactorcohesion: float = 1.50
    overallstabilityfactortgphi: float = 1.20
    overallstabilityfactorunitweight: float = 1.00
    factorrepvaluesmdpmax: float = 0.00
    verticalbalancegammamb: float = 1.25

