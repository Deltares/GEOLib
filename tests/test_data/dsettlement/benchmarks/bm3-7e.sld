Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 10/08/2023
TIME       : 07:52:55
FILENAME   : C:\Deltares\D-Settlement\Benchmarks\bm3-7e.sld
CREATED BY : D-Settlement version 23.2.1.41674
==========================    BEGINNING OF DATA     ==========================
[INPUT DATA]
[VERSION]
Soil=1011
Geometry=1002
D-Settlement=1011
[END OF VERSION]

[MODEL]
0 : Dimension = 1D
1 : Calculation type = Terzaghi
0 : Model = NEN - Koppejan
0 : Strain type = Linear
0 : Vertical drains = FALSE
0 : Fit for settlement plate = FALSE
0 : Probabilistic = FALSE
0 : Horizontal displacements = FALSE
0 : Secondary swelling = FALSE
[END OF MODEL]
[SOIL COLLECTION]
    1 = number of items
[SOIL]
Clay
SoilColor=9764853
SoilGamDry=15.00
SoilGamWet=18.00
SoilInitialVoidRatio=0.000000
SoilPreconIsotacheType=2
SoilPreconKoppejanType=1
SoilUseEquivalentAge=0
SoilEquivalentAge=0.00E+00
SoilPc=8.00E+00
SoilOCR=2.00
SoilPOP=7.72
SoilDrained=1
SoilApAsApproximationByCpCs=0
SoilSecondarySwellingReduced=0
SoilSecondarySwellingFactor=1.00
SoilUnloadingStressRatio=1.01
SoilCv=1.00E-09
SoilPermeabilityVer=1.000E+00
SoilPermeabilityHorFactor=3.000
SoilStorageType=1
SoilPermeabilityStrainModulus=1.000E+15
SoilUseProbDefaults=1
SoilStdGamDry=0.75
SoilStdGamWet=0.90
SoilStdCv=5.00E-10
SoilStdPc=2.00E+00
SoilStdPriCompIndex=2.497E-03
SoilStdSecCompIndex=2.497E-02
SoilStdSecCompRate=1.000E-03
SoilStdOCR=0.50
SoilStdPermeabilityVer=1.000E-01
SoilStdPOP=1.93
SoilStdPermeabilityHorFactor=0.750
SoilStdInitialVoidRatio=0.000000
SoilStdPermeabilityStrainModulus=0.000E+00
SoilStdLimitStress=0.00
SoilStdCp=1.50E+01
SoilStdCp1=3.75E+00
SoilStdCs=9.00E+01
SoilStdCs1=2.25E+01
SoilStdAp=9.00E+00
SoilStdAsec=4.50E+01
SoilStdCar=0.0000000
SoilStdCa=0.0000000
SoilStdRRatio=0.0000000
SoilStdCRatio=0.0000000
SoilStdSRatio=0.0000000
SoilStdCrIndex=0.0000000
SoilStdCcIndex=0.0000000
SoilStdCswIndex=0.0000000
SoilDistGamDry=2
SoilDistGamWet=2
SoilDistCv=2
SoilDistdPc=2
SoilDistPriCompIndex=2
SoilDistSecCompIndex=2
SoilDistSecCompRate=2
SoilDistOCR=2
SoilDistPermeabilityVer=2
SoilDistPOP=2
SoilDistPermeabilityHorFactor=2
SoilDistInitialVoidRatio=2
SoilDistPermeabilityStrainModulus=2
SoilDistLimitStress=2
SoilDistCp=2
SoilDistCp1=2
SoilDistCs=2
SoilDistCs1=2
SoilDistAp=2
SoilDistAsec=2
SoilDistCar=2
SoilDistCa=2
SoilDistRRatio=2
SoilDistCRatio=2
SoilDistSRatio=2
SoilDistCrIndex=2
SoilDistCcIndex=2
SoilDistCswIndex=2
SoilCorCpCp1=0.00
SoilCorCsCp1=0.00
SoilCorCs1Cp1=0.00
SoilCorApCp1=0.00
SoilCorASecCp1=0.00
SoilCorCrIndexCcIndex=0.00
SoilCorRRatioCRatio=0.00
SoilCorCaCcIndexOrCRatio=0.00
SoilCorPriCompIndexSecCompIndex=0.00
SoilCorSecCompRateSecCompIndex=0.00
SoilCp=5.00E+01
SoilCp1=1.25E+01
SoilCs=3.00E+02
SoilCs1=7.50E+01
SoilAp=3.00E+01
SoilAsec=1.50E+02
SoilCar=0.0000000
SoilCa=0.0000000
SoilCompRatio=1
SoilRRatio=0.0000000
SoilCRatio=0.0000000
SoilSRatio=0.0000000
SoilCrIndex=0.0000000
SoilCcIndex=0.0000000
SoilCswIndex=0.0000000
SoilPriCompIndex=9.989E-03
SoilSecCompIndex=9.989E-02
SoilSecCompRate=4.000E-03
SoilHorizontalBehaviourType=1
SoilElasticity=1.00000E+03
SoilDefaultElasticity=1
[END OF SOIL]
[END OF SOIL COLLECTION]
[GEOMETRY 1D DATA]
1
        0.000
