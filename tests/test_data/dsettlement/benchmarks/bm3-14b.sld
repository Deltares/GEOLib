Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 10/08/2023
TIME       : 07:52:46
FILENAME   : C:\Deltares\D-Settlement\Benchmarks\bm3-14b.sld
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
Clay
SoilColor=9764853
SoilGamDry=15.00
SoilGamWet=18.00
SoilInitialVoidRatio=0.000000
SoilPreconIsotacheType=0
SoilPreconKoppejanType=1
SoilUseEquivalentAge=0
SoilEquivalentAge=6.03E+00
SoilPc=0.00E+00
SoilOCR=1.20
SoilPOP=4.00
SoilDrained=0
SoilApAsApproximationByCpCs=0
SoilSecondarySwellingReduced=0
SoilSecondarySwellingFactor=1.00
SoilUnloadingStressRatio=1.01
SoilCv=1.00E-10
SoilPermeabilityVer=1.000E+00
SoilPermeabilityHorFactor=0.150
SoilStorageType=1
SoilPermeabilityStrainModulus=1.000E+15
SoilUseProbDefaults=1
SoilStdGamDry=0.75
SoilStdGamWet=0.90
SoilStdCv=5.00E-11
SoilStdPc=0.00E+00
SoilStdPriCompIndex=2.500E-03
SoilStdSecCompIndex=2.500E-02
SoilStdSecCompRate=1.000E-02
SoilStdOCR=0.30
SoilStdPermeabilityVer=2.500E+00
SoilStdPOP=1.00
SoilStdPermeabilityHorFactor=0.038
SoilStdInitialVoidRatio=0.000000
SoilStdPermeabilityStrainModulus=0.000E+00
SoilStdLimitStress=0.00
SoilStdCp=5.70E-01
SoilStdCp1=3.00E+00
SoilStdCs=1.50E+01
SoilStdCs1=3.00E+01
SoilStdAp=3.00E+00
SoilStdAsec=3.00E+01
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
SoilCp=1.90E+00
SoilCp1=1.00E+01
SoilCs=5.00E+01
SoilCs1=1.00E+02
SoilAp=1.00E+01
SoilAsec=1.00E+02
SoilCar=0.0000000
SoilCa=0.0000000
SoilCompRatio=1
SoilRRatio=0.0000000
SoilCRatio=0.0000000
SoilSRatio=0.0000000
SoilCrIndex=0.0000000
SoilCcIndex=0.0000000
SoilCswIndex=0.0000000
SoilPriCompIndex=1.000E-02
SoilSecCompIndex=1.000E-01
SoilSecCompRate=4.000E-02
SoilHorizontalBehaviourType=1
SoilElasticity=1.00000E+03
SoilDefaultElasticity=1
[END OF SOIL]
[END OF SOIL COLLECTION]
[GEOMETRY 1D DATA]
1
        0.020
Clay
5
        0.040
        0.000
        0.000
        0.000
1
1
 0.00000000000000E+0000
 0.00000000000000E+0000
 1.00000000000000E+0000
[END OF GEOMETRY 1D DATA]
[RUN IDENTIFICATION]
Benchmark MSettle: bm3-14b
Effect of dispersion conditions layer boundaries
Undrained at both sides
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
    9 = number of items
Initial load
3 : Uniform
          -1        20.00        0.010        0.020 = Time, Gamma, H, Yapplication
1
3 : Uniform
           0       100.00        0.050        0.020 = Time, Gamma, H, Yapplication
2
3 : Uniform
          10      -100.00        0.050        0.020 = Time, Gamma, H, Yapplication
3
3 : Uniform
          20       100.00        0.050        0.020 = Time, Gamma, H, Yapplication
4
3 : Uniform
          30       100.00        0.050        0.020 = Time, Gamma, H, Yapplication
5
3 : Uniform
          40      -100.00        0.050        0.020 = Time, Gamma, H, Yapplication
6
3 : Uniform
          50       100.00        0.050        0.020 = Time, Gamma, H, Yapplication
7
3 : Uniform
          60       100.00        0.100        0.020 = Time, Gamma, H, Yapplication
8
3 : Uniform
          70       100.00        0.200        0.020 = Time, Gamma, H, Yapplication
[END OF OTHER LOADS]
[CALCULATION OPTIONS]
0 : Precon. pressure within a layer = Constant (constant in the layers)
0 : Imaginary surface = FALSE
0 : Submerging = FALSE
0 : Use end time for fit = FALSE
0 : Maintain profile = FALSE
Superelevation
     0 = Time superelevation
    10.00 = Gamma dry superelevation
    10.00 = Gamma wet superelevation
0 : Dispersion conditions layer boundaries top = undrained
0 : Dispersion conditions layer boundaries bottom = undrained
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
 1.00000000000000E+0000 = Number of subtime steps
