Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 10/08/2023
TIME       : 07:53:53
FILENAME   : C:\Deltares\D-Settlement\Benchmarks\bm4-7c.sld
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
0 : Calculation type = Darcy
1 : Model = NEN - Bjerrum
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
Sample
SoilColor=16575398
SoilGamDry=14.00
SoilGamWet=14.00
SoilInitialVoidRatio=0.000000
SoilPreconIsotacheType=1
SoilPreconKoppejanType=1
SoilUseEquivalentAge=0
SoilEquivalentAge=0.00E+00
SoilPc=1.00E+01
SoilOCR=1.30
SoilPOP=10.00
SoilDrained=0
SoilApAsApproximationByCpCs=0
SoilSecondarySwellingReduced=0
SoilSecondarySwellingFactor=0.50
SoilUnloadingStressRatio=2.00
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
SoilStdPriCompIndex=1.110E-02
SoilStdSecCompIndex=4.388E-02
SoilStdSecCompRate=1.497E-02
SoilStdOCR=0.33
SoilStdPermeabilityVer=1.000E-01
SoilStdPOP=2.50
SoilStdPermeabilityHorFactor=0.750
SoilStdInitialVoidRatio=0.000000
SoilStdPermeabilityStrainModulus=0.000E+00
SoilStdLimitStress=0.00
SoilStdCp=7.50E+00
SoilStdCp1=2.40E+00
SoilStdCs=1.80E+01
SoilStdCs1=6.00E+00
SoilStdAp=3.00E+00
SoilStdAsec=2.40E+01
SoilStdCar=0.0000000
SoilStdCa=0.0156225
SoilStdRRatio=0.0191882
SoilStdCRatio=0.0575646
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
SoilCp=2.50E+01
SoilCp1=8.00E+00
SoilCs=6.00E+01
SoilCs1=2.00E+01
SoilAp=1.00E+01
SoilAsec=8.00E+01
SoilCar=0.0000000
SoilCa=0.0624900
SoilCompRatio=1
SoilRRatio=0.0767528
SoilCRatio=0.2302585
SoilSRatio=0.0000000
SoilCrIndex=1.0000000
SoilCcIndex=1.0000000
SoilCswIndex=0.0000000
SoilPriCompIndex=4.440E-02
SoilSecCompIndex=1.755E-01
SoilSecCompRate=5.987E-02
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
Benchmark MSettle bm4-7c
Conversion formulas for a single load
NEN-Bjerrum model
[END OF RUN IDENTIFICATION]
[VERTICALS]
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
     25  =  Time step count 
      1  =  Load step count 
   0.0000000      0.0000000   
   0.1000000      0.0022523   
   0.2008680      0.0024352   
   0.3280799      0.0025997   
   0.4885161      0.0027545   
   0.6908539      0.0029024   
   0.9460369      0.0030452   
   1.2678666      0.0031842   
   1.6737496      0.0033203   
   2.1856381      0.0034543   
   2.8312180      0.0035865   
   3.6454059      0.0037174   
   4.6722374      0.0038472   
   5.9672493      0.0039762   
   7.6004832      0.0041046   
   9.6602733      0.0042325   
  12.2580245      0.0043600   
  15.5342377      0.0044871   
  19.6661086      0.0046140   
  24.8771118      0.0047407   
  31.4490873      0.0048672   
  39.7374840      0.0049936   
  50.1905843      0.0051199   
  63.3737500      0.0052462   
  80.0000000      0.0053723   