Clay
5
        0.000
       -0.100
        0.000
        0.000
1
1
 0.00000000000000E+0000
 0.00000000000000E+0000
 1.00000000000000E+0000
[END OF GEOMETRY 1D DATA]
[RUN IDENTIFICATION]
Benchmark MSettle: bm3-7e
Pc compression
Variable within the layer and correction at t=0
[END OF RUN IDENTIFICATION]
[VERTICALS]
    1 = number of items
       0.000        0.000 = X, Z
[END OF VERTICALS]
[WATER]
       10.00 = Unit Weight of Water
[END OF WATER]
[NON-UNIFORM LOADS]
    0 = number of items
[END OF NON-UNIFORM LOADS]
[WATER LOADS]
    0 = number of items
[END OF WATER LOADS]
[OTHER LOADS]
   11 = number of items
Inital load top
3 : Uniform
          -1       100.00        0.050        0.000 = Time, Gamma, H, Yapplication
Inital load middle
3 : Uniform
          -1       100.00        0.050       -0.050 = Time, Gamma, H, Yapplication
Inital load bottom
3 : Uniform
          -1       100.00        0.050       -0.100 = Time, Gamma, H, Yapplication
1
3 : Uniform
           0       100.00        0.050        0.000 = Time, Gamma, H, Yapplication
2
3 : Uniform
           1      -100.00        0.050        0.000 = Time, Gamma, H, Yapplication
3
3 : Uniform
           2       100.00        0.050        0.000 = Time, Gamma, H, Yapplication
4
3 : Uniform
           3       100.00        0.050        0.000 = Time, Gamma, H, Yapplication
5
3 : Uniform
           4      -100.00        0.050        0.000 = Time, Gamma, H, Yapplication
6
3 : Uniform
           5       100.00        0.050        0.000 = Time, Gamma, H, Yapplication
7
3 : Uniform
           6       100.00        0.100        0.000 = Time, Gamma, H, Yapplication
8
3 : Uniform
           7       100.00        0.200        0.000 = Time, Gamma, H, Yapplication
[END OF OTHER LOADS]
[CALCULATION OPTIONS]
4 : Precon. pressure within a layer = Variable, correction at t=0 [days]
0 : Imaginary surface = FALSE
0 : Submerging = FALSE
0 : Use end time for fit = FALSE
0 : Maintain profile = FALSE
Superelevation
     0 = Time superelevation
    10.00 = Gamma dry superelevation
    10.00 = Gamma wet superelevation
1 : Dispersion conditions layer boundaries top = drained
1 : Dispersion conditions layer boundaries bottom = drained
0 : Stress distribution soil = Buisman
0 : Stress distribution loads = None
 0.10 = Iteration stop criteria submerging [m]
0.000 = Iteration stop criteria submerging minimum layer height [m]
1 = Maximum iteration steps for submerging
 0.10 = Iteration stop criteria desired profile [m]
    1.00 = Load column width imaginary surface [m]
    1.00 = Load column width non-uniform loads [m]
    1.00 = Load column width trapeziform loads [m]
8 = End of consolidation [days]
 1.00000000000000E+0000 = Number of subtime steps
4.000000000E+000 = Reference time
0 : Dissipation = FALSE
       0.000 = X co-ordinate dissipation
0 : Use fit factors = FALSE
       0.000 = X co-ordinate fit