4.000000000E+000 = Reference time
1 : Dissipation = TRUE
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
    121  =  Time step count 
      8  =  Load step count 
   0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000   
   0.1000000      0.0000658      0.0000658      0.0000658      0.0000658      0.0000658      0.0000658      0.0000658      0.0000658   
   0.2020378      0.0001105      0.0001105      0.0001105      0.0001105      0.0001105      0.0001105      0.0001105      0.0001105   
   0.3310343      0.0001568      0.0001568      0.0001568      0.0001568      0.0001568      0.0001568      0.0001568      0.0001568   
   0.4941118      0.0002068      0.0002068      0.0002068      0.0002068      0.0002068      0.0002068      0.0002068      0.0002068   
   0.7002747      0.0002617      0.0002617      0.0002617      0.0002617      0.0002617      0.0002617      0.0002617      0.0002617   
   0.9609063      0.0003230      0.0003230      0.0003230      0.0003230      0.0003230      0.0003230      0.0003230      0.0003230   
   1.2903972      0.0003919      0.0003919      0.0003919      0.0003919      0.0003919      0.0003919      0.0003919      0.0003919   
   1.7069403      0.0004697      0.0004697      0.0004697      0.0004697      0.0004697      0.0004697      0.0004697      0.0004697   
   2.2335348      0.0005579      0.0005579      0.0005579      0.0005579      0.0005579      0.0005579      0.0005579      0.0005579   
   2.8992565      0.0006583      0.0006583      0.0006583      0.0006583      0.0006583      0.0006583      0.0006583      0.0006583   
   3.7408633      0.0007727      0.0007727      0.0007727      0.0007727      0.0007727      0.0007727      0.0007727      0.0007727   
   4.8048241      0.0009031      0.0009031      0.0009031      0.0009031      0.0009031      0.0009031      0.0009031      0.0009031   
   6.1498854      0.0010520      0.0010520      0.0010520      0.0010520      0.0010520      0.0010520      0.0010520      0.0010520   
   7.8503144      0.0012222      0.0012222      0.0012222      0.0012222      0.0012222      0.0012222      0.0012222      0.0012222   
  10.0000000      0.0014166      0.0014166      0.0014166      0.0014166      0.0014166      0.0014166      0.0014166      0.0014166   
  10.1000000      0.0014252      0.0014136      0.0014136      0.0014136      0.0014136      0.0014136      0.0014136      0.0014136   
  10.2020378      0.0014339      0.0014172      0.0014172      0.0014172      0.0014172      0.0014172      0.0014172      0.0014172   
  10.3310343      0.0014449      0.0014232      0.0014232      0.0014232      0.0014232      0.0014232      0.0014232      0.0014232   
  10.4941118      0.0014587      0.0014317      0.0014317      0.0014317      0.0014317      0.0014317      0.0014317      0.0014317   
  10.7002747      0.0014761      0.0014431      0.0014431      0.0014431      0.0014431      0.0014431      0.0014431      0.0014431   
  10.9609063      0.0014978      0.0014580      0.0014580      0.0014580      0.0014580      0.0014580      0.0014580      0.0014580   
  11.2903972      0.0015249      0.0014772      0.0014772      0.0014772      0.0014772      0.0014772      0.0014772      0.0014772   
  11.7069403      0.0015588      0.0015016      0.0015016      0.0015016      0.0015016      0.0015016      0.0015016      0.0015016   
  12.2335348      0.0016008      0.0015323      0.0015323      0.0015323      0.0015323      0.0015323      0.0015323      0.0015323   
  12.8992565      0.0016529      0.0015705      0.0015705      0.0015705      0.0015705      0.0015705      0.0015705      0.0015705   
  13.7408633      0.0017172      0.0016177      0.0016177      0.0016177      0.0016177      0.0016177      0.0016177      0.0016177   
  14.8048241      0.0017961      0.0016756      0.0016756      0.0016756      0.0016756      0.0016756      0.0016756      0.0016756   
  16.1498854      0.0018926      0.0017460      0.0017460      0.0017460      0.0017460      0.0017460      0.0017460      0.0017460   
  17.8503144      0.0020098      0.0018309      0.0018309      0.0018309      0.0018309      0.0018309      0.0018309      0.0018309   
  20.0000000      0.0021513      0.0019325      0.0019325      0.0019325      0.0019325      0.0019325      0.0019325      0.0019325   
  20.1000000      0.0021577      0.0019371      0.0019487      0.0019487      0.0019487      0.0019487      0.0019487      0.0019487   
  20.2020378      0.0021643      0.0019418      0.0019585      0.0019585      0.0019585      0.0019585      0.0019585      0.0019585   
  20.3310343      0.0021725      0.0019477      0.0019694      0.0019694      0.0019694      0.0019694      0.0019694      0.0019694   
  20.4941118      0.0021829      0.0019551      0.0019821      0.0019821      0.0019821      0.0019821      0.0019821      0.0019821   
  20.7002747      0.0021960      0.0019644      0.0019974      0.0019974      0.0019974      0.0019974      0.0019974      0.0019974   
  20.9609063      0.0022125      0.0019761      0.0020159      0.0020159      0.0020159      0.0020159      0.0020159      0.0020159   
  21.2903972      0.0022332      0.0019908      0.0020386      0.0020386      0.0020386      0.0020386      0.0020386      0.0020386   
  21.7069403      0.0022591      0.0020093      0.0020664      0.0020664      0.0020664      0.0020664      0.0020664      0.0020664   
  22.2335348      0.0022917      0.0020323      0.0021009      0.0021009      0.0021009      0.0021009      0.0021009      0.0021009   
  22.8992565      0.0023323      0.0020611      0.0021435      0.0021435      0.0021435      0.0021435      0.0021435      0.0021435   
  23.7408633      0.0023830      0.0020968      0.0021962      0.0021962      0.0021962      0.0021962      0.0021962      0.0021962   
  24.8048241      0.0024460      0.0021410      0.0022615      0.0022615      0.0022615      0.0022615      0.0022615      0.0022615   
  26.1498854      0.0025239      0.0021956      0.0023421      0.0023421      0.0023421      0.0023421      0.0023421      0.0023421   
  27.8503144      0.0026200      0.0022624      0.0024412      0.0024412      0.0024412      0.0024412      0.0024412      0.0024412   
  30.0000000      0.0027378      0.0023440      0.0025627      0.0025627      0.0025627      0.0025627      0.0025627      0.0025627   
  30.1000000      0.0027432      0.0023477      0.0025682      0.0025709      0.0025709      0.0025709      0.0025709      0.0025709   
  30.2020378      0.0027486      0.0023515      0.0025739      0.0025781      0.0025781      0.0025781      0.0025781      0.0025781   
  30.3310343      0.0027556      0.0023563      0.0025810      0.0025870      0.0025870      0.0025870      0.0025870      0.0025870   
  30.4941118      0.0027643      0.0023623      0.0025900      0.0025981      0.0025981      0.0025981      0.0025981      0.0025981   
  30.7002747      0.0027753      0.0023699      0.0026013      0.0026122      0.0026122      0.0026122      0.0026122      0.0026122   
  30.9609063      0.0027892      0.0023794      0.0026156      0.0026300      0.0026300      0.0026300      0.0026300      0.0026300   
  31.2903972      0.0028067      0.0023914      0.0026336      0.0026526      0.0026526      0.0026526      0.0026526      0.0026526   
  31.7069403      0.0028286      0.0024065      0.0026562      0.0026811      0.0026811      0.0026811      0.0026811      0.0026811   
  32.2335348      0.0028562      0.0024254      0.0026846      0.0027170      0.0027170      0.0027170      0.0027170      0.0027170   
  32.8992565      0.0028908      0.0024491      0.0027202      0.0027621      0.0027621      0.0027621      0.0027621      0.0027621   
  33.7408633      0.0029340      0.0024787      0.0027647      0.0028186      0.0028186      0.0028186      0.0028186      0.0028186   
  34.8048241      0.0029880      0.0025154      0.0028202      0.0028890      0.0028890      0.0028890      0.0028890      0.0028890   
  36.1498854      0.0030550      0.0025610      0.0028892      0.0029761      0.0029761      0.0029761      0.0029761      0.0029761   
  37.8503144      0.0031382      0.0026173      0.0029746      0.0030833      0.0030833      0.0030833      0.0030833      0.0030833   
  40.0000000      0.0032406      0.0026863      0.0030799      0.0032144      0.0032144      0.0032144      0.0032144      0.0032144   
  40.1000000      0.0032453      0.0026894      0.0030847      0.0032204      0.0032180      0.0032180      0.0032180      0.0032180   
  40.2020378      0.0032501      0.0026926      0.0030896      0.0032265      0.0032230      0.0032230      0.0032230      0.0032230   
  40.3310343      0.0032561      0.0026967      0.0030958      0.0032342      0.0032295      0.0032295      0.0032295      0.0032295   
  40.4941118      0.0032638      0.0027018      0.0031036      0.0032439      0.0032379      0.0032379      0.0032379      0.0032379   
  40.7002747      0.0032734      0.0027083      0.0031135      0.0032561      0.0032485      0.0032485      0.0032485      0.0032485   
  40.9609063      0.0032855      0.0027164      0.0031260      0.0032715      0.0032621      0.0032621      0.0032621      0.0032621   
  41.2903972      0.0033008      0.0027266      0.0031416      0.0032909      0.0032791      0.0032791      0.0032791      0.0032791   
  41.7069403      0.0033200      0.0027395      0.0031614      0.0033152      0.0033005      0.0033005      0.0033005      0.0033005   
  42.2335348      0.0033441      0.0027556      0.0031862      0.0033458      0.0033273      0.0033273      0.0033273      0.0033273   
  42.8992565      0.0033744      0.0027758      0.0032173      0.0033840      0.0033608      0.0033608      0.0033608      0.0033608   
  43.7408633      0.0034124      0.0028011      0.0032562      0.0034317      0.0034024      0.0034024      0.0034024      0.0034024   
  44.8048241      0.0034598      0.0028326      0.0033049      0.0034912      0.0034540      0.0034540      0.0034540      0.0034540   
  46.1498854      0.0035189      0.0028718      0.0033655      0.0035651      0.0035177      0.0035177      0.0035177      0.0035177   
  47.8503144      0.0035921      0.0029201      0.0034408      0.0036563      0.0035961      0.0035961      0.0035961      0.0035961   
  50.0000000      0.0036827      0.0029796      0.0035337      0.0037686      0.0036919      0.0036919      0.0036919      0.0036919   
  50.1000000      0.0036868      0.0029824      0.0035380      0.0037737      0.0036963      0.0036987      0.0036987      0.0036987   
  50.2020378      0.0036910      0.0029851      0.0035423      0.0037789      0.0037008      0.0037043      0.0037043      0.0037043   
  50.3310343      0.0036964      0.0029886      0.0035478      0.0037855      0.0037064      0.0037111      0.0037111      0.0037111   
  50.4941118      0.0037031      0.0029931      0.0035547      0.0037939      0.0037135      0.0037194      0.0037194      0.0037194   
  50.7002747      0.0037116      0.0029986      0.0035635      0.0038044      0.0037225      0.0037298      0.0037298      0.0037298   
  50.9609063      0.0037224      0.0030056      0.0035745      0.0038176      0.0037337      0.0037429      0.0037429      0.0037429   
  51.2903972      0.0037359      0.0030145      0.0035883      0.0038343      0.0037479      0.0037592      0.0037592      0.0037592   
  51.7069403      0.0037529      0.0030256      0.0036058      0.0038553      0.0037658      0.0037798      0.0037798      0.0037798   
  52.2335348      0.0037743      0.0030395      0.0036278      0.0038816      0.0037882      0.0038056      0.0038056      0.0038056   
  52.8992565      0.0038011      0.0030570      0.0036553      0.0039147      0.0038162      0.0038380      0.0038380      0.0038380   
  53.7408633      0.0038347      0.0030789      0.0036899      0.0039560      0.0038513      0.0038787      0.0038787      0.0038787   
  54.8048241      0.0038768      0.0031062      0.0037330      0.0040077      0.0038951      0.0039297      0.0039297      0.0039297   
  56.1498854      0.0039292      0.0031401      0.0037869      0.0040719      0.0039495      0.0039934      0.0039934      0.0039934   
  57.8503144      0.0039942      0.0031821      0.0038537      0.0041515      0.0040168      0.0040727      0.0040727      0.0040727   
  60.0000000      0.0040746      0.0032337      0.0039364      0.0042497      0.0040998      0.0041708      0.0041708      0.0041708   
  60.1000000      0.0040783      0.0032361      0.0039402      0.0042542      0.0041036      0.0041753      0.0041778      0.0041778   
  60.2020378      0.0040821      0.0032385      0.0039440      0.0042588      0.0041075      0.0041799      0.0041837      0.0041837   
  60.3310343      0.0040868      0.0032415      0.0039489      0.0042646      0.0041124      0.0041857      0.0041910      0.0041910   
  60.4941118      0.0040928      0.0032453      0.0039551      0.0042719      0.0041186      0.0041930      0.0042001      0.0042001   
  60.7002747      0.0041004      0.0032502      0.0039628      0.0042811      0.0041263      0.0042023      0.0042116      0.0042116   
  60.9609063      0.0041099      0.0032563      0.0039726      0.0042927      0.0041362      0.0042139      0.0042261      0.0042261   
  61.2903972      0.0041219      0.0032640      0.0039850      0.0043073      0.0041485      0.0042286      0.0042445      0.0042445   
  61.7069403      0.0041370      0.0032736      0.0040005      0.0043258      0.0041641      0.0042471      0.0042677      0.0042677   
  62.2335348      0.0041560      0.0032857      0.0040201      0.0043489      0.0041836      0.0042703      0.0042970      0.0042970   
  62.8992565      0.0041799      0.0033009      0.0040446      0.0043779      0.0042081      0.0042995      0.0043340      0.0043340   
  63.7408633      0.0042098      0.0033199      0.0040754      0.0044143      0.0042388      0.0043360      0.0043805      0.0043805   
  64.8048241      0.0042472      0.0033437      0.0041139      0.0044598      0.0042771      0.0043817      0.0044387      0.0044387   
  66.1498854      0.0042938      0.0033732      0.0041618      0.0045164      0.0043248      0.0044387      0.0045112      0.0045112   
  67.8503144      0.0043516      0.0034097      0.0042214      0.0045866      0.0043840      0.0045095      0.0046009      0.0046009   
  70.0000000      0.0044232      0.0034546      0.0042951      0.0046733      0.0044571      0.0045969      0.0047112      0.0047112   
  70.1000000      0.0044264      0.0034567      0.0042985      0.0046773      0.0044605      0.0046010      0.0047163      0.0047188   
  70.2020378      0.0044298      0.0034588      0.0043020      0.0046814      0.0044639      0.0046051      0.0047214      0.0047255   
  70.3310343      0.0044340      0.0034614      0.0043063      0.0046865      0.0044682      0.0046102      0.0047279      0.0047337   
  70.4941118      0.0044393      0.0034648      0.0043118      0.0046930      0.0044736      0.0046167      0.0047361      0.0047442   
  70.7002747      0.0044461      0.0034690      0.0043187      0.0047011      0.0044805      0.0046250      0.0047464      0.0047574   
  70.9609063      0.0044546      0.0034743      0.0043275      0.0047114      0.0044891      0.0046353      0.0047594      0.0047741   
  71.2903972      0.0044652      0.0034810      0.0043385      0.0047243      0.0045000      0.0046484      0.0047758      0.0047953   
  71.7069403      0.0044787      0.0034894      0.0043524      0.0047406      0.0045138      0.0046649      0.0047964      0.0048220   
  72.2335348      0.0044956      0.0034999      0.0043698      0.0047611      0.0045310      0.0046855      0.0048223      0.0048557   
  72.8992565      0.0045168      0.0035132      0.0043917      0.0047868      0.0045526      0.0047115      0.0048547      0.0048979   
  73.7408633      0.0045434      0.0035297      0.0044191      0.0048190      0.0045797      0.0047440      0.0048952      0.0049506   
  74.8048241      0.0045767      0.0035504      0.0044535      0.0048593      0.0046136      0.0047847      0.0049457      0.0050160   
  76.1498854      0.0046182      0.0035761      0.0044963      0.0049094      0.0046558      0.0048354      0.0050085      0.0050966   
  77.8503144      0.0046697      0.0036079      0.0045494      0.0049717      0.0047081      0.0048984      0.0050863      0.0051953   
  80.0000000      0.0047334      0.0036471      0.0046152      0.0050486      0.0047728      0.0049762      0.0051820      0.0053156   
