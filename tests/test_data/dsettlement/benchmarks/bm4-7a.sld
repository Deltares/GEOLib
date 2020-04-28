Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 8-3-2019
TIME       : 16:05:19
FILENAME   : D:\DSettlement\Test Results DSettlement\Benchmarks Branch\bm4-7a.sld
CREATED BY : D-Settlement version 19.1.1.23743
==========================    BEGINNING OF DATA     ==========================
[Input Data]
[VERSION]
Soil=1005
Geometry=1000
D-Settlement=1007
[END OF VERSION]

[SOIL COLLECTION]
    1 = number of items
[SOIL]
Sample
SoilColor=16575398
SoilGamDry=14.00
SoilGamWet=14.00
SoilInitialVoidRatio=0.000000
SoilCohesion=0.00
SoilPhi=0.00
SoilPreconIsotacheType=1
SoilPreconKoppejanType=1
SoilUseEquivalentAge=0
SoilEquivalentAge=0.00E+00
SoilPc=1.00E+01
SoilOCR=1.30
SoilPOP=10.00
SoilLimitStress=1.00
SoilDrained=0
SoilApAsApproximationByCpCs=1
SoilCv=6.00E-08
SoilPermeabilityVer=5.000E-02
SoilPermeabilityHorFactor=3.000
SoilStorageType=0
SoilPermeabilityStrainModulus=1.000E+15
SoilUseProbDefaults=1
SoilStdGamDry=0.70
SoilStdGamWet=0.70
SoilStdCv=3.00E-08
SoilStdPc=2.50E+00
SoilStdPriCompIndex=1.500E-02
SoilStdSecCompIndex=5.000E-02
SoilStdSecCompRate=1.250E-02
SoilStdOCR=0.33
SoilStdPermeabilityVer=1.000E-01
SoilStdPOP=2.50
SoilStdPermeabilityHorFactor=0.750
SoilStdInitialVoidRatio=0.000000
SoilStdPermeabilityStrainModulus=0.000E+00
SoilStdLimitStress=0.00
SoilStdCp=9.00E+00
SoilStdCp1=3.00E+00
SoilStdCs=1.80E+01
SoilStdCs1=9.00E+00
SoilStdAp=9.00E+00
SoilStdAsec=9.00E+00
SoilStdCar=0.0000000
SoilStdCa=0.2500000
SoilStdRRatio=0.2500000
SoilStdCRatio=0.2500000
SoilStdSRatio=0.0000000
SoilStdCrIndex=0.2500000
SoilStdCcIndex=0.2500000
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
SoilCorCpCp1=0.01
SoilCorCsCp1=0.01
SoilCorCs1Cp1=0.01
SoilCorApCp1=0.01
SoilCorASecCp1=0.01
SoilCorCrIndexCcIndex=0.01
SoilCorRRatioCRatio=0.01
SoilCorCaCcIndexOrCRatio=0.01
SoilCorPriCompIndexSecCompIndex=0.01
SoilCorSecCompRateSecCompIndex=0.01
SoilCp=3.00E+01
SoilCp1=1.00E+01
SoilCs=6.00E+01
SoilCs1=3.00E+01
SoilAp=3.00E+01
SoilAsec=3.00E+01
SoilCar=0.0000000
SoilCa=1.0000000
SoilCompRatio=0
SoilRRatio=1.0000000
SoilCRatio=1.0000000
SoilSRatio=0.0000000
SoilCrIndex=1.0000000
SoilCcIndex=1.0000000
SoilCswIndex=0.0000000
SoilPriCompIndex=6.000E-02
SoilSecCompIndex=2.000E-01
SoilSecCompRate=5.000E-02
SoilHorizontalBehaviourType=1
SoilElasticity=1.00000E+03
SoilDefaultElasticity=1
[END OF SOIL]
[END OF SOIL COLLECTION]
[GEOMETRY 1D DATA]
1
        0.000
Sample
5
        0.000
       -0.020
        0.000
        0.000
1
1
 0.00000000000000E+0000
 0.00000000000000E+0000
 1.00000000000000E+0000