[End of Time-Settlement per Load]
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
   0.0000000    1.0000419   -0.0000000    1.0000419    0.0000000    0.0000000    0.0000000      1332.7260381 
   0.0000000    1.0419000   -0.0000000    1.0419000    0.0000000    0.0000000    0.0000000      1314.1913144 
   0.0000000    1.0838000   -0.0000000    1.0838000    0.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.100000000000    =  Time in days
   0.0022523   21.0000419   -0.0000000    1.0000419   20.0000000    2.4316114    2.4316114       429.0709160 
   0.0011201   20.6850220    0.0363790    1.0419000   20.0000000    2.4315581    2.4315581       428.7667634 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.200867964560    =  Time in days
   0.0024352   21.0000419   -0.0000000    1.0000419   20.0000000    0.2717644    0.2717644       391.5020324 
   0.0012114   20.9115916    0.0132832    1.0419000   20.0000000    0.2721295    0.2721295       391.3211485 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.328079897109    =  Time in days
   0.0025997   21.0000419   -0.0000000    1.0000419   20.0000000    0.2506524    0.2506524       360.5391284 
   0.0012937   20.9422096    0.0101621    1.0419000   20.0000000    0.2511817    0.2511817       360.4341832 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.488516125335    =  Time in days
   0.0027545   21.0000419   -0.0000000    1.0000419   20.0000000    0.2360063    0.2360063       333.6566712 
   0.0013710   20.9612917    0.0082169    1.0419000   20.0000000    0.2366295    0.2366295       333.5996278 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.690853931321    =  Time in days
   0.0029024   21.0000419   -0.0000000    1.0000419   20.0000000    0.2255230    0.2255230       309.8521442 
   0.0014450   20.9759649    0.0067212    1.0419000   20.0000000    0.2262035    0.2262035       309.8261300 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.946036867147    =  Time in days
   0.0030452   21.0000419   -0.0000000    1.0000419   20.0000000    0.2178255    0.2178255       288.4797156 
   0.0015164   20.9875626    0.0055390    1.0419000   20.0000000    0.2185428    0.2185428       288.4740766 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.267866642947    =  Time in days
   0.0031842   21.0000419   -0.0000000    1.0000419   20.0000000    0.2120664    0.2120664       269.0937176 
   0.0015859   20.9968720    0.0045900    1.0419000   20.0000000    0.2128083    0.2128083       269.1014961 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.673749600038    =  Time in days
   0.0033203   21.0000419   -0.0000000    1.0000419   20.0000000    0.2076965    0.2076965       251.3736636 
   0.0016540   21.0044303    0.0038195    1.0419000   20.0000000    0.2084554    0.2084554       251.3902046 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.185638142502    =  Time in days
   0.0034543   21.0000419   -0.0000000    1.0000419   20.0000000    0.2043450    0.2043450       235.0810735 
   0.0017210   21.0106203    0.0031886    1.0419000   20.0000000    0.2051160    0.2051160       235.1032086 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.831218045106    =  Time in days
   0.0035865   21.0000419   -0.0000000    1.0000419   20.0000000    0.2017534    0.2017534       220.0331531 
   0.0017871   21.0157234    0.0026684    1.0419000   20.0000000    0.2025331    0.2025331       220.0587013 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.645405853722    =  Time in days
   0.0037174   21.0000419   -0.0000000    1.0000419   20.0000000    0.1997365    0.1997365       206.0860658 
   0.0018525   21.0199520    0.0022373    1.0419000   20.0000000    0.2005226    0.2005226       206.1135161 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.672237366021    =  Time in days
   0.0038472   21.0000419   -0.0000000    1.0000419   20.0000000    0.1981589    0.1981589       193.1239340 
   0.0019175   21.0234701    0.0018787    1.0419000   20.0000000    0.1989498    0.1989498       193.1522379 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.967249331922    =  Time in days
   0.0039762   21.0000419   -0.0000000    1.0000419   20.0000000    0.1969200    0.1969200       181.0514029 
   0.0019820   21.0264061    0.0015794    1.0419000   20.0000000    0.1977144    0.1977144       181.0798352 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.600483189417    =  Time in days
   0.0041046   21.0000419   -0.0000000    1.0000419   20.0000000    0.1959188    0.1959188       169.7884898 
   0.0020463   21.0288641    0.0013288    1.0419000   20.0000000    0.1967159    0.1967159       169.8165536 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   9.660273294451    =  Time in days
   0.0042325   21.0000419   -0.0000000    1.0000419   20.0000000    0.1951519    0.1951519       159.2669631 
   0.0021102   21.0309225    0.0011190    1.0419000   20.0000000    0.1959511    0.1959511       159.2943234 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  12.258024533400    =  Time in days
   0.0043600   21.0000419   -0.0000000    1.0000419   20.0000000    0.1945450    0.1945450       149.4277115 
   0.0021740   21.0326506    0.0009429    1.0419000   20.0000000    0.1953459    0.1953459       149.4541490 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  15.534237717922    =  Time in days
   0.0044871   21.0000419   -0.0000000    1.0000419   20.0000000    0.1940639    0.1940639       140.2188537 
   0.0022376   21.0341032    0.0007948    1.0419000   20.0000000    0.1948660    0.1948660       140.2442316 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  19.666108649017    =  Time in days
   0.0046140   21.0000419   -0.0000000    1.0000419   20.0000000    0.1936820    0.1936820       131.5943261 
   0.0023011   21.0353252    0.0006702    1.0419000   20.0000000    0.1944850    0.1944850       131.6185665 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  24.877111849874    =  Time in days
   0.0047407   21.0000419   -0.0000000    1.0000419   20.0000000    0.1933784    0.1933784       123.5128284 
   0.0023644   21.0363542    0.0005653    1.0419000   20.0000000    0.1941822    0.1941822       123.5358952 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  31.449087308977    =  Time in days
   0.0048672   21.0000419   -0.0000000    1.0000419   20.0000000    0.1931368    0.1931368       115.9370218 
   0.0024277   21.0372210    0.0004770    1.0419000   20.0000000    0.1939412    0.1939412       115.9589085 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  39.737483951673    =  Time in days
   0.0049936   21.0000419   -0.0000000    1.0000419   20.0000000    0.1929444    0.1929444       108.8329142 
   0.0024910   21.0379517    0.0004025    1.0419000   20.0000000    0.1937493    0.1937493       108.8536347 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.190584291769    =  Time in days
   0.0051199   21.0000419   -0.0000000    1.0000419   20.0000000    0.1927910    0.1927910       102.1693806 
   0.0025542   21.0385677    0.0003397    1.0419000   20.0000000    0.1935963    0.1935963       102.1889628 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  63.373750039078    =  Time in days
   0.0052462   21.0000419   -0.0000000    1.0000419   20.0000000    0.1926687    0.1926687        95.9177851 
   0.0026173   21.0390874    0.0002867    1.0419000   20.0000000    0.1934742    0.1934742        95.9362665 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  80.000000000000    =  Time in days
   0.0053723   21.0000419   -0.0000000    1.0000419   20.0000000    0.1925711    0.1925711         0.0000000 
   0.0026804   21.0395257    0.0002420    1.0419000   20.0000000    0.1933768    0.1933768         0.0000000 
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
  -0.0000100    0.0000225
  -0.0010095    0.0000214
  -0.0020090    0.0000203
  -0.0030085    0.0000191
  -0.0040080    0.0000180
  -0.0050075    0.0000169
  -0.0060070    0.0000157
  -0.0070065    0.0000146
  -0.0080060    0.0000135
  -0.0090055    0.0000123
  -0.0100050    0.0000112
  -0.0110045    0.0000101
  -0.0120040    0.0000090
  -0.0130035    0.0000078
  -0.0140030    0.0000067
  -0.0150025    0.0000056
  -0.0160020    0.0000045
  -0.0170015    0.0000034
  -0.0180010    0.0000022
  -0.0190005    0.0000011
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000450
  -0.0010095    0.0000428
  -0.0020090    0.0000405
  -0.0030085    0.0000382
  -0.0040080    0.0000360
  -0.0050075    0.0000337
  -0.0060070    0.0000315
  -0.0070065    0.0000292
  -0.0080060    0.0000269
  -0.0090055    0.0000247
  -0.0100050    0.0000224
  -0.0110045    0.0000202
  -0.0120040    0.0000179
  -0.0130035    0.0000157
  -0.0140030    0.0000134
  -0.0150025    0.0000112
  -0.0160020    0.0000090
  -0.0170015    0.0000067
  -0.0180010    0.0000045
  -0.0190005    0.0000022
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0001126
  -0.0010095    0.0001070
  -0.0020090    0.0001013
  -0.0030085    0.0000956
  -0.0040080    0.0000900
  -0.0050075    0.0000843
  -0.0060070    0.0000786
  -0.0070065    0.0000730
  -0.0080060    0.0000673
  -0.0090055    0.0000616
  -0.0100050    0.0000560
  -0.0110045    0.0000504
  -0.0120040    0.0000448
  -0.0130035    0.0000392
  -0.0140030    0.0000336
  -0.0150025    0.0000280
  -0.0160020    0.0000224
  -0.0170015    0.0000168
  -0.0180010    0.0000112
  -0.0190005    0.0000056
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0002252
  -0.0010095    0.0002139
  -0.0020090    0.0002026
  -0.0030085    0.0001912
  -0.0040080    0.0001799
  -0.0050075    0.0001686
  -0.0060070    0.0001573
  -0.0070065    0.0001459
  -0.0080060    0.0001346
  -0.0090055    0.0001233
  -0.0100050    0.0001120
  -0.0110045    0.0001008
  -0.0120040    0.0000896
  -0.0130035    0.0000784
  -0.0140030    0.0000672
  -0.0150025    0.0000560
  -0.0160020    0.0000448
  -0.0170015    0.0000336
  -0.0180010    0.0000224
  -0.0190005    0.0000112
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
  -0.0000100    0.0004505
  -0.0010095    0.0004278
  -0.0020090    0.0004051
  -0.0030085    0.0003825
  -0.0040080    0.0003598
  -0.0050075    0.0003372
  -0.0060070    0.0003145
  -0.0070065    0.0002919
  -0.0080060    0.0002692
  -0.0090055    0.0002466
  -0.0100050    0.0002239
  -0.0110045    0.0002015
  -0.0120040    0.0001791
  -0.0130035    0.0001567
  -0.0140030    0.0001343
  -0.0150025    0.0001120
  -0.0160020    0.0000896
  -0.0170015    0.0000672
  -0.0180010    0.0000448
  -0.0190005    0.0000224
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
  -0.0000100    0.0011261
  -0.0010095    0.0010695
  -0.0020090    0.0010129
  -0.0030085    0.0009562
  -0.0040080    0.0008996
  -0.0050075    0.0008429
  -0.0060070    0.0007863
  -0.0070065    0.0007297
  -0.0080060    0.0006730
  -0.0090055    0.0006164
  -0.0100050    0.0005598
  -0.0110045    0.0005038
  -0.0120040    0.0004478
  -0.0130035    0.0003918
  -0.0140030    0.0003359
  -0.0150025    0.0002799
  -0.0160020    0.0002239
  -0.0170015    0.0001679
  -0.0180010    0.0001120
  -0.0190005    0.0000560
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0022523
  -0.0010095    0.0021390
  -0.0020090    0.0020257
  -0.0030085    0.0019125
  -0.0040080    0.0017992
  -0.0050075    0.0016859
  -0.0060070    0.0015726
  -0.0070065    0.0014593
  -0.0080060    0.0013461
  -0.0090055    0.0012328
  -0.0100050    0.0011195
  -0.0110045    0.0010076
  -0.0120040    0.0008956
  -0.0130035    0.0007837
  -0.0140030    0.0006717
  -0.0150025    0.0005598
  -0.0160020    0.0004478
  -0.0170015    0.0003359
  -0.0180010    0.0002239
  -0.0190005    0.0001120
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0024341
  -0.0010095    0.0023117
  -0.0020090    0.0021893
  -0.0030085    0.0020669
  -0.0040080    0.0019446
  -0.0050075    0.0018222
  -0.0060070    0.0016998
  -0.0070065    0.0015774
  -0.0080060    0.0014550
  -0.0090055    0.0013326
  -0.0100050    0.0012103
  -0.0110045    0.0010892
  -0.0120040    0.0009682
  -0.0130035    0.0008472
  -0.0140030    0.0007262
  -0.0150025    0.0006051
  -0.0160020    0.0004841
  -0.0170015    0.0003631
  -0.0180010    0.0002421
  -0.0190005    0.0001210
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0027644
  -0.0010095    0.0026255
  -0.0020090    0.0024866
  -0.0030085    0.0023477
  -0.0040080    0.0022088
  -0.0050075    0.0020699
  -0.0060070    0.0019310
  -0.0070065    0.0017920
  -0.0080060    0.0016531
  -0.0090055    0.0015142
  -0.0100050    0.0013753
  -0.0110045    0.0012378
  -0.0120040    0.0011002
  -0.0130035    0.0009627
  -0.0140030    0.0008252
  -0.0150025    0.0006877
  -0.0160020    0.0005501
  -0.0170015    0.0004126
  -0.0180010    0.0002751
  -0.0190005    0.0001375
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0030715
  -0.0010095    0.0029173
  -0.0020090    0.0027630
  -0.0030085    0.0026087
  -0.0040080    0.0024544
  -0.0050075    0.0023002
  -0.0060070    0.0021459
  -0.0070065    0.0019916
  -0.0080060    0.0018373
  -0.0090055    0.0016830
  -0.0100050    0.0015288
  -0.0110045    0.0013759
  -0.0120040    0.0012230
  -0.0130035    0.0010701
  -0.0140030    0.0009173
  -0.0150025    0.0007644
  -0.0160020    0.0006115
  -0.0170015    0.0004586
  -0.0180010    0.0003058
  -0.0190005    0.0001529
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100    0.0034097
  -0.0010095    0.0032385
  -0.0020090    0.0030673
  -0.0030085    0.0028961
  -0.0040080    0.0027250
  -0.0050075    0.0025538
  -0.0060070    0.0023826
  -0.0070065    0.0022114
  -0.0080060    0.0020402
  -0.0090055    0.0018690
  -0.0100050    0.0016978
  -0.0110045    0.0015280
  -0.0120040    0.0013583
  -0.0130035    0.0011885
  -0.0140030    0.0010187
  -0.0150025    0.0008489
  -0.0160020    0.0006791
  -0.0170015    0.0005093
  -0.0180010    0.0003396
  -0.0190005    0.0001698
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0038830
  -0.0010095    0.0036881
  -0.0020090    0.0034933
  -0.0030085    0.0032984
  -0.0040080    0.0031035
  -0.0050075    0.0029087
  -0.0060070    0.0027138
  -0.0070065    0.0025190
  -0.0080060    0.0023241
  -0.0090055    0.0021293
  -0.0100050    0.0019344
  -0.0110045    0.0017410
  -0.0120040    0.0015475
  -0.0130035    0.0013541
  -0.0140030    0.0011606
  -0.0150025    0.0009672
  -0.0160020    0.0007738
  -0.0170015    0.0005803
  -0.0180010    0.0003869
  -0.0190005    0.0001934
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0042510
  -0.0010095    0.0040377
  -0.0020090    0.0038245
  -0.0030085    0.0036112
  -0.0040080    0.0033980
  -0.0050075    0.0031847
  -0.0060070    0.0029714
  -0.0070065    0.0027582
  -0.0080060    0.0025449
  -0.0090055    0.0023317
  -0.0100050    0.0021184
  -0.0110045    0.0019066
  -0.0120040    0.0016947
  -0.0130035    0.0014829
  -0.0140030    0.0012711
  -0.0150025    0.0010592
  -0.0160020    0.0008474
  -0.0170015    0.0006355
  -0.0180010    0.0004237
  -0.0190005    0.0002118
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0046231
  -0.0010095    0.0043912
  -0.0020090    0.0041594
  -0.0030085    0.0039275
  -0.0040080    0.0036956
  -0.0050075    0.0034638
  -0.0060070    0.0032319
  -0.0070065    0.0030000
  -0.0080060    0.0027682
  -0.0090055    0.0025363
  -0.0100050    0.0023045
  -0.0110045    0.0020740
  -0.0120040    0.0018436
  -0.0130035    0.0016131
  -0.0140030    0.0013827
  -0.0150025    0.0011522
  -0.0160020    0.0009218
  -0.0170015    0.0006913
  -0.0180010    0.0004609
  -0.0190005    0.0002304
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0051179
  -0.0010095    0.0048613
  -0.0020090    0.0046047
  -0.0030085    0.0043481
  -0.0040080    0.0040915
  -0.0050075    0.0038349
  -0.0060070    0.0035783
  -0.0070065    0.0033217
  -0.0080060    0.0030650
  -0.0090055    0.0028084
  -0.0100050    0.0025518
  -0.0110045    0.0022967
  -0.0120040    0.0020415
  -0.0130035    0.0017863
  -0.0140030    0.0015311
  -0.0150025    0.0012759
  -0.0160020    0.0010207
  -0.0170015    0.0007656
  -0.0180010    0.0005104
  -0.0190005    0.0002552
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0053723
  -0.0010095    0.0051030
  -0.0020090    0.0048337
  -0.0030085    0.0045643
  -0.0040080    0.0042950
  -0.0050075    0.0040257
  -0.0060070    0.0037564
  -0.0070065    0.0034870
  -0.0080060    0.0032177
  -0.0090055    0.0029484
  -0.0100050    0.0026791
  -0.0110045    0.0024112
  -0.0120040    0.0021432
  -0.0130035    0.0018753
  -0.0140030    0.0016074
  -0.0150025    0.0013395
  -0.0160020    0.0010716
  -0.0170015    0.0008037
  -0.0180010    0.0005358
  -0.0190005    0.0002679
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
   0.1000000      0.9962815   
   0.2008680      0.9970689   
   0.3280799      0.9976336   
   0.4885161      0.9980825   
   0.6908539      0.9984310   
   0.9460369      0.9987067   
   1.2678666      0.9989282   
   1.6737496      0.9991080   
   2.1856381      0.9992553   
   2.8312180      0.9993768   
   3.6454059      0.9994774   
   4.6722374      0.9995612   
   5.9672493      0.9996311   
   7.6004832      0.9996896   
   9.6602733      0.9997386   
  12.2580245      0.9997798   
  15.5342377      0.9998144   
  19.6661086      0.9998435   
  24.8771118      0.9998680   
  31.4490873      0.9998886   
  39.7374840      0.9999060   
  50.1905843      0.9999207   
  63.3737500      0.9999330   
  80.0000000      0.9999435   
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