0 : Predict settlements omitting additional loadsteps = FALSE
[END OF CALCULATION OPTIONS]
[RESIDUAL TIMES]
0 : Number of items
[END OF RESIDUAL TIMES]
[FILTER BAND WIDTH]
1 : Number of items
0.05
[END OF FILTER BAND WIDTH]
[VERTICAL DRAIN]
1 : Flow type = Plane
       0.000 = Bottom position
       0.000 = Position of the drain pipe
      -0.250 = Position of the leftmost drain
       0.250 = Position of the rightmost drain
       3.000 = Center to center distance
       0.200 = Diameter
       0.100 = Width
       0.003 = Thickness
2 = Grid
       0.000 = Begin time
       0.000 = End time
      35.000 = Under pressure for strips and columns
       0.000 = Under pressure for sand wall
       0.000 = Start of drainage
       0.040 = Phreatic level in drain
       0.000 = Water head during dewatering
    10.00 = Tube pressure during dewatering
2 : Flow type = Detailed input
1 = number of items
     0.000       40.000      0.000      0.00 = Time, Under pressure, Water level, Tube pressure
[END OF VERTICAL DRAIN]
[PROBABILISTIC DATA]
Reliability X Co-ordinate=0.000
Residual Settlement=1.00
Maximum Drawings=100
Maximum Iterations=15
Reliability Type=0
Is Reliability Calculation=0
[END OF PROBABILISTIC DATA]
[PROBABILISTIC DEFAULTS]
ProbDefGamDryVar=0.05
ProbDefGamWetVar=0.05
ProbDefPOPVar=0.25
ProbDefOCRVar=0.25
ProbDefPcVar=0.25
ProbDefPermeabilityVerVar=2.50
ProbDefRatioHorVerPermeabilityCvVar=0.25
ProbDefCvVar=0.50
ProbDefCpVar=0.30
ProbDefCp1Var=0.30
ProbDefCsVar=0.30
ProbDefCs1Var=0.30
ProbDefApVar=0.30
ProbDefASecVar=0.30
ProbDefRRCrVar=0.25
ProbDefCRCcVar=0.25
ProbDefCaVar=0.25
ProbDefPriCompIndexVar=0.25
ProbDefSecCompIndexVar=0.25
ProbDefSecCompRateVar=0.25
ProbDefCpCor=0.00
ProbDefCsCor=0.00
ProbDefCs1Cor=0.00
ProbDefApCor=0.00
ProbDefASecCor=0.00
ProbDefRRCrCor=0.00
ProbDefCaCor=0.00
ProbDefPriCompIndexCor=0.00
ProbDefSecCompRateCor=0.00
ProbDefGamDryDist=2
ProbDefGamWetDist=2
ProbDefPOPDist=2
ProbDefOCRDist=2
ProbDefPcDist=2
ProbDefPermeabilityVerDist=2
ProbDefRatioHorVerPermeabilityCvDist=2
ProbDefCvDist=2
ProbDefCpDist=2
ProbDefCp1Dist=2
ProbDefCsDist=2
ProbDefCs1Dist=2
ProbDefApDist=2
ProbDefASecDist=2
ProbDefRRCrDist=2
ProbDefCRCcDist=2
ProbDefCaDist=2
ProbDefPriCompIndexDist=2
ProbDefSecCompIndexDist=2
ProbDefSecCompRateDist=2
ProbDefLayerStd=0.10
ProbDefLayerDist=0
[END OF PROBABILISTIC DEFAULTS]
[FIT OPTIONS]
Fit Maximum Number of Iterations=5
Fit Required Iteration Accuracy=0.0001000000
Fit Required Correlation Coefficient=0.990
[END OF FIT OPTIONS]
[FIT CALCULATION]
Is Fit Calculation=0
Fit Vertical Number=-1
[END OF FIT CALCULATION]
[FIT]
    0 = number of items
[END OF FIT]
[END OF INPUT DATA]

[Results]
[CALCULATION SETTINGS]
IsSecondarySwellingUsed=0
[END OF CALCULATION SETTINGS]
[Verticals Count]
1
[End of Verticals Count]
[Vertical]
      1     =  Vertical count
   0.0000000     =  X co-ordinate
   0.0000000     =  Z co-ordinate