[END OF GEOMETRY 1D DATA]
[RUN IDENTIFICATION]
Benchmark MSettle bm4-7a
Conversion formulas for a single load
NEN-Koppejan model
[END OF RUN IDENTIFICATION]
[MODEL]
0 : Dimension = 1D
0 : Calculation type = Darcy
0 : Model = NEN - Koppejan
0 : Strain type = Linear
0 : Vertical drains = FALSE
0 : Fit for settlement plate = FALSE
0 : Probabilistic = FALSE
0 : Horizontal displacements = FALSE
0 : Secondary swelling = FALSE
0 : Waspan = FALSE
[END OF MODEL]
[VERTICALS]
    100 = total Mesh
    1 = number of items
       0.000        0.000 = X, Z
[END OF VERTICALS]
[WATER]
        9.81 = Unit Weight of Water
[END OF WATER]
[NON-UNIFORM LOADS]
    0 = number of items
[END OF NON-UNIFORM LOADS]
[WATER LOADS]
    0 = number of items
[END OF WATER LOADS]
[OTHER LOADS]
    2 = number of items
Initial load
3 : Uniform
          -1      1000.00        0.001        0.000 = Time, Gamma, H, Yapplication
Load step 1
3 : Uniform
           0      1000.00        0.020        0.000 = Time, Gamma, H, Yapplication
[END OF OTHER LOADS]
[CALCULATION OPTIONS]
5 : Precon. pressure within a layer = Variable, correction at every step
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
80 = End of consolidation [days]
 1.00000000000000E-0002 = Number of subtime steps
1.000000000E+000 = Reference time
1 : Dissipation = TRUE
       0.000 = X co-ordinate dissipation
0 : Use fit factors = FALSE
       0.000 = X co-ordinate fit
1 : Predict settlements omitting additional loadsteps = TRUE
[END OF CALCULATION OPTIONS]
[RESIDUAL TIMES]
0 : Number of items
[END OF RESIDUAL TIMES]
[FILTER BAND WIDTH]
1 : Number of items
0.05
[END OF FILTER BAND WIDTH]
[PORE PRESSURE METERS]
    0 = number of items
[END OF PORE PRESSURE METERS]
[NON-UNIFORM LOADS PORE PRESSURES]
    0 = number of items
[END OF NON-UNIFORM LOADS PORE PRESSURES]
[OTHER LOADS PORE PRESSURES]
    2 = number of items
Initial load
       0.000 = Top of heightening
Load step 1
       0.000 = Top of heightening
[END OF OTHER LOADS PORE PRESSURES]
[CALCULATION OPTIONS PORE PRESSURES]
1 : Shear stress = TRUE
1 : calculation method of lateral stress ratio (k0) = Nu
[END OF CALCULATION OPTIONS PORE PRESSURES]
[VERTICAL DRAIN]
0 : Flow type = Radial
       0.000 = Bottom position
       0.000 = Position of the drain pipe
       0.000 = Position of the leftmost drain
       1.000 = Position of the rightmost drain
       1.000 = Center to center distance
       0.100 = Diameter
       0.100 = Width
       0.003 = Thickness
0 = Grid
       0.000 = Begin time
       0.000 = End time
      35.000 = Under pressure for strips and columns
       0.000 = Under pressure for sand wall
       0.000 = Start of drainage
       0.000 = Phreatic level in drain
       0.000 = Water head during dewatering
    10.00 = Tube pressure during dewatering
0 : Flow type = Off
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
ProbDefCpCor=0.01
ProbDefCsCor=0.01
ProbDefCs1Cor=0.01
ProbDefApCor=0.01
ProbDefASecCor=0.01
ProbDefRRCrCor=0.01
ProbDefCaCor=0.01
ProbDefPriCompIndexCor=0.01
ProbDefSecCompRateCor=0.01
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
[EPS]
        0.00 = Dry unit weight
        0.00 = Saturated unit weight
        0.00 = Load
        0.00 = Height above surface
[END OF EPS]
[FIT]
    0 = number of items
[END OF FIT]
[End of Input Data]

[Results]
[Verticals Count]
1
[End of Verticals Count]
[Vertical]
      1     =  Vertical count
   0.0000000     =  X co-ordinate
   0.0000000     =  Z co-ordinate