[End of Time-Settlement per Load]
[Depths]
      3    =  Depth count
   0.0199900
   0.0100000
   0.0000000
[End of Depths]
[Stresses]
[Column Indication]
Initial total stress
Initial water stress
Final total stress
Final water stress
[End of Column Indication]
[Stress Data]
      3  =  Depth step count 
   0.4001800      0.2001000     40.4533358      0.2532558   
   0.5800000      0.3000000     40.6059603      0.3259603   
   0.7600000      0.4000000     40.7600000      0.4000000   
[End of Stress Data]
[End of Stresses]
[Time-dependent Data]
[Column Indication]
Settlement
Loading
[End of Column Indication]
[Vertical Data at Time]
   0.000000000000    =  Time in days
   0.0000000    0.2000800
   0.0000000    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.100000000000    =  Time in days
   0.0000658    5.2000800
   0.0000300    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.202037840055    =  Time in days
   0.0001105    5.2000800
   0.0000511    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.331034271074    =  Time in days
   0.0001568    5.2000800
   0.0000731    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.494111803945    =  Time in days
   0.0002068    5.2000800
   0.0000970    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.700274730448    =  Time in days
   0.0002617    5.2000800
   0.0001233    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.960906293338    =  Time in days
   0.0003230    5.2000800
   0.0001528    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.290397209704    =  Time in days
   0.0003919    5.2000800
   0.0001859    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.706940251398    =  Time in days
   0.0004697    5.2000800
   0.0002235    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.233534755119    =  Time in days
   0.0005579    5.2000800
   0.0002661    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.899256525960    =  Time in days
   0.0006583    5.2000800
   0.0003146    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.740863251897    =  Time in days
   0.0007727    5.2000800
   0.0003700    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.804824071816    =  Time in days
   0.0009031    5.2000800
   0.0004332    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.149885359274    =  Time in days
   0.0010520    5.2000800
   0.0005055    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.850314391197    =  Time in days
   0.0012222    5.2000800
   0.0005881    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.000000000000    =  Time in days
   0.0014166    5.2000800
   0.0006826    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.100000000000    =  Time in days
   0.0014136    0.2000800
   0.0006812    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.202037840055    =  Time in days
   0.0014172    0.2000800
   0.0006830    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.331034271074    =  Time in days
   0.0014232    0.2000800
   0.0006859    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.494111803945    =  Time in days
   0.0014317    0.2000800
   0.0006900    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.700274730448    =  Time in days
   0.0014431    0.2000800
   0.0006955    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  10.960906293338    =  Time in days
   0.0014580    0.2000800
   0.0007027    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  11.290397209704    =  Time in days
   0.0014772    0.2000800
   0.0007121    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  11.706940251398    =  Time in days
   0.0015016    0.2000800
   0.0007239    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  12.233534755119    =  Time in days
   0.0015323    0.2000800
   0.0007387    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  12.899256525960    =  Time in days
   0.0015705    0.2000800
   0.0007572    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  13.740863251897    =  Time in days
   0.0016177    0.2000800
   0.0007801    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  14.804824071816    =  Time in days
   0.0016756    0.2000800
   0.0008081    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  16.149885359274    =  Time in days
   0.0017460    0.2000800
   0.0008421    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  17.850314391197    =  Time in days
   0.0018309    0.2000800
   0.0008831    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.000000000000    =  Time in days
   0.0019325    0.2000800
   0.0009321    0.2800000
   0.0000000    0.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.100000000000    =  Time in days
   0.0019487    5.2000800
   0.0009400    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.202037840055    =  Time in days
   0.0019585    5.2000800
   0.0009447    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.331034271074    =  Time in days
   0.0019694    5.2000800
   0.0009500    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.494111803945    =  Time in days
   0.0019821    5.2000800
   0.0009562    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.700274730448    =  Time in days
   0.0019974    5.2000800
   0.0009635    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  20.960906293338    =  Time in days
   0.0020159    5.2000800
   0.0009725    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  21.290397209704    =  Time in days
   0.0020386    5.2000800
   0.0009835    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  21.706940251398    =  Time in days
   0.0020664    5.2000800
   0.0009971    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  22.233534755119    =  Time in days
   0.0021009    5.2000800
   0.0010138    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  22.899256525960    =  Time in days
   0.0021435    5.2000800
   0.0010345    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  23.740863251897    =  Time in days
   0.0021962    5.2000800
   0.0010602    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  24.804824071816    =  Time in days
   0.0022615    5.2000800
   0.0010919    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  26.149885359274    =  Time in days
   0.0023421    5.2000800
   0.0011312    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  27.850314391197    =  Time in days
   0.0024412    5.2000800
   0.0011795    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.000000000000    =  Time in days
   0.0025627    5.2000800
   0.0012388    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.100000000000    =  Time in days
   0.0025709   10.2000800
   0.0012428   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.202037840055    =  Time in days
   0.0025781   10.2000800
   0.0012464   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.331034271074    =  Time in days
   0.0025870   10.2000800
   0.0012507   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.494111803945    =  Time in days
   0.0025981   10.2000800
   0.0012562   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.700274730448    =  Time in days
   0.0026122   10.2000800
   0.0012631   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  30.960906293338    =  Time in days
   0.0026300   10.2000800
   0.0012719   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  31.290397209704    =  Time in days
   0.0026526   10.2000800
   0.0012829   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  31.706940251398    =  Time in days
   0.0026811   10.2000800
   0.0012969   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  32.233534755119    =  Time in days
   0.0027170   10.2000800
   0.0013146   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  32.899256525960    =  Time in days
   0.0027621   10.2000800
   0.0013367   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  33.740863251897    =  Time in days
   0.0028186   10.2000800
   0.0013645   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  34.804824071816    =  Time in days
   0.0028890   10.2000800
   0.0013991   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  36.149885359274    =  Time in days
   0.0029761   10.2000800
   0.0014419   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  37.850314391197    =  Time in days
   0.0030833   10.2000800
   0.0014946   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.000000000000    =  Time in days
   0.0032144   10.2000800
   0.0015591   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.100000000000    =  Time in days
   0.0032180    5.2000800
   0.0015608    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.202037840055    =  Time in days
   0.0032230    5.2000800
   0.0015632    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.331034271074    =  Time in days
   0.0032295    5.2000800
   0.0015664    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.494111803945    =  Time in days
   0.0032379    5.2000800
   0.0015705    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.700274730448    =  Time in days
   0.0032485    5.2000800
   0.0015757    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  40.960906293338    =  Time in days
   0.0032621    5.2000800
   0.0015823    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  41.290397209704    =  Time in days
   0.0032791    5.2000800
   0.0015907    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  41.706940251398    =  Time in days
   0.0033005    5.2000800
   0.0016012    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  42.233534755119    =  Time in days
   0.0033273    5.2000800
   0.0016143    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  42.899256525960    =  Time in days
   0.0033608    5.2000800
   0.0016307    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  43.740863251897    =  Time in days
   0.0034024    5.2000800
   0.0016511    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  44.804824071816    =  Time in days
   0.0034540    5.2000800
   0.0016763    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  46.149885359274    =  Time in days
   0.0035177    5.2000800
   0.0017075    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  47.850314391197    =  Time in days
   0.0035961    5.2000800
   0.0017459    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.000000000000    =  Time in days
   0.0036919    5.2000800
   0.0017928    5.2800000
   0.0000000    5.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.100000000000    =  Time in days
   0.0036987   10.2000800
   0.0017961   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.202037840055    =  Time in days
   0.0037043   10.2000800
   0.0017989   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.331034271074    =  Time in days
   0.0037111   10.2000800
   0.0018022   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.494111803945    =  Time in days
   0.0037194   10.2000800
   0.0018063   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.700274730448    =  Time in days
   0.0037298   10.2000800
   0.0018114   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  50.960906293338    =  Time in days
   0.0037429   10.2000800
   0.0018178   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  51.290397209704    =  Time in days
   0.0037592   10.2000800
   0.0018259   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  51.706940251398    =  Time in days
   0.0037798   10.2000800
   0.0018360   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  52.233534755119    =  Time in days
   0.0038056   10.2000800
   0.0018486   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  52.899256525960    =  Time in days
   0.0038380   10.2000800
   0.0018646   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  53.740863251897    =  Time in days
   0.0038787   10.2000800
   0.0018846   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  54.804824071816    =  Time in days
   0.0039297   10.2000800
   0.0019096   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  56.149885359274    =  Time in days
   0.0039934   10.2000800
   0.0019410   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  57.850314391197    =  Time in days
   0.0040727   10.2000800
   0.0019799   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.000000000000    =  Time in days
   0.0041708   10.2000800
   0.0020282   10.2800000
   0.0000000   10.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.100000000000    =  Time in days
   0.0041778   20.2000800
   0.0020317   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.202037840055    =  Time in days
   0.0041837   20.2000800
   0.0020346   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.331034271074    =  Time in days
   0.0041910   20.2000800
   0.0020382   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.494111803945    =  Time in days
   0.0042001   20.2000800
   0.0020427   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.700274730448    =  Time in days
   0.0042116   20.2000800
   0.0020484   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  60.960906293338    =  Time in days
   0.0042261   20.2000800
   0.0020555   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  61.290397209704    =  Time in days
   0.0042445   20.2000800
   0.0020646   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  61.706940251398    =  Time in days
   0.0042677   20.2000800
   0.0020761   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  62.233534755119    =  Time in days
   0.0042970   20.2000800
   0.0020906   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  62.899256525960    =  Time in days
   0.0043340   20.2000800
   0.0021089   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  63.740863251897    =  Time in days
   0.0043805   20.2000800
   0.0021319   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  64.804824071816    =  Time in days
   0.0044387   20.2000800
   0.0021607   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  66.149885359274    =  Time in days
   0.0045112   20.2000800
   0.0021965   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  67.850314391197    =  Time in days
   0.0046009   20.2000800
   0.0022409   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.000000000000    =  Time in days
   0.0047112   20.2000800
   0.0022955   20.2800000
   0.0000000   20.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.100000000000    =  Time in days
   0.0047188   40.2000800
   0.0022993   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.202037840055    =  Time in days
   0.0047255   40.2000800
   0.0023026   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.331034271074    =  Time in days
   0.0047337   40.2000800
   0.0023067   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.494111803945    =  Time in days
   0.0047442   40.2000800
   0.0023119   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.700274730448    =  Time in days
   0.0047574   40.2000800
   0.0023184   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  70.960906293338    =  Time in days
   0.0047741   40.2000800
   0.0023268   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  71.290397209704    =  Time in days
   0.0047953   40.2000800
   0.0023373   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  71.706940251398    =  Time in days
   0.0048220   40.2000800
   0.0023506   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  72.233534755119    =  Time in days
   0.0048557   40.2000800
   0.0023674   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  72.899256525960    =  Time in days
   0.0048979   40.2000800
   0.0023884   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  73.740863251897    =  Time in days
   0.0049506   40.2000800
   0.0024145   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  74.804824071816    =  Time in days
   0.0050160   40.2000800
   0.0024470   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  76.149885359274    =  Time in days
   0.0050966   40.2000800
   0.0024871   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  77.850314391197    =  Time in days
   0.0051953   40.2000800
   0.0025362   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[Vertical Data at Time]
  80.000000000000    =  Time in days
   0.0053156   40.2000800
   0.0025960   40.2800000
   0.0000000   40.3600000