[Time-Settlement per Load]
     49  =  Time step count 
      8  =  Load step count 
   0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000   
   0.1000000      0.0033002      0.0033002      0.0033002      0.0033002      0.0033002      0.0033002      0.0033002      0.0033002   
   0.2050612      0.0033062      0.0033062      0.0033062      0.0033062      0.0033062      0.0033062      0.0033062      0.0033062   
   0.3387023      0.0033137      0.0033137      0.0033137      0.0033137      0.0033137      0.0033137      0.0033137      0.0033137   
   0.5086977      0.0033229      0.0033229      0.0033229      0.0033229      0.0033229      0.0033229      0.0033229      0.0033229   
   0.7249370      0.0033340      0.0033340      0.0033340      0.0033340      0.0033340      0.0033340      0.0033340      0.0033340   
   1.0000000      0.0033475      0.0033475      0.0033475      0.0033475      0.0033475      0.0033475      0.0033475      0.0033475   
   1.1000000      0.0033522      0.0019767      0.0019767      0.0019767      0.0019767      0.0019767      0.0019767      0.0019767   
   1.2050612      0.0033571      0.0019785      0.0019785      0.0019785      0.0019785      0.0019785      0.0019785      0.0019785   
   1.3387023      0.0033632      0.0019808      0.0019808      0.0019808      0.0019808      0.0019808      0.0019808      0.0019808   
   1.5086977      0.0033706      0.0019837      0.0019837      0.0019837      0.0019837      0.0019837      0.0019837      0.0019837   
   1.7249370      0.0033798      0.0019873      0.0019873      0.0019873      0.0019873      0.0019873      0.0019873      0.0019873   
   2.0000000      0.0033910      0.0019918      0.0019918      0.0019918      0.0019918      0.0019918      0.0019918      0.0019918   
   2.1000000      0.0033949      0.0019933      0.0052935      0.0052935      0.0052935      0.0052935      0.0052935      0.0052935   
   2.2050612      0.0033990      0.0019950      0.0053012      0.0053012      0.0053012      0.0053012      0.0053012      0.0053012   
   2.3387023      0.0034041      0.0019970      0.0053107      0.0053107      0.0053107      0.0053107      0.0053107      0.0053107   
   2.5086977      0.0034104      0.0019996      0.0053225      0.0053225      0.0053225      0.0053225      0.0053225      0.0053225   
   2.7249370      0.0034182      0.0020028      0.0053369      0.0053369      0.0053369      0.0053369      0.0053369      0.0053369   
   3.0000000      0.0034278      0.0020068      0.0053543      0.0053543      0.0053543      0.0053543      0.0053543      0.0053543   
   3.1000000      0.0034311      0.0020082      0.0053604      0.0076678      0.0076678      0.0076678      0.0076678      0.0076678   
   3.2050612      0.0034346      0.0020097      0.0053668      0.0076784      0.0076784      0.0076784      0.0076784      0.0076784   
   3.3387023      0.0034390      0.0020115      0.0053747      0.0076915      0.0076915      0.0076915      0.0076915      0.0076915   
   3.5086977      0.0034445      0.0020138      0.0053844      0.0077077      0.0077077      0.0077077      0.0077077      0.0077077   
   3.7249370      0.0034513      0.0020167      0.0053965      0.0077275      0.0077275      0.0077275      0.0077275      0.0077275   
   4.0000000      0.0034596      0.0020202      0.0054112      0.0077517      0.0077517      0.0077517      0.0077517      0.0077517   
   4.1000000      0.0034626      0.0020215      0.0054165      0.0077602      0.0067985      0.0067985      0.0067985      0.0067985   
   4.2050612      0.0034656      0.0020228      0.0054219      0.0077690      0.0068052      0.0068052      0.0068052      0.0068052   
   4.3387023      0.0034695      0.0020245      0.0054286      0.0077800      0.0068135      0.0068135      0.0068135      0.0068135   
   4.5086977      0.0034743      0.0020266      0.0054370      0.0077936      0.0068239      0.0068239      0.0068239      0.0068239   
   4.7249370      0.0034803      0.0020292      0.0054474      0.0078104      0.0068368      0.0068368      0.0068368      0.0068368   
   5.0000000      0.0034877      0.0020324      0.0054602      0.0078310      0.0068527      0.0068527      0.0068527      0.0068527   
   5.1000000      0.0034903      0.0020336      0.0054647      0.0078383      0.0068584      0.0091658      0.0091658      0.0091658   
   5.2050612      0.0034931      0.0020348      0.0054694      0.0078459      0.0068642      0.0091758      0.0091758      0.0091758   
   5.3387023      0.0034965      0.0020363      0.0054753      0.0078553      0.0068716      0.0091884      0.0091884      0.0091884   
   5.5086977      0.0035008      0.0020382      0.0054827      0.0078671      0.0068807      0.0092039      0.0092039      0.0092039   
   5.7249370      0.0035062      0.0020405      0.0054918      0.0078817      0.0068921      0.0092231      0.0092231      0.0092231   
   6.0000000      0.0035128      0.0020435      0.0055031      0.0078997      0.0069062      0.0092466      0.0092466      0.0092466   
   6.1000000      0.0035152      0.0020445      0.0055071      0.0079060      0.0069112      0.0092549      0.0124906      0.0124906   
   6.2050612      0.0035176      0.0020456      0.0055113      0.0079127      0.0069164      0.0092635      0.0125051      0.0125051   
   6.3387023      0.0035207      0.0020470      0.0055165      0.0079210      0.0069229      0.0092743      0.0125232      0.0125232   
   6.5086977      0.0035246      0.0020488      0.0055231      0.0079313      0.0069310      0.0092877      0.0125456      0.0125456   
   6.7249370      0.0035295      0.0020509      0.0055312      0.0079442      0.0069412      0.0093043      0.0125731      0.0125731   
   7.0000000      0.0035355      0.0020537      0.0055413      0.0079602      0.0069538      0.0093247      0.0126068      0.0126068   
   7.1000000      0.0035377      0.0020546      0.0055449      0.0079658      0.0069583      0.0093319      0.0126186      0.0166900   
   7.2050612      0.0035399      0.0020556      0.0055487      0.0079717      0.0069630      0.0093395      0.0126309      0.0167098   
   7.3387023      0.0035428      0.0020569      0.0055534      0.0079791      0.0069689      0.0093489      0.0126463      0.0167343   
   7.5086977      0.0035463      0.0020585      0.0055593      0.0079884      0.0069762      0.0093607      0.0126654      0.0167647   
   7.7249370      0.0035508      0.0020605      0.0055667      0.0080000      0.0069854      0.0093753      0.0126890      0.0168022   
   8.0000000      0.0035563      0.0020630      0.0055758      0.0080143      0.0069968      0.0093934      0.0127181      0.0168479   