[Time-Settlement per Load]
     25  =  Time step count 
      1  =  Load step count 
   0.0000000      0.0000000   
   0.1000000      0.0029885   
   0.2008680      0.0030865   
   0.3280799      0.0031468   
   0.4885161      0.0032093   
   0.6908539      0.0032786   
   0.9460369      0.0033549   
   1.2678666      0.0034380   
   1.6737496      0.0035274   
   2.1856381      0.0036225   
   2.8312180      0.0037227   
   3.6454059      0.0038272   
   4.6722374      0.0039356   
   5.9672493      0.0040472   
   7.6004832      0.0041615   
   9.6602733      0.0042780   
  12.2580245      0.0043963   
  15.5342377      0.0045162   
  19.6661086      0.0046372   
  24.8771118      0.0047592   
  31.4490873      0.0048820   
  39.7374840      0.0050054   
  50.1905843      0.0051293   
  63.3737500      0.0052537   
  80.0000000      0.0053783   
[End of Time-Settlement per Load]
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
      1      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000   
[End of Koppejan Settlement Data]
[End of Koppejan Settlement]
[Depths]
      3    =  Depth count
  -0.0000100
  -0.0100000
  -0.0200000
[End of Depths]
[Leakages]
      2    =  Leakage count
   0.0002669
   0.0002674
[End of Leakages]
[Drained Layers]
      2    =  Layer count
0
0
[End of Drained Layers]
[Time-dependent Data]
[Column Indication]
Settlement
Effective stress vertical
Hydraulic head
Initial Stress
Loading
Upper amplitude convolution
Lower amplitude convolution
Normalized consolidation coefficient
[End of Column Indication]
[Vertical Data at Time]
   0.000000000000    =  Time in days
   0.0000000    1.0000419   -0.0000000    1.0000419    0.0000000    0.0000000    0.0000000       444.2419664 
   0.0000000    1.0419000   -0.0000000    1.0419000    0.0000000    0.0000000    0.0000000       438.0637235 
   0.0000000    1.0838000   -0.0000000    1.0838000    0.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.100000000000    =  Time in days
   0.0029885   21.0000419   -0.0000000    1.0000419   20.0000000    2.0387360    2.0387360        98.9014048 
   0.0014877   20.1617948    0.0897151    1.0419000   20.0000000    2.0387360    2.0387360        98.9528472 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.200867964560    =  Time in days
   0.0030865   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        94.1574752 
   0.0015367   20.9381621    0.0105747    1.0419000   20.0000000    0.0000000    0.0000000        94.2258576 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.328079897109    =  Time in days
   0.0031468   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        91.3482023 
   0.0015667   21.0315124    0.0010589    1.0419000   20.0000000    0.0000000    0.0000000        91.4419960 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.488516125335    =  Time in days
   0.0032093   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        88.5206279 
   0.0015978   21.0410342    0.0000883    1.0419000   20.0000000    0.0000000    0.0000000        88.6411296 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.690853931321    =  Time in days
   0.0032786   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        85.4894828 
   0.0016322   21.0418400    0.0000061    1.0419000   20.0000000    0.0000000    0.0000000        85.6377766 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.946036867147    =  Time in days
   0.0033549   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        82.2693527 
   0.0016702   21.0418965    0.0000004    1.0419000   20.0000000    0.0000000    0.0000000        82.4459449 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.267866642947    =  Time in days
   0.0034380   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        78.9016303 
   0.0017116   21.0418998    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        79.1063923 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.673749600038    =  Time in days
   0.0035274   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        75.4329269 
   0.0017560   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        75.6651115 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.185638142502    =  Time in days
   0.0036225   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        71.9100872 
   0.0018034   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        72.1683911 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.831218045106    =  Time in days
   0.0037227   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        68.3771725 
   0.0018532   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        68.6598303 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.645405853722    =  Time in days
   0.0038272   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        64.8733495 
   0.0019052   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        65.1782453 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.672237366021    =  Time in days
   0.0039356   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        61.4316754 
   0.0019592   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        61.7564554 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.967249331922    =  Time in days
   0.0040472   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        58.0786800 
   0.0020147   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        58.4208583 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.600483189417    =  Time in days
   0.0041615   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        54.8345596 
   0.0020716   21.0419000    0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        55.1916088 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   9.660273294451    =  Time in days
   0.0042780   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        51.7137678 
   0.0021295   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        52.0831919 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  12.258024533400    =  Time in days
   0.0043963   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        48.7258129 
   0.0021884   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        49.1052026 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  15.534237717922    =  Time in days
   0.0045162   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        45.8761184 
   0.0022480   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        46.2631901 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  19.666108649017    =  Time in days
   0.0046372   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        43.1668504 
   0.0023082   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        43.5594720 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  24.877111849874    =  Time in days
   0.0047592   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        40.5976598 
   0.0023689   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        40.9938651 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  31.449087308977    =  Time in days
   0.0048820   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        38.1663151 
   0.0024300   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        38.5643099 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  39.737483951673    =  Time in days
   0.0050054   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        35.8692231 
   0.0024914   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        36.2673853 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.190584291769    =  Time in days
   0.0051293   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        33.7018452 
   0.0025531   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        34.0987202 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  63.373750039078    =  Time in days
   0.0052537   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000        31.6590224 
   0.0026150   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000        32.0533163 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  80.000000000000    =  Time in days
   0.0053783   21.0000419   -0.0000000    1.0000419   20.0000000    0.0000000    0.0000000         0.0000000 
   0.0026770   21.0419000   -0.0000000    1.0419000   20.0000000    0.0000000    0.0000000         0.0000000 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[End of Time dependent Data]
