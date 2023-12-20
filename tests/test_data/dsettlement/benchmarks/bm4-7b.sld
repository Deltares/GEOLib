Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 10/08/2023
TIME       : 07:53:52
FILENAME   : C:\Deltares\D-Settlement\Benchmarks\bm4-7b.sld
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
2 : Model = Isotache
1 : Strain type = Natural
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
SoilStdPriCompIndex=8.665E-03
SoilStdSecCompIndex=2.820E-02
SoilStdSecCompRate=8.597E-03
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
SoilCp=2.50E+01
SoilCp1=8.00E+00
SoilCs=6.00E+01
SoilCs1=2.00E+01
SoilAp=1.00E+01
SoilAsec=8.00E+01
SoilCar=0.0000000
SoilCa=1.0000000
SoilCompRatio=0
SoilRRatio=1.0000000
SoilCRatio=1.0000000
SoilSRatio=0.0000000
SoilCrIndex=1.0000000
SoilCcIndex=1.0000000
SoilCswIndex=0.0000000
SoilPriCompIndex=3.466E-02
SoilSecCompIndex=1.128E-01
SoilSecCompRate=3.439E-02
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
Benchmark MSettle bm4-7b
Conversion formulas for a single load
Isotache model
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
   0.1000000      0.0022321   
   0.2008680      0.0024221   
   0.3280799      0.0025946   
   0.4885161      0.0027574   
   0.6908539      0.0029131   
   0.9460369      0.0030633   
   1.2678666      0.0032089   
   1.6737496      0.0033509   
   2.1856381      0.0034899   
   2.8312180      0.0036263   
   3.6454059      0.0037605   
   4.6722374      0.0038927   
   5.9672493      0.0040232   
   7.6004832      0.0041522   
   9.6602733      0.0042796   
  12.2580245      0.0044057   
  15.5342377      0.0045306   
  19.6661086      0.0046543   
  24.8771118      0.0047768   
  31.4490873      0.0048982   
  39.7374840      0.0050185   
  50.1905843      0.0051378   
  63.3737500      0.0052561   
  80.0000000      0.0053734   
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
   0.0000000    1.0000419   -0.0000000    1.0000419    0.0000000    0.0000000    0.0000000      1362.3695644 
   0.0000000    1.0419000   -0.0000000    1.0419000    0.0000000    0.0000000    0.0000000      1344.6841122 
   0.0000000    1.0838000   -0.0000000    1.0838000    0.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.100000000000    =  Time in days
   0.0022321   21.0000419   -0.0000000    1.0000419   20.0000000    2.4681751    2.4681751       638.9346855 
   0.0011105   20.6876170    0.0361145    1.0419000   20.0000000    2.4682191    2.4682191       635.7905303 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.200867964560    =  Time in days
   0.0024221   21.0000419   -0.0000000    1.0000419   20.0000000    0.3076081    0.3076081       600.0604641 
   0.0012055   20.9426689    0.0101153    1.0419000   20.0000000    0.3080352    0.3080352       597.1376707 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.328079897109    =  Time in days
   0.0025946   21.0000419   -0.0000000    1.0000419   20.0000000    0.2891673    0.2891673       566.9571663 
   0.0012917   20.9668929    0.0076460    1.0419000   20.0000000    0.2897758    0.2897758       564.2009510 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.488516125335    =  Time in days
   0.0027574   21.0000419   -0.0000000    1.0000419   20.0000000    0.2759491    0.2759491       537.4709144 
   0.0013732   20.9819345    0.0061127    1.0419000   20.0000000    0.2766703    0.2766703       534.8474606 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.690853931321    =  Time in days
   0.0029131   21.0000419   -0.0000000    1.0000419   20.0000000    0.2662657    0.2662657       510.8086374 
   0.0014511   20.9935305    0.0049306    1.0419000   20.0000000    0.2670606    0.2670606       508.2955426 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.946036867147    =  Time in days
   0.0030633   21.0000419   -0.0000000    1.0000419   20.0000000    0.2590340    0.2590340       486.4364035 
   0.0015262   21.0026573    0.0040003    1.0419000   20.0000000    0.2598789    0.2598789       484.0181264 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.267866642947    =  Time in days
   0.0032089   21.0000419   -0.0000000    1.0000419   20.0000000    0.2535547    0.2535547       463.9727671 
   0.0015991   21.0099262    0.0032593    1.0419000   20.0000000    0.2544347    0.2544347       461.6381191 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.673749600038    =  Time in days
   0.0033509   21.0000419   -0.0000000    1.0000419   20.0000000    0.2493574    0.2493574       443.1357439 
   0.0016701   21.0157665    0.0026640    1.0419000   20.0000000    0.2502626    0.2502626       440.8764051 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.185638142502    =  Time in days
   0.0034899   21.0000419   -0.0000000    1.0000419   20.0000000    0.2461152    0.2461152       423.7107448 
   0.0017397   21.0204903    0.0021824    1.0419000   20.0000000    0.2470388    0.2470388       421.5203447 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.831218045106    =  Time in days
   0.0036263   21.0000419   -0.0000000    1.0000419   20.0000000    0.2435942    0.2435942       405.5302511 
   0.0018080   21.0243302    0.0017910    1.0419000   20.0000000    0.2445316    0.2445316       403.4037766 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.645405853722    =  Time in days
   0.0037605   21.0000419   -0.0000000    1.0000419   20.0000000    0.2416241    0.2416241       388.4604716 
   0.0018752   21.0274635    0.0014716    1.0419000   20.0000000    0.2425718    0.2425718       386.3938752 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.672237366021    =  Time in days
   0.0038927   21.0000419   -0.0000000    1.0000419   20.0000000    0.2400486    0.2400486       372.3923243 
   0.0019414   21.0300291    0.0012101    1.0419000   20.0000000    0.2410041    0.2410041       370.3822572 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.967249331922    =  Time in days
   0.0040232   21.0000419   -0.0000000    1.0000419   20.0000000    0.2388372    0.2388372       357.2352084 
   0.0020067   21.0321314    0.0009958    1.0419000   20.0000000    0.2397988    0.2397988       355.2788357 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.600483189417    =  Time in days
   0.0041522   21.0000419   -0.0000000    1.0000419   20.0000000    0.2378814    0.2378814       342.9125726 
   0.0020712   21.0338584    0.0008197    1.0419000   20.0000000    0.2388476    0.2388476       341.0074431 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   9.660273294451    =  Time in days
   0.0042796   21.0000419   -0.0000000    1.0000419   20.0000000    0.2371256    0.2371256       329.3587571 
   0.0021350   21.0352787    0.0006750    1.0419000   20.0000000    0.2380954    0.2380954       327.5027101 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  12.258024533400    =  Time in days
   0.0044057   21.0000419   -0.0000000    1.0000419   20.0000000    0.2365271    0.2365271       316.5166719 
   0.0021982   21.0364478    0.0005558    1.0419000   20.0000000    0.2374997    0.2374997       314.7077700 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  15.534237717922    =  Time in days
   0.0045306   21.0000419   -0.0000000    1.0000419   20.0000000    0.2360524    0.2360524       304.3360795 
   0.0022607   21.0374105    0.0004576    1.0419000   20.0000000    0.2370272    0.2370272       302.5725597 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  19.666108649017    =  Time in days
   0.0046543   21.0000419   -0.0000000    1.0000419   20.0000000    0.2356756    0.2356756       292.7723059 
   0.0023226   21.0382037    0.0003768    1.0419000   20.0000000    0.2366521    0.2366521       291.0525433 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  24.877111849874    =  Time in days
   0.0047768   21.0000419   -0.0000000    1.0000419   20.0000000    0.2353761    0.2353761       281.7852611 
   0.0023839   21.0388572    0.0003102    1.0419000   20.0000000    0.2363540    0.2363540       280.1077423 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  31.449087308977    =  Time in days
   0.0048982   21.0000419   -0.0000000    1.0000419   20.0000000    0.2351380    0.2351380       271.3386855 
   0.0024447   21.0393958    0.0002553    1.0419000   20.0000000    0.2361169    0.2361169       269.7019894 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  39.737483951673    =  Time in days
   0.0050185   21.0000419   -0.0000000    1.0000419   20.0000000    0.2349484    0.2349484       261.3995647 
   0.0025049   21.0398396    0.0002100    1.0419000   20.0000000    0.2359282    0.2359282       259.8023466 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.190584291769    =  Time in days
   0.0051378   21.0000419   -0.0000000    1.0000419   20.0000000    0.2347976    0.2347976       251.9376670 
   0.0025646   21.0402052    0.0001728    1.0419000   20.0000000    0.2357780    0.2357780       250.3786484 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  63.373750039078    =  Time in days
   0.0052561   21.0000419   -0.0000000    1.0000419   20.0000000    0.2346773    0.2346773       242.9251765 
   0.0026239   21.0405064    0.0001421    1.0419000   20.0000000    0.2356583    0.2356583       241.4031358 
   0.0000000   21.0838000   -0.0000000    1.0838000   20.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
  80.000000000000    =  Time in days
   0.0053734   21.0000419   -0.0000000    1.0000419   20.0000000    0.2345815    0.2345815         0.0000000 
   0.0026826   21.0407544    0.0001168    1.0419000   20.0000000    0.2355629    0.2355629         0.0000000 
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
  -0.0000100    0.0000223
  -0.0010095    0.0000212
  -0.0020090    0.0000201
  -0.0030085    0.0000190
  -0.0040080    0.0000178
  -0.0050075    0.0000167
  -0.0060070    0.0000156
  -0.0070065    0.0000145
  -0.0080060    0.0000133
  -0.0090055    0.0000122
  -0.0100050    0.0000111
  -0.0110045    0.0000100
  -0.0120040    0.0000089
  -0.0130035    0.0000078
  -0.0140030    0.0000067
  -0.0150025    0.0000055
  -0.0160020    0.0000044
  -0.0170015    0.0000033
  -0.0180010    0.0000022
  -0.0190005    0.0000011
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000446
  -0.0010095    0.0000424
  -0.0020090    0.0000402
  -0.0030085    0.0000379
  -0.0040080    0.0000357
  -0.0050075    0.0000334
  -0.0060070    0.0000312
  -0.0070065    0.0000289
  -0.0080060    0.0000267
  -0.0090055    0.0000244
  -0.0100050    0.0000222
  -0.0110045    0.0000200
  -0.0120040    0.0000178
  -0.0130035    0.0000155
  -0.0140030    0.0000133
  -0.0150025    0.0000111
  -0.0160020    0.0000089
  -0.0170015    0.0000067
  -0.0180010    0.0000044
  -0.0190005    0.0000022
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0001116
  -0.0010095    0.0001060
  -0.0020090    0.0001004
  -0.0030085    0.0000948
  -0.0040080    0.0000892
  -0.0050075    0.0000836
  -0.0060070    0.0000779
  -0.0070065    0.0000723
  -0.0080060    0.0000667
  -0.0090055    0.0000611
  -0.0100050    0.0000555
  -0.0110045    0.0000499
  -0.0120040    0.0000444
  -0.0130035    0.0000388
  -0.0140030    0.0000333
  -0.0150025    0.0000277
  -0.0160020    0.0000222
  -0.0170015    0.0000166
  -0.0180010    0.0000111
  -0.0190005    0.0000055
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0002232
  -0.0010095    0.0002120
  -0.0020090    0.0002008
  -0.0030085    0.0001895
  -0.0040080    0.0001783
  -0.0050075    0.0001671
  -0.0060070    0.0001559
  -0.0070065    0.0001447
  -0.0080060    0.0001334
  -0.0090055    0.0001222
  -0.0100050    0.0001110
  -0.0110045    0.0000999
  -0.0120040    0.0000888
  -0.0130035    0.0000777
  -0.0140030    0.0000666
  -0.0150025    0.0000555
  -0.0160020    0.0000444
  -0.0170015    0.0000333
  -0.0180010    0.0000222
  -0.0190005    0.0000111
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
  -0.0000100    0.0004464
  -0.0010095    0.0004240
  -0.0020090    0.0004015
  -0.0030085    0.0003791
  -0.0040080    0.0003567
  -0.0050075    0.0003342
  -0.0060070    0.0003118
  -0.0070065    0.0002893
  -0.0080060    0.0002669
  -0.0090055    0.0002444
  -0.0100050    0.0002220
  -0.0110045    0.0001998
  -0.0120040    0.0001776
  -0.0130035    0.0001554
  -0.0140030    0.0001332
  -0.0150025    0.0001110
  -0.0160020    0.0000888
  -0.0170015    0.0000666
  -0.0180010    0.0000444
  -0.0190005    0.0000222
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
  -0.0000100    0.0011161
  -0.0010095    0.0010600
  -0.0020090    0.0010038
  -0.0030085    0.0009477
  -0.0040080    0.0008916
  -0.0050075    0.0008355
  -0.0060070    0.0007794
  -0.0070065    0.0007233
  -0.0080060    0.0006672
  -0.0090055    0.0006111
  -0.0100050    0.0005550
  -0.0110045    0.0004995
  -0.0120040    0.0004440
  -0.0130035    0.0003885
  -0.0140030    0.0003330
  -0.0150025    0.0002775
  -0.0160020    0.0002220
  -0.0170015    0.0001665
  -0.0180010    0.0001110
  -0.0190005    0.0000555
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0022321
  -0.0010095    0.0021199
  -0.0020090    0.0020077
  -0.0030085    0.0018955
  -0.0040080    0.0017833
  -0.0050075    0.0016710
  -0.0060070    0.0015588
  -0.0070065    0.0014466
  -0.0080060    0.0013344
  -0.0090055    0.0012221
  -0.0100050    0.0011099
  -0.0110045    0.0009989
  -0.0120040    0.0008879
  -0.0130035    0.0007769
  -0.0140030    0.0006660
  -0.0150025    0.0005550
  -0.0160020    0.0004440
  -0.0170015    0.0003330
  -0.0180010    0.0002220
  -0.0190005    0.0001110
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0024210
  -0.0010095    0.0022993
  -0.0020090    0.0021776
  -0.0030085    0.0020559
  -0.0040080    0.0019343
  -0.0050075    0.0018126
  -0.0060070    0.0016909
  -0.0070065    0.0015693
  -0.0080060    0.0014476
  -0.0090055    0.0013259
  -0.0100050    0.0012043
  -0.0110045    0.0010838
  -0.0120040    0.0009634
  -0.0130035    0.0008430
  -0.0140030    0.0007226
  -0.0150025    0.0006021
  -0.0160020    0.0004817
  -0.0170015    0.0003613
  -0.0180010    0.0002409
  -0.0190005    0.0001204
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0027679
  -0.0010095    0.0026289
  -0.0020090    0.0024898
  -0.0030085    0.0023508
  -0.0040080    0.0022118
  -0.0050075    0.0020728
  -0.0060070    0.0019338
  -0.0070065    0.0017948
  -0.0080060    0.0016557
  -0.0090055    0.0015167
  -0.0100050    0.0013777
  -0.0110045    0.0012399
  -0.0120040    0.0011022
  -0.0130035    0.0009644
  -0.0140030    0.0008266
  -0.0150025    0.0006889
  -0.0160020    0.0005511
  -0.0170015    0.0004133
  -0.0180010    0.0002755
  -0.0190005    0.0001378
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0030909
  -0.0010095    0.0029357
  -0.0020090    0.0027805
  -0.0030085    0.0026254
  -0.0040080    0.0024702
  -0.0050075    0.0023150
  -0.0060070    0.0021599
  -0.0070065    0.0020047
  -0.0080060    0.0018495
  -0.0090055    0.0016944
  -0.0100050    0.0015392
  -0.0110045    0.0013853
  -0.0120040    0.0012314
  -0.0130035    0.0010775
  -0.0140030    0.0009235
  -0.0150025    0.0007696
  -0.0160020    0.0006157
  -0.0170015    0.0004618
  -0.0180010    0.0003078
  -0.0190005    0.0001539
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100    0.0034437
  -0.0010095    0.0032709
  -0.0020090    0.0030981
  -0.0030085    0.0029253
  -0.0040080    0.0027525
  -0.0050075    0.0025797
  -0.0060070    0.0024069
  -0.0070065    0.0022341
  -0.0080060    0.0020613
  -0.0090055    0.0018885
  -0.0100050    0.0017157
  -0.0110045    0.0015441
  -0.0120040    0.0013726
  -0.0130035    0.0012010
  -0.0140030    0.0010294
  -0.0150025    0.0008579
  -0.0160020    0.0006863
  -0.0170015    0.0005147
  -0.0180010    0.0003431
  -0.0190005    0.0001716
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0039289
  -0.0010095    0.0037319
  -0.0020090    0.0035348
  -0.0030085    0.0033378
  -0.0040080    0.0031407
  -0.0050075    0.0029437
  -0.0060070    0.0027466
  -0.0070065    0.0025496
  -0.0080060    0.0023526
  -0.0090055    0.0021555
  -0.0100050    0.0019585
  -0.0110045    0.0017626
  -0.0120040    0.0015668
  -0.0130035    0.0013709
  -0.0140030    0.0011751
  -0.0150025    0.0009792
  -0.0160020    0.0007834
  -0.0170015    0.0005875
  -0.0180010    0.0003917
  -0.0190005    0.0001958
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0042979
  -0.0010095    0.0040824
  -0.0020090    0.0038670
  -0.0030085    0.0036515
  -0.0040080    0.0034360
  -0.0050075    0.0032205
  -0.0060070    0.0030050
  -0.0070065    0.0027896
  -0.0080060    0.0025741
  -0.0090055    0.0023586
  -0.0100050    0.0021431
  -0.0110045    0.0019288
  -0.0120040    0.0017145
  -0.0130035    0.0015002
  -0.0140030    0.0012859
  -0.0150025    0.0010716
  -0.0160020    0.0008572
  -0.0170015    0.0006429
  -0.0180010    0.0004286
  -0.0190005    0.0002143
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0046630
  -0.0010095    0.0044293
  -0.0020090    0.0041956
  -0.0030085    0.0039619
  -0.0040080    0.0037281
  -0.0050075    0.0034944
  -0.0060070    0.0032607
  -0.0070065    0.0030270
  -0.0080060    0.0027932
  -0.0090055    0.0025595
  -0.0100050    0.0023258
  -0.0110045    0.0020932
  -0.0120040    0.0018606
  -0.0130035    0.0016281
  -0.0140030    0.0013955
  -0.0150025    0.0011629
  -0.0160020    0.0009303
  -0.0170015    0.0006977
  -0.0180010    0.0004652
  -0.0190005    0.0002326
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0051359
  -0.0010095    0.0048785
  -0.0020090    0.0046212
  -0.0030085    0.0043638
  -0.0040080    0.0041065
  -0.0050075    0.0038491
  -0.0060070    0.0035918
  -0.0070065    0.0033344
  -0.0080060    0.0030771
  -0.0090055    0.0028197
  -0.0100050    0.0025624
  -0.0110045    0.0023061
  -0.0120040    0.0020499
  -0.0130035    0.0017937
  -0.0140030    0.0015374
  -0.0150025    0.0012812
  -0.0160020    0.0010250
  -0.0170015    0.0007687
  -0.0180010    0.0005125
  -0.0190005    0.0002562
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0053734
  -0.0010095    0.0051042
  -0.0020090    0.0048350
  -0.0030085    0.0045658
  -0.0040080    0.0042965
  -0.0050075    0.0040273
  -0.0060070    0.0037581
  -0.0070065    0.0034889
  -0.0080060    0.0032197
  -0.0090055    0.0029505
  -0.0100050    0.0026812
  -0.0110045    0.0024131
  -0.0120040    0.0021450
  -0.0130035    0.0018769
  -0.0140030    0.0016087
  -0.0150025    0.0013406
  -0.0160020    0.0010725
  -0.0170015    0.0008044
  -0.0180010    0.0005362
  -0.0190005    0.0002681
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
   0.1000000      0.9959843   
   0.2008680      0.9984743   
   0.3280799      0.9988181   
   0.4885161      0.9990619   
   0.6908539      0.9992491   
   0.9460369      0.9993952   
   1.2678666      0.9995107   
   1.6737496      0.9996029   
   2.1856381      0.9996769   
   2.8312180      0.9997366   
   3.6454059      0.9997850   
   4.6722374      0.9998243   
   5.9672493      0.9998564   
   7.6004832      0.9998825   
   9.6602733      0.9999038   
  12.2580245      0.9999213   
  15.5342377      0.9999356   
  19.6661086      0.9999473   
  24.8771118      0.9999569   
  31.4490873      0.9999647   
  39.7374840      0.9999711   
  50.1905843      0.9999764   
  63.3737500      0.9999807   
  80.0000000      0.9999842   
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