[End of Time-Settlement per Load]
[Depths]
      3    =  Depth count
  -0.0000100
  -0.0500000
  -0.1000000
[End of Depths]
[Stresses]
[Column Indication]
Initial total stress
Initial water stress
Final pre consolidation stress
Final total stress
Final water stress
[End of Column Indication]
[Stress Data]
      3  =  Depth step count 
   5.0001800      0.0001000      7.7000400     45.1686588      0.1685788   
  10.9000000      0.5000000     13.1000000     50.9720811      0.5720811   
  16.8000000      1.0000000      0.0000000     56.8000000      1.0000000   
[End of Stress Data]
[End of Stresses]
[Koppejan settlement]
[Column Indication]
Layer number
Primary swelling
Secundary swelling
Primary settlement below pre cons. stress
Secondary settlement below pre cons. stress
Primary settlement above pre cons. stress
Secondary settlement above pre cons. stress
[End of Column Indication]
[Koppejan Settlement Data]
      1  =  Layer seperation count 
      1     -0.0023323     -0.0004665      0.0000000      0.0000000      0.0184892      0.0030815   
[End of Koppejan Settlement Data]
[End of Koppejan Settlement]
[Time-dependent Data]
[Column Indication]
Settlement
Loading
[End of Column Indication]
[Vertical Data at Time]
   0.000000000000    =  Time in days
   0.0000000    5.0000800
   0.0000000   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.100000000000    =  Time in days
   0.0033002   10.0000800
   0.0012955   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.205061218966    =  Time in days
   0.0033062   10.0000800
   0.0012979   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.338702261693    =  Time in days
   0.0033137   10.0000800
   0.0013008   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.508697703179    =  Time in days
   0.0033229   10.0000800
   0.0013044   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.724937037565    =  Time in days
   0.0033340   10.0000800
   0.0013088   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.000000000000    =  Time in days
   0.0033475   10.0000800
   0.0013141   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.100000000000    =  Time in days
   0.0019767    5.0000800
   0.0007760   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.205061218966    =  Time in days
   0.0019785    5.0000800
   0.0007767   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.338702261693    =  Time in days
   0.0019808    5.0000800
   0.0007776   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.508697703179    =  Time in days
   0.0019837    5.0000800
   0.0007787   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.724937037565    =  Time in days
   0.0019873    5.0000800
   0.0007801   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.000000000000    =  Time in days
   0.0019918    5.0000800
   0.0007819   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.100000000000    =  Time in days
   0.0052935   10.0000800
   0.0020780   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.205061218966    =  Time in days
   0.0053012   10.0000800
   0.0020810   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.338702261693    =  Time in days
   0.0053107   10.0000800
   0.0020848   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.508697703179    =  Time in days
   0.0053225   10.0000800
   0.0020894   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.724937037565    =  Time in days
   0.0053369   10.0000800
   0.0020950   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.000000000000    =  Time in days
   0.0053543   10.0000800
   0.0021019   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.100000000000    =  Time in days
   0.0076678   15.0000800
   0.0030817   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.205061218966    =  Time in days
   0.0076784   15.0000800
   0.0030860   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.338702261693    =  Time in days
   0.0076915   15.0000800
   0.0030913   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.508697703179    =  Time in days
   0.0077077   15.0000800
   0.0030978   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.724937037565    =  Time in days
   0.0077275   15.0000800
   0.0031059   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.000000000000    =  Time in days
   0.0077517   15.0000800
   0.0031157   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.100000000000    =  Time in days
   0.0067985   10.0000800
   0.0027117   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.205061218966    =  Time in days
   0.0068052   10.0000800
   0.0027144   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.338702261693    =  Time in days
   0.0068135   10.0000800
   0.0027177   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.508697703179    =  Time in days
   0.0068239   10.0000800
   0.0027218   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.724937037565    =  Time in days
   0.0068368   10.0000800
   0.0027270   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.000000000000    =  Time in days
   0.0068527   10.0000800
   0.0027333   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.100000000000    =  Time in days
   0.0091658   15.0000800
   0.0037130   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.205061218966    =  Time in days
   0.0091758   15.0000800
   0.0037171   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.338702261693    =  Time in days
   0.0091884   15.0000800
   0.0037222   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.508697703179    =  Time in days
   0.0092039   15.0000800
   0.0037286   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.724937037565    =  Time in days
   0.0092231   15.0000800
   0.0037365   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.000000000000    =  Time in days
   0.0092466   15.0000800
   0.0037461   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.100000000000    =  Time in days
   0.0124906   25.0000800
   0.0051908   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.205061218966    =  Time in days
   0.0125051   25.0000800
   0.0051970   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.338702261693    =  Time in days
   0.0125232   25.0000800
   0.0052046   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.508697703179    =  Time in days
   0.0125456   25.0000800
   0.0052141   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.724937037565    =  Time in days
   0.0125731   25.0000800
   0.0052257   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.000000000000    =  Time in days
   0.0126068   25.0000800
   0.0052400   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.100000000000    =  Time in days
   0.0166900   45.0000800
   0.0071390   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.205061218966    =  Time in days
   0.0167098   45.0000800
   0.0071476   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.338702261693    =  Time in days
   0.0167343   45.0000800
   0.0071584   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.508697703179    =  Time in days
   0.0167647   45.0000800
   0.0071717   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.724937037565    =  Time in days
   0.0168022   45.0000800
   0.0071881   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   8.000000000000    =  Time in days
   0.0168479   45.0000800
   0.0072081   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[End of Time dependent Data]