[End of Vertical Data at Time]
[End of Time dependent Data]
[Time-dependent Data]
[Column Indication]
Depth
Settlement
[End of Column Indication]
[Vertical Data at Fixed Time]
   0.001000000000    =  Time in days
   0.0199900    0.0000007
   0.0189905    0.0000006
   0.0179910    0.0000006
   0.0169915    0.0000006
   0.0159920    0.0000005
   0.0149925    0.0000005
   0.0139930    0.0000004
   0.0129935    0.0000004
   0.0119940    0.0000004
   0.0109945    0.0000003
   0.0099950    0.0000003
   0.0089955    0.0000003
   0.0079960    0.0000002
   0.0069965    0.0000002
   0.0059970    0.0000002
   0.0049975    0.0000001
   0.0039980    0.0000001
   0.0029985    0.0000001
   0.0019990    0.0000001
   0.0009995    0.0000000
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
   0.0199900    0.0000013
   0.0189905    0.0000012
   0.0179910    0.0000012
   0.0169915    0.0000011
   0.0159920    0.0000010
   0.0149925    0.0000010
   0.0139930    0.0000009
   0.0129935    0.0000008
   0.0119940    0.0000007
   0.0109945    0.0000007
   0.0099950    0.0000006
   0.0089955    0.0000005
   0.0079960    0.0000005
   0.0069965    0.0000004
   0.0059970    0.0000004
   0.0049975    0.0000003
   0.0039980    0.0000002
   0.0029985    0.0000002
   0.0019990    0.0000001
   0.0009995    0.0000001
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
   0.0199900    0.0000033
   0.0189905    0.0000031
   0.0179910    0.0000029
   0.0169915    0.0000028
   0.0159920    0.0000026
   0.0149925    0.0000024
   0.0139930    0.0000022
   0.0129935    0.0000020
   0.0119940    0.0000019
   0.0109945    0.0000017
   0.0099950    0.0000015
   0.0089955    0.0000013
   0.0079960    0.0000012
   0.0069965    0.0000010
   0.0059970    0.0000009
   0.0049975    0.0000007
   0.0039980    0.0000006
   0.0029985    0.0000004
   0.0019990    0.0000003
   0.0009995    0.0000001
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
   0.0199900    0.0000066
   0.0189905    0.0000062
   0.0179910    0.0000059
   0.0169915    0.0000055
   0.0159920    0.0000051
   0.0149925    0.0000048
   0.0139930    0.0000044
   0.0129935    0.0000041
   0.0119940    0.0000037
   0.0109945    0.0000034
   0.0099950    0.0000030
   0.0089955    0.0000027
   0.0079960    0.0000024
   0.0069965    0.0000021
   0.0059970    0.0000018
   0.0049975    0.0000015
   0.0039980    0.0000012
   0.0029985    0.0000009
   0.0019990    0.0000006
   0.0009995    0.0000003
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
   0.0199900    0.0000132
   0.0189905    0.0000124
   0.0179910    0.0000117
   0.0169915    0.0000110
   0.0159920    0.0000103
   0.0149925    0.0000096
   0.0139930    0.0000089
   0.0129935    0.0000081
   0.0119940    0.0000074
   0.0109945    0.0000067
   0.0099950    0.0000060
   0.0089955    0.0000054
   0.0079960    0.0000048
   0.0069965    0.0000042
   0.0059970    0.0000036
   0.0049975    0.0000030
   0.0039980    0.0000024
   0.0029985    0.0000018
   0.0019990    0.0000012
   0.0009995    0.0000006
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
   0.0199900    0.0000329
   0.0189905    0.0000311
   0.0179910    0.0000293
   0.0169915    0.0000275
   0.0159920    0.0000257
   0.0149925    0.0000239
   0.0139930    0.0000221
   0.0129935    0.0000203
   0.0119940    0.0000186
   0.0109945    0.0000168
   0.0099950    0.0000150
   0.0089955    0.0000135
   0.0079960    0.0000120
   0.0069965    0.0000105
   0.0059970    0.0000090
   0.0049975    0.0000075
   0.0039980    0.0000060
   0.0029985    0.0000045
   0.0019990    0.0000030
   0.0009995    0.0000015
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
   0.0199900    0.0000658
   0.0189905    0.0000622
   0.0179910    0.0000586
   0.0169915    0.0000550
   0.0159920    0.0000514
   0.0149925    0.0000479
   0.0139930    0.0000443
   0.0129935    0.0000407
   0.0119940    0.0000371
   0.0109945    0.0000335
   0.0099950    0.0000300
   0.0089955    0.0000270
   0.0079960    0.0000240
   0.0069965    0.0000210
   0.0059970    0.0000180
   0.0049975    0.0000150
   0.0039980    0.0000120
   0.0029985    0.0000090
   0.0019990    0.0000060
   0.0009995    0.0000030
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
   0.0199900    0.0001099
   0.0189905    0.0001039
   0.0179910    0.0000980
   0.0169915    0.0000921
   0.0159920    0.0000862
   0.0149925    0.0000803
   0.0139930    0.0000744
   0.0129935    0.0000685
   0.0119940    0.0000626
   0.0109945    0.0000567
   0.0099950    0.0000508
   0.0089955    0.0000457
   0.0079960    0.0000406
   0.0069965    0.0000355
   0.0059970    0.0000305
   0.0049975    0.0000254
   0.0039980    0.0000203
   0.0029985    0.0000152
   0.0019990    0.0000102
   0.0009995    0.0000051
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
   0.0199900    0.0002086
   0.0189905    0.0001975
   0.0179910    0.0001865
   0.0169915    0.0001754
   0.0159920    0.0001643
   0.0149925    0.0001532
   0.0139930    0.0001422
   0.0129935    0.0001311
   0.0119940    0.0001200
   0.0109945    0.0001089
   0.0099950    0.0000978
   0.0089955    0.0000881
   0.0079960    0.0000783
   0.0069965    0.0000685
   0.0059970    0.0000587
   0.0049975    0.0000489
   0.0039980    0.0000391
   0.0029985    0.0000294
   0.0019990    0.0000196
   0.0009995    0.0000098
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
   0.0199900    0.0003323
   0.0189905    0.0003148
   0.0179910    0.0002973
   0.0169915    0.0002798
   0.0159920    0.0002623
   0.0149925    0.0002447
   0.0139930    0.0002272
   0.0129935    0.0002097
   0.0119940    0.0001922
   0.0109945    0.0001747
   0.0099950    0.0001572
   0.0089955    0.0001415
   0.0079960    0.0001257
   0.0069965    0.0001100
   0.0059970    0.0000943
   0.0049975    0.0000786
   0.0039980    0.0000629
   0.0029985    0.0000472
   0.0019990    0.0000314
   0.0009995    0.0000157
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
   0.0199900    0.0005217
   0.0189905    0.0004944
   0.0179910    0.0004670
   0.0169915    0.0004397
   0.0159920    0.0004124
   0.0149925    0.0003851
   0.0139930    0.0003577
   0.0129935    0.0003304
   0.0119940    0.0003031
   0.0109945    0.0002758
   0.0099950    0.0002484
   0.0089955    0.0002236
   0.0079960    0.0001988
   0.0069965    0.0001739
   0.0059970    0.0001491
   0.0049975    0.0001242
   0.0039980    0.0000994
   0.0029985    0.0000745
   0.0019990    0.0000497
   0.0009995    0.0000248
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
   0.0199900    0.0009271
   0.0189905    0.0008789
   0.0179910    0.0008306
   0.0169915    0.0007824
   0.0159920    0.0007341
   0.0149925    0.0006859
   0.0139930    0.0006376
   0.0129935    0.0005894
   0.0119940    0.0005411
   0.0109945    0.0004929
   0.0099950    0.0004446
   0.0089955    0.0004002
   0.0079960    0.0003557
   0.0069965    0.0003113
   0.0059970    0.0002668
   0.0049975    0.0002223
   0.0039980    0.0001779
   0.0029985    0.0001334
   0.0019990    0.0000889
   0.0009995    0.0000445
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
   0.0199900    0.0014166
   0.0189905    0.0013432
   0.0179910    0.0012697
   0.0169915    0.0011963
   0.0159920    0.0011229
   0.0149925    0.0010494
   0.0139930    0.0009760
   0.0129935    0.0009026
   0.0119940    0.0008291
   0.0109945    0.0007557
   0.0099950    0.0006823
   0.0089955    0.0006140
   0.0079960    0.0005458
   0.0069965    0.0004776
   0.0059970    0.0004094
   0.0049975    0.0003411
   0.0039980    0.0002729
   0.0029985    0.0002047
   0.0019990    0.0001365
   0.0009995    0.0000682
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
   0.0199900    0.0019325
   0.0189905    0.0018324
   0.0179910    0.0017323
   0.0169915    0.0016322
   0.0159920    0.0015322
   0.0149925    0.0014321
   0.0139930    0.0013320
   0.0129935    0.0012319
   0.0119940    0.0011318
   0.0109945    0.0010317
   0.0099950    0.0009317
   0.0089955    0.0008385
   0.0079960    0.0007453
   0.0069965    0.0006522
   0.0059970    0.0005590
   0.0049975    0.0004658
   0.0039980    0.0003727
   0.0029985    0.0002795
   0.0019990    0.0001863
   0.0009995    0.0000932
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
   0.0199900    0.0036919
   0.0189905    0.0035019
   0.0179910    0.0033119
   0.0169915    0.0031219
   0.0159920    0.0029319
   0.0149925    0.0027419
   0.0139930    0.0025519
   0.0129935    0.0023619
   0.0119940    0.0021718
   0.0109945    0.0019818
   0.0099950    0.0017919
   0.0089955    0.0016127
   0.0079960    0.0014335
   0.0069965    0.0012543
   0.0059970    0.0010751
   0.0049975    0.0008959
   0.0039980    0.0007168
   0.0029985    0.0005376
   0.0019990    0.0003584
   0.0009995    0.0001792
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
   0.0199900    0.0053156
   0.0189905    0.0050435
   0.0179910    0.0047714
   0.0169915    0.0044993
   0.0159920    0.0042272
   0.0149925    0.0039551
   0.0139930    0.0036830
   0.0129935    0.0034109
   0.0119940    0.0031388
   0.0109945    0.0028668
   0.0099950    0.0025947
   0.0089955    0.0023353
   0.0079960    0.0020758
   0.0069965    0.0018163
   0.0059970    0.0015568
   0.0049975    0.0012974
   0.0039980    0.0010379
   0.0029985    0.0007784
   0.0019990    0.0005189
   0.0009995    0.0002595
   0.0000000    0.0000000
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
[Dissipation in Layers]
      1  =  Number of Layers 
     25  =  Number of time steps 
[Dissipation layer]
      1  =  Layer Number 
   0.0000000      0.0002026   
   0.1000000      0.0262343   
   0.2008680      0.0371813   
   0.3280799      0.0475181   
   0.4885161      0.0579841   
   0.6908539      0.0689544   
   0.9460369      0.0806906   
   1.2678666      0.0934127   
   1.6737496      0.1073283   
   2.1856381      0.1226474   
   2.8312180      0.1395905   
   3.6454059      0.1583952   
   4.6722374      0.1793212   
   5.9672493      0.2026545   
   7.6004832      0.2287124   
   9.6602733      0.2578480   
  12.2580245      0.2904553   
  15.5342377      0.3269745   
  19.6661086      0.3678960   
  24.8771118      0.4137519   
  31.4490873      0.4650561   
  39.7374840      0.5221265   
  50.1905843      0.5847608   
  63.3737500      0.6518509   
  80.0000000      0.7211219   
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