[Time-dependent Data]
[Column Indication]
Depth
Settlement
[End of Column Indication]
[Vertical Data at Fixed Time]
   0.001000000000    =  Time in days
  -0.0000100    0.0000299
  -0.0010095    0.0000284
  -0.0020090    0.0000269
  -0.0030085    0.0000254
  -0.0040080    0.0000239
  -0.0050075    0.0000224
  -0.0060070    0.0000209
  -0.0070065    0.0000194
  -0.0080060    0.0000179
  -0.0090055    0.0000164
  -0.0100050    0.0000149
  -0.0110045    0.0000134
  -0.0120040    0.0000119
  -0.0130035    0.0000104
  -0.0140030    0.0000089
  -0.0150025    0.0000074
  -0.0160020    0.0000059
  -0.0170015    0.0000045
  -0.0180010    0.0000030
  -0.0190005    0.0000015
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000598
  -0.0010095    0.0000568
  -0.0020090    0.0000538
  -0.0030085    0.0000508
  -0.0040080    0.0000478
  -0.0050075    0.0000448
  -0.0060070    0.0000418
  -0.0070065    0.0000387
  -0.0080060    0.0000357
  -0.0090055    0.0000327
  -0.0100050    0.0000297
  -0.0110045    0.0000268
  -0.0120040    0.0000238
  -0.0130035    0.0000208
  -0.0140030    0.0000178
  -0.0150025    0.0000149
  -0.0160020    0.0000119
  -0.0170015    0.0000089
  -0.0180010    0.0000059
  -0.0190005    0.0000030
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0001494
  -0.0010095    0.0001419
  -0.0020090    0.0001344
  -0.0030085    0.0001269
  -0.0040080    0.0001194
  -0.0050075    0.0001119
  -0.0060070    0.0001044
  -0.0070065    0.0000969
  -0.0080060    0.0000894
  -0.0090055    0.0000819
  -0.0100050    0.0000743
  -0.0110045    0.0000669
  -0.0120040    0.0000595
  -0.0130035    0.0000520
  -0.0140030    0.0000446
  -0.0150025    0.0000372
  -0.0160020    0.0000297
  -0.0170015    0.0000223
  -0.0180010    0.0000149
  -0.0190005    0.0000074
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0002988
  -0.0010095    0.0002838
  -0.0020090    0.0002688
  -0.0030085    0.0002538
  -0.0040080    0.0002388
  -0.0050075    0.0002238
  -0.0060070    0.0002088
  -0.0070065    0.0001937
  -0.0080060    0.0001787
  -0.0090055    0.0001637
  -0.0100050    0.0001487
  -0.0110045    0.0001338
  -0.0120040    0.0001190
  -0.0130035    0.0001041
  -0.0140030    0.0000892
  -0.0150025    0.0000743
  -0.0160020    0.0000595
  -0.0170015    0.0000446
  -0.0180010    0.0000297
  -0.0190005    0.0000149
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
  -0.0000100    0.0005977
  -0.0010095    0.0005677
  -0.0020090    0.0005376
  -0.0030085    0.0005076
  -0.0040080    0.0004776
  -0.0050075    0.0004475
  -0.0060070    0.0004175
  -0.0070065    0.0003875
  -0.0080060    0.0003575
  -0.0090055    0.0003274
  -0.0100050    0.0002974
  -0.0110045    0.0002677
  -0.0120040    0.0002379
  -0.0130035    0.0002082
  -0.0140030    0.0001784
  -0.0150025    0.0001487
  -0.0160020    0.0001190
  -0.0170015    0.0000892
  -0.0180010    0.0000595
  -0.0190005    0.0000297
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
  -0.0000100    0.0014942
  -0.0010095    0.0014192
  -0.0020090    0.0013441
  -0.0030085    0.0012690
  -0.0040080    0.0011939
  -0.0050075    0.0011189
  -0.0060070    0.0010438
  -0.0070065    0.0009687
  -0.0080060    0.0008936
  -0.0090055    0.0008186
  -0.0100050    0.0007435
  -0.0110045    0.0006691
  -0.0120040    0.0005948
  -0.0130035    0.0005204
  -0.0140030    0.0004461
  -0.0150025    0.0003717
  -0.0160020    0.0002974
  -0.0170015    0.0002230
  -0.0180010    0.0001487
  -0.0190005    0.0000743
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0029885
  -0.0010095    0.0028383
  -0.0020090    0.0026882
  -0.0030085    0.0025380
  -0.0040080    0.0023879
  -0.0050075    0.0022377
  -0.0060070    0.0020876
  -0.0070065    0.0019374
  -0.0080060    0.0017873
  -0.0090055    0.0016371
  -0.0100050    0.0014870
  -0.0110045    0.0013383
  -0.0120040    0.0011896
  -0.0130035    0.0010409
  -0.0140030    0.0008922
  -0.0150025    0.0007435
  -0.0160020    0.0005948
  -0.0170015    0.0004461
  -0.0180010    0.0002974
  -0.0190005    0.0001487
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0030859
  -0.0010095    0.0029309
  -0.0020090    0.0027758
  -0.0030085    0.0026208
  -0.0040080    0.0024658
  -0.0050075    0.0023108
  -0.0060070    0.0021557
  -0.0070065    0.0020007
  -0.0080060    0.0018457
  -0.0090055    0.0016906
  -0.0100050    0.0015356
  -0.0110045    0.0013820
  -0.0120040    0.0012285
  -0.0130035    0.0010749
  -0.0140030    0.0009214
  -0.0150025    0.0007678
  -0.0160020    0.0006142
  -0.0170015    0.0004607
  -0.0180010    0.0003071
  -0.0190005    0.0001536
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0032139
  -0.0010095    0.0030525
  -0.0020090    0.0028910
  -0.0030085    0.0027295
  -0.0040080    0.0025681
  -0.0050075    0.0024066
  -0.0060070    0.0022451
  -0.0070065    0.0020837
  -0.0080060    0.0019222
  -0.0090055    0.0017607
  -0.0100050    0.0015993
  -0.0110045    0.0014394
  -0.0120040    0.0012794
  -0.0130035    0.0011195
  -0.0140030    0.0009596
  -0.0150025    0.0007996
  -0.0160020    0.0006397
  -0.0170015    0.0004798
  -0.0180010    0.0003199
  -0.0190005    0.0001599
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0033707
  -0.0010095    0.0032013
  -0.0020090    0.0030320
  -0.0030085    0.0028626
  -0.0040080    0.0026933
  -0.0050075    0.0025239
  -0.0060070    0.0023546
  -0.0070065    0.0021852
  -0.0080060    0.0020159
  -0.0090055    0.0018466
  -0.0100050    0.0016772
  -0.0110045    0.0015095
  -0.0120040    0.0013418
  -0.0130035    0.0011741
  -0.0140030    0.0010063
  -0.0150025    0.0008386
  -0.0160020    0.0006709
  -0.0170015    0.0005032
  -0.0180010    0.0003354
  -0.0190005    0.0001677
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100    0.0035909
  -0.0010095    0.0034104
  -0.0020090    0.0032300
  -0.0030085    0.0030496
  -0.0040080    0.0028692
  -0.0050075    0.0026888
  -0.0060070    0.0025084
  -0.0070065    0.0023280
  -0.0080060    0.0021475
  -0.0090055    0.0019671
  -0.0100050    0.0017867
  -0.0110045    0.0016081
  -0.0120040    0.0014294
  -0.0130035    0.0012507
  -0.0140030    0.0010720
  -0.0150025    0.0008934
  -0.0160020    0.0007147
  -0.0170015    0.0005360
  -0.0180010    0.0003573
  -0.0190005    0.0001787
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0039666
  -0.0010095    0.0037673
  -0.0020090    0.0035680
  -0.0030085    0.0033687
  -0.0040080    0.0031694
  -0.0050075    0.0029701
  -0.0060070    0.0027708
  -0.0070065    0.0025715
  -0.0080060    0.0023722
  -0.0090055    0.0021729
  -0.0100050    0.0019736
  -0.0110045    0.0017762
  -0.0120040    0.0015789
  -0.0130035    0.0013815
  -0.0140030    0.0011841
  -0.0150025    0.0009868
  -0.0160020    0.0007894
  -0.0170015    0.0005921
  -0.0180010    0.0003947
  -0.0190005    0.0001974
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0042952
  -0.0010095    0.0040794
  -0.0020090    0.0038635
  -0.0030085    0.0036477
  -0.0040080    0.0034319
  -0.0050075    0.0032161
  -0.0060070    0.0030003
  -0.0070065    0.0027844
  -0.0080060    0.0025686
  -0.0090055    0.0023528
  -0.0100050    0.0021370
  -0.0110045    0.0019233
  -0.0120040    0.0017096
  -0.0130035    0.0014959
  -0.0140030    0.0012822
  -0.0150025    0.0010685
  -0.0160020    0.0008548
  -0.0170015    0.0006411
  -0.0180010    0.0004274
  -0.0190005    0.0002137
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0046459
  -0.0010095    0.0044125
  -0.0020090    0.0041790
  -0.0030085    0.0039456
  -0.0040080    0.0037121
  -0.0050075    0.0034787
  -0.0060070    0.0032452
  -0.0070065    0.0030118
  -0.0080060    0.0027783
  -0.0090055    0.0025449
  -0.0100050    0.0023114
  -0.0110045    0.0020803
  -0.0120040    0.0018491
  -0.0130035    0.0016180
  -0.0140030    0.0013869
  -0.0150025    0.0011557
  -0.0160020    0.0009246
  -0.0170015    0.0006934
  -0.0180010    0.0004623
  -0.0190005    0.0002311
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0051273
  -0.0010095    0.0048697
  -0.0020090    0.0046120
  -0.0030085    0.0043544
  -0.0040080    0.0040967
  -0.0050075    0.0038391
  -0.0060070    0.0035814
  -0.0070065    0.0033238
  -0.0080060    0.0030661
  -0.0090055    0.0028085
  -0.0100050    0.0025508
  -0.0110045    0.0022957
  -0.0120040    0.0020407
  -0.0130035    0.0017856
  -0.0140030    0.0015305
  -0.0150025    0.0012754
  -0.0160020    0.0010203
  -0.0170015    0.0007652
  -0.0180010    0.0005102
  -0.0190005    0.0002551
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0053783
  -0.0010095    0.0051080
  -0.0020090    0.0048378
  -0.0030085    0.0045675
  -0.0040080    0.0042972
  -0.0050075    0.0040270
  -0.0060070    0.0037567
  -0.0070065    0.0034864
  -0.0080060    0.0032162
  -0.0090055    0.0029459
  -0.0100050    0.0026756
  -0.0110045    0.0024081
  -0.0120040    0.0021405
  -0.0130035    0.0018730
  -0.0140030    0.0016054
  -0.0150025    0.0013378
  -0.0160020    0.0010703
  -0.0170015    0.0008027
  -0.0180010    0.0005351
  -0.0190005    0.0002676
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[End of Time dependent Data]
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
[Dissipation in Layers]
      1  =  Number of Layers 
     25  =  Number of time steps 
[Dissipation layer]
      1  =  Layer Number 
   0.0000000      0.0000000   
   0.1000000      0.9902590   
   0.2008680      0.9988930   
   0.3280799      0.9998844   
   0.4885161      0.9999897   
   0.6908539      0.9999992   
   0.9460369      0.9999999   
   1.2678666      1.0000000   
   1.6737496      1.0000000   
   2.1856381      1.0000000   
   2.8312180      1.0000000   
   3.6454059      1.0000000   
   4.6722374      1.0000000   
   5.9672493      1.0000000   
   7.6004832      1.0000000   
   9.6602733      1.0000000   
  12.2580245      1.0000000   
  15.5342377      1.0000000   
  19.6661086      1.0000000   
  24.8771118      1.0000000   
  31.4490873      1.0000000   
  39.7374840      1.0000000   
  50.1905843      1.0000000   
  63.3737500      1.0000000   
  80.0000000      1.0000000   
[End of Dissipation layer]
[End of Dissipation in Layers]
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