[Time-dependent Data]
[Column Indication]
Depth
Settlement
[End of Column Indication]
[Vertical Data at Fixed Time]
   0.001000000000    =  Time in days
  -0.0000100    0.0000330
  -0.0050095    0.0000310
  -0.0100090    0.0000290
  -0.0150085    0.0000270
  -0.0200080    0.0000250
  -0.0250075    0.0000230
  -0.0300070    0.0000210
  -0.0350065    0.0000190
  -0.0400060    0.0000170
  -0.0450055    0.0000150
  -0.0500050    0.0000130
  -0.0550045    0.0000117
  -0.0600040    0.0000104
  -0.0650035    0.0000091
  -0.0700030    0.0000078
  -0.0750025    0.0000065
  -0.0800020    0.0000052
  -0.0850015    0.0000039
  -0.0900010    0.0000026
  -0.0950005    0.0000013
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000660
  -0.0050095    0.0000620
  -0.0100090    0.0000580
  -0.0150085    0.0000540
  -0.0200080    0.0000500
  -0.0250075    0.0000460
  -0.0300070    0.0000419
  -0.0350065    0.0000379
  -0.0400060    0.0000339
  -0.0450055    0.0000299
  -0.0500050    0.0000259
  -0.0550045    0.0000233
  -0.0600040    0.0000207
  -0.0650035    0.0000181
  -0.0700030    0.0000155
  -0.0750025    0.0000130
  -0.0800020    0.0000104
  -0.0850015    0.0000078
  -0.0900010    0.0000052
  -0.0950005    0.0000026
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0001650
  -0.0050095    0.0001550
  -0.0100090    0.0001450
  -0.0150085    0.0001349
  -0.0200080    0.0001249
  -0.0250075    0.0001149
  -0.0300070    0.0001049
  -0.0350065    0.0000948
  -0.0400060    0.0000848
  -0.0450055    0.0000748
  -0.0500050    0.0000648
  -0.0550045    0.0000583
  -0.0600040    0.0000518
  -0.0650035    0.0000453
  -0.0700030    0.0000389
  -0.0750025    0.0000324
  -0.0800020    0.0000259
  -0.0850015    0.0000194
  -0.0900010    0.0000130
  -0.0950005    0.0000065
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0003300
  -0.0050095    0.0003100
  -0.0100090    0.0002899
  -0.0150085    0.0002699
  -0.0200080    0.0002498
  -0.0250075    0.0002298
  -0.0300070    0.0002097
  -0.0350065    0.0001897
  -0.0400060    0.0001696
  -0.0450055    0.0001496
  -0.0500050    0.0001295
  -0.0550045    0.0001166
  -0.0600040    0.0001036
  -0.0650035    0.0000907
  -0.0700030    0.0000777
  -0.0750025    0.0000648
  -0.0800020    0.0000518
  -0.0850015    0.0000389
  -0.0900010    0.0000259
  -0.0950005    0.0000130
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
  -0.0000100    0.0006600
  -0.0050095    0.0006199
  -0.0100090    0.0005798
  -0.0150085    0.0005397
  -0.0200080    0.0004996
  -0.0250075    0.0004596
  -0.0300070    0.0004195
  -0.0350065    0.0003794
  -0.0400060    0.0003393
  -0.0450055    0.0002992
  -0.0500050    0.0002591
  -0.0550045    0.0002332
  -0.0600040    0.0002073
  -0.0650035    0.0001814
  -0.0700030    0.0001554
  -0.0750025    0.0001295
  -0.0800020    0.0001036
  -0.0850015    0.0000777
  -0.0900010    0.0000518
  -0.0950005    0.0000259
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
  -0.0000100    0.0016501
  -0.0050095    0.0015499
  -0.0100090    0.0014496
  -0.0150085    0.0013494
  -0.0200080    0.0012491
  -0.0250075    0.0011489
  -0.0300070    0.0010486
  -0.0350065    0.0009484
  -0.0400060    0.0008481
  -0.0450055    0.0007479
  -0.0500050    0.0006477
  -0.0550045    0.0005829
  -0.0600040    0.0005182
  -0.0650035    0.0004534
  -0.0700030    0.0003886
  -0.0750025    0.0003238
  -0.0800020    0.0002591
  -0.0850015    0.0001943
  -0.0900010    0.0001295
  -0.0950005    0.0000648
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0033002
  -0.0050095    0.0030997
  -0.0100090    0.0028992
  -0.0150085    0.0026987
  -0.0200080    0.0024982
  -0.0250075    0.0022978
  -0.0300070    0.0020973
  -0.0350065    0.0018968
  -0.0400060    0.0016963
  -0.0450055    0.0014958
  -0.0500050    0.0012954
  -0.0550045    0.0011658
  -0.0600040    0.0010363
  -0.0650035    0.0009068
  -0.0700030    0.0007772
  -0.0750025    0.0006477
  -0.0800020    0.0005182
  -0.0850015    0.0003886
  -0.0900010    0.0002591
  -0.0950005    0.0001295
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0033060
  -0.0050095    0.0031052
  -0.0100090    0.0029043
  -0.0150085    0.0027035
  -0.0200080    0.0025027
  -0.0250075    0.0023018
  -0.0300070    0.0021010
  -0.0350065    0.0019001
  -0.0400060    0.0016993
  -0.0450055    0.0014984
  -0.0500050    0.0012977
  -0.0550045    0.0011679
  -0.0600040    0.0010381
  -0.0650035    0.0009084
  -0.0700030    0.0007786
  -0.0750025    0.0006488
  -0.0800020    0.0005191
  -0.0850015    0.0003893
  -0.0900010    0.0002595
  -0.0950005    0.0001298
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0033225
  -0.0050095    0.0031206
  -0.0100090    0.0029188
  -0.0150085    0.0027169
  -0.0200080    0.0025151
  -0.0250075    0.0023133
  -0.0300070    0.0021114
  -0.0350065    0.0019096
  -0.0400060    0.0017077
  -0.0450055    0.0015059
  -0.0500050    0.0013041
  -0.0550045    0.0011737
  -0.0600040    0.0010433
  -0.0650035    0.0009129
  -0.0700030    0.0007825
  -0.0750025    0.0006521
  -0.0800020    0.0005216
  -0.0850015    0.0003912
  -0.0900010    0.0002608
  -0.0950005    0.0001304
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0033475
  -0.0050095    0.0031442
  -0.0100090    0.0029408
  -0.0150085    0.0027374
  -0.0200080    0.0025341
  -0.0250075    0.0023307
  -0.0300070    0.0021273
  -0.0350065    0.0019240
  -0.0400060    0.0017206
  -0.0450055    0.0015172
  -0.0500050    0.0013140
  -0.0550045    0.0011826
  -0.0600040    0.0010512
  -0.0650035    0.0009198
  -0.0700030    0.0007884
  -0.0750025    0.0006570
  -0.0800020    0.0005256
  -0.0850015    0.0003942
  -0.0900010    0.0002628
  -0.0950005    0.0001314
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100    0.0019918
  -0.0050095    0.0018708
  -0.0100090    0.0017498
  -0.0150085    0.0016288
  -0.0200080    0.0015078
  -0.0250075    0.0013868
  -0.0300070    0.0012658
  -0.0350065    0.0011448
  -0.0400060    0.0010238
  -0.0450055    0.0009028
  -0.0500050    0.0007818
  -0.0550045    0.0007036
  -0.0600040    0.0006254
  -0.0650035    0.0005473
  -0.0700030    0.0004691
  -0.0750025    0.0003909
  -0.0800020    0.0003127
  -0.0850015    0.0002345
  -0.0900010    0.0001564
  -0.0950005    0.0000782
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0068527
  -0.0050095    0.0064408
  -0.0100090    0.0060288
  -0.0150085    0.0056168
  -0.0200080    0.0052048
  -0.0250075    0.0047928
  -0.0300070    0.0043808
  -0.0350065    0.0039689
  -0.0400060    0.0035569
  -0.0450055    0.0031449
  -0.0500050    0.0027330
  -0.0550045    0.0024597
  -0.0600040    0.0021864
  -0.0650035    0.0019131
  -0.0700030    0.0016398
  -0.0750025    0.0013665
  -0.0800020    0.0010932
  -0.0850015    0.0008199
  -0.0900010    0.0005466
  -0.0950005    0.0002733
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0168479
  -0.0050095    0.0158838
  -0.0100090    0.0149197
  -0.0150085    0.0139557
  -0.0200080    0.0129916
  -0.0250075    0.0120275
  -0.0300070    0.0110634
  -0.0350065    0.0100994
  -0.0400060    0.0091353
  -0.0450055    0.0081712
  -0.0500050    0.0072074
  -0.0550045    0.0064867
  -0.0600040    0.0057659
  -0.0650035    0.0050452
  -0.0700030    0.0043244
  -0.0750025    0.0036037
  -0.0800020    0.0028830
  -0.0850015    0.0021622
  -0.0900010    0.0014415
  -0.0950005    0.0007207
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[End of Vertical]
[RESIDUAL SETTLEMENTS]
[Column Indication]
Vertical
Time
Settlement
Part of final settlement
Residual settlement
[End of Column Indication]
[DATA COUNT]
      0 Data count
[END OF DATA COUNT]
[RESIDUAL SETTLEMENT DATA]
[END OF RESIDUAL SETTLEMENT DATA]
[END OF RESIDUAL SETTLEMENTS]
[End of Results]
