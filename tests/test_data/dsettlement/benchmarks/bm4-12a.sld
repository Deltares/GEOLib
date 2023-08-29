Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 10/08/2023
TIME       : 07:53:00
FILENAME   : C:\Deltares\D-Settlement\Benchmarks\bm4-12a.sld
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
SoilPreconIsotacheType=0
SoilPreconKoppejanType=1
SoilUseEquivalentAge=1
SoilEquivalentAge=3.00E+03
SoilPc=1.50E+01
SoilOCR=2.87
SoilPOP=10.00
SoilDrained=0
SoilApAsApproximationByCpCs=0
SoilSecondarySwellingReduced=0
SoilSecondarySwellingFactor=0.50
SoilUnloadingStressRatio=2.00
SoilCv=1.44E-06
SoilPermeabilityVer=1.244E-03
SoilPermeabilityHorFactor=3.000
SoilStorageType=0
SoilPermeabilityStrainModulus=1.000E+15
SoilUseProbDefaults=1
SoilStdGamDry=0.70
SoilStdGamWet=0.70
SoilStdCv=7.20E-07
SoilStdPc=3.75E+00
SoilStdPriCompIndex=5.000E-03
SoilStdSecCompIndex=1.000E-01
SoilStdSecCompRate=1.250E-02
SoilStdOCR=0.25
SoilStdPermeabilityVer=3.110E-03
SoilStdPOP=2.50
SoilStdPermeabilityHorFactor=0.750
SoilStdInitialVoidRatio=0.000000
SoilStdPermeabilityStrainModulus=0.000E+00
SoilStdLimitStress=0.00
SoilStdCp=4.50E+00
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
SoilCp=1.50E+01
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
SoilPriCompIndex=2.000E-02
SoilSecCompIndex=4.000E-01
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
Benchmark MSettle 4-12a
Influence of the creep rate reference time
Tau_0 = 1 day (i.e. Time unit = days)
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
    9 = number of items
Initial load
3 : Uniform
          -1      1000.00        0.001        0.000 = Time, Gamma, H, Yapplication
Load step 1
3 : Uniform
           0      1000.00        0.001        0.000 = Time, Gamma, H, Yapplication
Load step 2
3 : Uniform
           1      1000.00        0.002        0.000 = Time, Gamma, H, Yapplication
Load step 3
3 : Uniform
           2      1000.00        0.004        0.000 = Time, Gamma, H, Yapplication
Load step 4
3 : Uniform
           3      1000.00        0.008        0.000 = Time, Gamma, H, Yapplication
Load step 5
3 : Uniform
           4      1000.00        0.016        0.000 = Time, Gamma, H, Yapplication
Load step 6
3 : Uniform
           5      1000.00        0.032        0.000 = Time, Gamma, H, Yapplication
Load step 7
3 : Uniform
           6      1000.00        0.064        0.000 = Time, Gamma, H, Yapplication
Load step 8
3 : Uniform
           7      1000.00        0.128        0.000 = Time, Gamma, H, Yapplication
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
8 = End of consolidation [days]
 1.00000000000000E-0002 = Number of subtime steps
1.000000000E+000 = Reference time
0 : Dissipation = FALSE
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
     49  =  Time step count 
      8  =  Load step count 
   0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000   
   0.1000000      0.0002727      0.0002727      0.0002727      0.0002727      0.0002727      0.0002727      0.0002727      0.0002727   
   0.2050612      0.0002784      0.0002784      0.0002784      0.0002784      0.0002784      0.0002784      0.0002784      0.0002784   
   0.3387023      0.0002855      0.0002855      0.0002855      0.0002855      0.0002855      0.0002855      0.0002855      0.0002855   
   0.5086977      0.0002946      0.0002946      0.0002946      0.0002946      0.0002946      0.0002946      0.0002946      0.0002946   
   0.7249370      0.0003060      0.0003060      0.0003060      0.0003060      0.0003060      0.0003060      0.0003060      0.0003060   
   1.0000000      0.0003202      0.0003202      0.0003202      0.0003202      0.0003202      0.0003202      0.0003202      0.0003202   
   1.1000000      0.0003254      0.0012187      0.0012187      0.0012187      0.0012187      0.0012187      0.0012187      0.0012187   
   1.2050612      0.0003307      0.0016004      0.0016004      0.0016004      0.0016004      0.0016004      0.0016004      0.0016004   
   1.3387023      0.0003375      0.0019253      0.0019253      0.0019253      0.0019253      0.0019253      0.0019253      0.0019253   
   1.5086977      0.0003461      0.0022148      0.0022148      0.0022148      0.0022148      0.0022148      0.0022148      0.0022148   
   1.7249370      0.0003568      0.0024803      0.0024803      0.0024803      0.0024803      0.0024803      0.0024803      0.0024803   
   2.0000000      0.0003704      0.0027286      0.0027286      0.0027286      0.0027286      0.0027286      0.0027286      0.0027286   
   2.1000000      0.0003752      0.0028031      0.0052473      0.0052473      0.0052473      0.0052473      0.0052473      0.0052473   
   2.2050612      0.0003803      0.0028747      0.0057473      0.0057473      0.0057473      0.0057473      0.0057473      0.0057473   
   2.3387023      0.0003867      0.0029575      0.0060928      0.0060928      0.0060928      0.0060928      0.0060928      0.0060928   
   2.5086977      0.0003949      0.0030519      0.0063688      0.0063688      0.0063688      0.0063688      0.0063688      0.0063688   
   2.7249370      0.0004051      0.0031579      0.0066058      0.0066058      0.0066058      0.0066058      0.0066058      0.0066058   
   3.0000000      0.0004179      0.0032753      0.0068179      0.0068179      0.0068179      0.0068179      0.0068179      0.0068179   
   3.1000000      0.0004225      0.0033140      0.0068802      0.0088026      0.0088026      0.0088026      0.0088026      0.0088026   
   3.2050612      0.0004274      0.0033527      0.0069396      0.0091834      0.0091834      0.0091834      0.0091834      0.0091834   
   3.3387023      0.0004335      0.0033994      0.0070077      0.0094461      0.0094461      0.0094461      0.0094461      0.0094461   
   3.5086977      0.0004412      0.0034550      0.0070848      0.0096558      0.0096558      0.0096558      0.0096558      0.0096558   
   3.7249370      0.0004509      0.0035206      0.0071706      0.0098357      0.0098357      0.0098357      0.0098357      0.0098357   
   4.0000000      0.0004632      0.0035967      0.0072648      0.0099967      0.0099967      0.0099967      0.0099967      0.0099967   
   4.1000000      0.0004676      0.0036227      0.0072958      0.0100440      0.0115071      0.0115071      0.0115071      0.0115071   
   4.2050612      0.0004722      0.0036490      0.0073266      0.0100891      0.0117959      0.0117959      0.0117959      0.0117959   
   4.3387023      0.0004780      0.0036813      0.0073637      0.0101408      0.0119951      0.0119951      0.0119951      0.0119951   
   4.5086977      0.0004854      0.0037205      0.0074079      0.0101993      0.0121540      0.0121540      0.0121540      0.0121540   
   4.7249370      0.0004946      0.0037677      0.0074597      0.0102644      0.0122905      0.0122905      0.0122905      0.0122905   
   5.0000000      0.0005063      0.0038239      0.0075197      0.0103359      0.0124126      0.0124126      0.0124126      0.0124126   
   5.1000000      0.0005105      0.0038433      0.0075400      0.0103594      0.0124484      0.0135595      0.0135595      0.0135595   
   5.2050612      0.0005149      0.0038632      0.0075607      0.0103828      0.0124826      0.0137784      0.0137784      0.0137784   
   5.3387023      0.0005205      0.0038878      0.0075861      0.0104110      0.0125218      0.0139294      0.0139294      0.0139294   
   5.5086977      0.0005275      0.0039180      0.0076168      0.0104445      0.0125662      0.0140499      0.0140499      0.0140499   
   5.7249370      0.0005364      0.0039547      0.0076537      0.0104838      0.0126156      0.0141533      0.0141533      0.0141533   
   6.0000000      0.0005475      0.0039990      0.0076975      0.0105293      0.0126698      0.0142459      0.0142459      0.0142459   
   6.1000000      0.0005515      0.0040145      0.0077126      0.0105448      0.0126875      0.0142731      0.0151160      0.0151160   
   6.2050612      0.0005557      0.0040305      0.0077281      0.0105605      0.0127053      0.0142990      0.0152819      0.0152819   
   6.3387023      0.0005611      0.0040503      0.0077473      0.0105797      0.0127267      0.0143287      0.0153963      0.0153963   
   6.5086977      0.0005678      0.0040748      0.0077707      0.0106030      0.0127520      0.0143623      0.0154877      0.0154877   
   6.7249370      0.0005763      0.0041048      0.0077993      0.0106310      0.0127818      0.0143997      0.0155660      0.0155660   
   7.0000000      0.0005870      0.0041414      0.0078337      0.0106642      0.0128164      0.0144408      0.0156362      0.0156362   
   7.1000000      0.0005908      0.0041543      0.0078457      0.0106757      0.0128281      0.0144543      0.0156568      0.0162960   
   7.2050612      0.0005949      0.0041675      0.0078581      0.0106874      0.0128400      0.0144678      0.0156764      0.0164217   
   7.3387023      0.0006000      0.0041841      0.0078734      0.0107020      0.0128546      0.0144840      0.0156990      0.0165084   
   7.5086977      0.0006064      0.0042047      0.0078924      0.0107198      0.0128722      0.0145032      0.0157244      0.0165776   
   7.7249370      0.0006146      0.0042300      0.0079156      0.0107414      0.0128935      0.0145258      0.0157528      0.0166371   
   8.0000000      0.0006248      0.0042611      0.0079439      0.0107675      0.0129187      0.0145520      0.0157840      0.0166902   
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
   0.0000000    1.0000419   -0.0000000    1.0000419    0.0000000    0.0000000    0.0000000    105130.6476713 
   0.0000000    1.0419000   -0.0000000    1.0419000    0.0000000    0.0000000    0.0000000    104920.4915066 
   0.0000000    1.0838000   -0.0000000    1.0838000    0.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.100000000000    =  Time in days
   0.0002727    2.0000419   -0.0000000    1.0000419    1.0000000    0.1063578    0.1063578    104425.1351924 
   0.0001343    2.0417018    0.0000202    1.0419000    1.0000000    0.1059012    0.1059012    104237.5028280 
   0.0000000    2.0838000   -0.0000000    1.0838000    1.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.205061218966    =  Time in days
   0.0002784    2.0000419   -0.0000000    1.0000419    1.0000000    0.0046167    0.0046167    104410.0582802 
   0.0001369    2.0418921    0.0000008    1.0419000    1.0000000    0.0041433    0.0041433    104224.4897659 
   0.0000000    2.0838000   -0.0000000    1.0838000    1.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.338702261693    =  Time in days
   0.0002855    2.0000419   -0.0000000    1.0000419    1.0000000    0.0058344    0.0058344    104391.1290992 
   0.0001402    2.0418922    0.0000008    1.0419000    1.0000000    0.0052412    0.0052412    104208.1405019 
   0.0000000    2.0838000   -0.0000000    1.0838000    1.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.508697703179    =  Time in days
   0.0002946    2.0000419   -0.0000000    1.0000419    1.0000000    0.0073563    0.0073563    104367.3232000 
   0.0001444    2.0418923    0.0000008    1.0419000    1.0000000    0.0066163    0.0066163    104187.5471167 
   0.0000000    2.0838000   -0.0000000    1.0838000    1.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.724937037565    =  Time in days
   0.0003060    2.0000419   -0.0000000    1.0000419    1.0000000    0.0092539    0.0092539    104337.4726019 
   0.0001497    2.0418923    0.0000008    1.0419000    1.0000000    0.0083355    0.0083355    104161.6744180 
   0.0000000    2.0838000   -0.0000000    1.0838000    1.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.000000000000    =  Time in days
   0.0003202    2.0000419   -0.0000000    1.0000419    1.0000000    0.0116079    0.0116079    104300.1799854 
   0.0001563    2.0418924    0.0000008    1.0419000    1.0000000    0.0104755    0.0104755    104129.2730730 
   0.0000000    2.0838000   -0.0000000    1.0838000    1.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.100000000000    =  Time in days
   0.0012187    4.0000419   -0.0000000    1.0000419    3.0000000    0.7381909    0.7381909    102259.4842286 
   0.0005802    4.0405662    0.0001360    1.0419000    3.0000000    0.6777777    0.6777777    102278.0982937 
   0.0000000    4.0838000   -0.0000000    1.0838000    3.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.205061218966    =  Time in days
   0.0016004    4.0000419   -0.0000000    1.0000419    3.0000000    0.3208268    0.3208268    101568.8036688 
   0.0007630    4.0413288    0.0000582    1.0419000    3.0000000    0.3044022    0.3044022    101614.8322640 
   0.0000000    4.0838000   -0.0000000    1.0838000    3.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.338702261693    =  Time in days
   0.0019253    4.0000419   -0.0000000    1.0000419    3.0000000    0.2746257    0.2746257    101066.6256438 
   0.0009211    4.0415075    0.0000400    1.0419000    3.0000000    0.2684095    0.2684095    101108.2658973 
   0.0000000    4.0838000   -0.0000000    1.0838000    3.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.508697703179    =  Time in days
   0.0022148    4.0000419   -0.0000000    1.0000419    3.0000000    0.2466964    0.2466964    100682.9727506 
   0.0010634    4.0416190    0.0000286    1.0419000    3.0000000    0.2455450    0.2455450    100706.7876389 
   0.0000000    4.0838000   -0.0000000    1.0838000    3.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.724937037565    =  Time in days
   0.0024803    4.0000419   -0.0000000    1.0000419    3.0000000    0.2284555    0.2284555    100383.0446587 
   0.0011947    4.0416934    0.0000211    1.0419000    3.0000000    0.2301454    0.2301454    100382.7497156 
   0.0000000    4.0838000   -0.0000000    1.0838000    3.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.000000000000    =  Time in days
   0.0027286    4.0000419   -0.0000000    1.0000419    3.0000000    0.2159143    0.2159143    100147.3365909 
   0.0013181    4.0417454    0.0000158    1.0419000    3.0000000    0.2193362    0.2193362    100119.8594929 
   0.0000000    4.0838000   -0.0000000    1.0838000    3.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.100000000000    =  Time in days
   0.0052473    8.0000419   -0.0000000    1.0000419    7.0000000    2.5797847    2.5797847    100389.7892214 
   0.0025740    8.0368026    0.0005196    1.0419000    7.0000000    2.6246307    2.6246307     99972.8486935 
   0.0000000    8.0838000   -0.0000000    1.0838000    7.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.205061218966    =  Time in days
   0.0057473    8.0000419   -0.0000000    1.0000419    7.0000000    0.5158535    0.5158535    101086.7236615 
   0.0028256    8.0409196    0.0000999    1.0419000    7.0000000    0.5356968    0.5356968    100578.0261089 
   0.0000000    8.0838000   -0.0000000    1.0838000    7.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.338702261693    =  Time in days
   0.0060928    8.0000419   -0.0000000    1.0000419    7.0000000    0.3669112    0.3669112    101716.4304993 
   0.0029995    8.0413553    0.0000555    1.0419000    7.0000000    0.3814474    0.3814474    101142.8755279 
   0.0000000    8.0838000   -0.0000000    1.0838000    7.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.508697703179    =  Time in days
   0.0063688    8.0000419   -0.0000000    1.0000419    7.0000000    0.2997159    0.2997159    102312.8725478 
   0.0031385    8.0415522    0.0000355    1.0419000    7.0000000    0.3117418    0.3117418    101686.4742910 
   0.0000000    8.0838000   -0.0000000    1.0838000    7.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.724937037565    =  Time in days
   0.0066058    8.0000419   -0.0000000    1.0000419    7.0000000    0.2621396    0.2621396    102894.8927177 
   0.0032578    8.0416622    0.0000242    1.0419000    7.0000000    0.2727314    0.2727314    102222.2860205 
   0.0000000    8.0838000   -0.0000000    1.0838000    7.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.000000000000    =  Time in days
   0.0068179    8.0000419   -0.0000000    1.0000419    7.0000000    0.2386679    0.2386679    103473.7706704 
   0.0033646    8.0417307    0.0000173    1.0419000    7.0000000    0.2483531    0.2483531    102759.0348611 
   0.0000000    8.0838000   -0.0000000    1.0838000    7.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.100000000000    =  Time in days
   0.0088026   16.0000419   -0.0000000    1.0000419   15.0000000    3.0556569    3.0556569    112142.9889630 
   0.0043616   16.0360146    0.0005999    1.0419000   15.0000000    3.1327112    3.1327112    110915.5624840 
   0.0000000   16.0838000   -0.0000000    1.0838000   15.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.205061218966    =  Time in days
   0.0091834   16.0000419   -0.0000000    1.0000419   15.0000000    0.5174451    0.5174451    114638.3954035 
   0.0045535   16.0410158    0.0000901    1.0419000   15.0000000    0.5382766    0.5382766    113300.8949309 
   0.0000000   16.0838000   -0.0000000    1.0838000   15.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.338702261693    =  Time in days
   0.0094461   16.0000419   -0.0000000    1.0000419   15.0000000    0.3675311    0.3675311    116558.8142727 
   0.0046858   16.0414171    0.0000492    1.0419000   15.0000000    0.3824537    0.3824537    115141.3475692 
   0.0000000   16.0838000   -0.0000000    1.0838000   15.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.508697703179    =  Time in days
   0.0096558   16.0000419   -0.0000000    1.0000419   15.0000000    0.3000218    0.3000218    118219.7960743 
   0.0047915   16.0415951    0.0000311    1.0419000   15.0000000    0.3122487    0.3122487    116735.7180922 
   0.0000000   16.0838000   -0.0000000    1.0838000   15.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.724937037565    =  Time in days
   0.0098357   16.0000419   -0.0000000    1.0000419   15.0000000    0.2623154    0.2623154    119742.2102482 
   0.0048822   16.0416933    0.0000211    1.0419000   15.0000000    0.2730275    0.2730275    118198.7886914 
   0.0000000   16.0838000   -0.0000000    1.0838000   15.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.000000000000    =  Time in days
   0.0099967   16.0000419   -0.0000000    1.0000419   15.0000000    0.2387781    0.2387781    121186.0316861 
   0.0049633   16.0417540    0.0000149    1.0419000   15.0000000    0.2485414    0.2485414    119587.6176886 
   0.0000000   16.0838000   -0.0000000    1.0838000   15.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.100000000000    =  Time in days
   0.0115071   32.0000419   -0.0000000    1.0000419   31.0000000    3.8752434    3.8752434    139465.1764223 
   0.0057235   32.0355174    0.0006506    1.0419000   31.0000000    3.9599029    3.9599029    137170.8285919 
   0.0000000   32.0838000   -0.0000000    1.0838000   31.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.205061218966    =  Time in days
   0.0117959   32.0000419   -0.0000000    1.0000419   31.0000000    0.5173572    0.5173572    144208.3026733 
   0.0058691   32.0411870    0.0000727    1.0419000   31.0000000    0.5383851    0.5383851    141754.6625740 
   0.0000000   32.0838000   -0.0000000    1.0838000   31.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.338702261693    =  Time in days
   0.0119951   32.0000419   -0.0000000    1.0000419   31.0000000    0.3674969    0.3674969    147784.9807693 
   0.0059695   32.0415151    0.0000392    1.0419000   31.0000000    0.3824960    0.3824960    145213.5489704 
   0.0000000   32.0838000   -0.0000000    1.0838000   31.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.508697703179    =  Time in days
   0.0121540   32.0000419   -0.0000000    1.0000419   31.0000000    0.2999955    0.2999955    150837.5741161 
   0.0060496   32.0416589    0.0000246    1.0419000   31.0000000    0.3122618    0.3122618    148166.8314298 
   0.0000000   32.0838000   -0.0000000    1.0838000   31.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.724937037565    =  Time in days
   0.0122905   32.0000419   -0.0000000    1.0000419   31.0000000    0.2622959    0.2622959    153607.5765267 
   0.0061184   32.0417376    0.0000166    1.0419000   31.0000000    0.2730315    0.2730315    150847.5236292 
   0.0000000   32.0838000   -0.0000000    1.0838000   31.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.000000000000    =  Time in days
   0.0124126   32.0000419   -0.0000000    1.0000419   31.0000000    0.2387634    0.2387634    156213.3007749 
   0.0061799   32.0417859    0.0000116    1.0419000   31.0000000    0.2485420    0.2485420    153369.8360312 
   0.0000000   32.0838000   -0.0000000    1.0838000   31.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.100000000000    =  Time in days
   0.0135595   64.0000419   -0.0000000    1.0000419   63.0000000    5.5082157    5.5082157    188161.3405660 
   0.0067577   64.0348643    0.0007172    1.0419000   63.0000000    5.5966470    5.5966470    184269.2153958 
   0.0000000   64.0838000   -0.0000000    1.0838000   63.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.205061218966    =  Time in days
   0.0137784   64.0000419   -0.0000000    1.0000419   63.0000000    0.5172926    0.5172926    196254.6695589 
   0.0068681   64.0413704    0.0000540    1.0419000   63.0000000    0.5384153    0.5384153    192110.5354724 
   0.0000000   64.0838000   -0.0000000    1.0838000   63.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.338702261693    =  Time in days
   0.0139294   64.0000419   -0.0000000    1.0000419   63.0000000    0.3674718    0.3674718    202328.4601844 
   0.0069442   64.0416166    0.0000289    1.0419000   63.0000000    0.3825077    0.3825077    197996.3631101 
   0.0000000   64.0838000   -0.0000000    1.0838000   63.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.508697703179    =  Time in days
   0.0140499   64.0000419   -0.0000000    1.0000419   63.0000000    0.2999788    0.2999788    207495.8750925 
   0.0070050   64.0417235    0.0000180    1.0419000   63.0000000    0.3122641    0.3122641    203004.4257837 
   0.0000000   64.0838000   -0.0000000    1.0838000   63.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.724937037565    =  Time in days
   0.0141533   64.0000419   -0.0000000    1.0000419   63.0000000    0.2622843    0.2622843    212173.7153869 
   0.0070571   64.0417817    0.0000121    1.0419000   63.0000000    0.2730312    0.2730312    207538.3594734 
   0.0000000   64.0838000   -0.0000000    1.0838000   63.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.000000000000    =  Time in days
   0.0142459   64.0000419   -0.0000000    1.0000419   63.0000000    0.2387550    0.2387550    216565.6119755 
   0.0071038   64.0418172    0.0000084    1.0419000   63.0000000    0.2485409    0.2485409    211795.3915909 
   0.0000000   64.0838000   -0.0000000    1.0838000   63.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.100000000000    =  Time in days
   0.0151160  128.0000419   -0.0000000    1.0000419  127.0000000    8.7711141    8.7711141    270032.5370450 
   0.0075423  128.0338259    0.0008230    1.0419000  127.0000000    8.8614343    8.8614343    263584.3376932 
   0.0000000  128.0838000   -0.0000000    1.0838000  127.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.205061218966    =  Time in days
   0.0152819  128.0000419   -0.0000000    1.0000419  127.0000000    0.5172512    0.5172512    283504.3122499 
   0.0076260  128.0415303    0.0000377    1.0419000  127.0000000    0.5384206    0.5384206    276641.6896768 
   0.0000000  128.0838000   -0.0000000    1.0838000  127.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.338702261693    =  Time in days
   0.0153963  128.0000419   -0.0000000    1.0000419  127.0000000    0.3674557    0.3674557    293606.2704701 
   0.0076837  128.0417035    0.0000200    1.0419000  127.0000000    0.3825098    0.3825098    286433.2614714 
   0.0000000  128.0838000   -0.0000000    1.0838000  127.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.508697703179    =  Time in days
   0.0154877  128.0000419   -0.0000000    1.0000419  127.0000000    0.2999690    0.2999690    302196.5805727 
   0.0077298  128.0417782    0.0000124    1.0419000  127.0000000    0.3122637    0.3122637    294759.7390679 
   0.0000000  128.0838000   -0.0000000    1.0838000  127.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.724937037565    =  Time in days
   0.0155660  128.0000419   -0.0000000    1.0000419  127.0000000    0.2622778    0.2622778    309970.4878863 
   0.0077693  128.0418187    0.0000083    1.0419000  127.0000000    0.2730303    0.2730303    302294.9153694 
   0.0000000  128.0838000   -0.0000000    1.0838000  127.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.000000000000    =  Time in days
   0.0156362  128.0000419   -0.0000000    1.0000419  127.0000000    0.2387505    0.2387505    317267.5042149 
   0.0078047  128.0418433    0.0000058    1.0419000  127.0000000    0.2485400    0.2485400    309367.8384293 
   0.0000000  128.0838000   -0.0000000    1.0838000  127.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.100000000000    =  Time in days
   0.0162960  256.0000419   -0.0000000    1.0000419  255.0000000   15.2955506   15.2955506    406097.9813242 
   0.0081373  256.0322955    0.0009791    1.0419000  255.0000000   15.3868176   15.3868176    395427.4747875 
   0.0000000  256.0838000   -0.0000000    1.0838000  255.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.205061218966    =  Time in days
   0.0164217  256.0000419   -0.0000000    1.0000419  255.0000000    0.5172240    0.5172240    428486.8763941 
   0.0082007  256.0416538    0.0000251    1.0419000  255.0000000    0.5384162    0.5384162    417122.0615608 
   0.0000000  256.0838000   -0.0000000    1.0838000  255.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.338702261693    =  Time in days
   0.0165084  256.0000419   -0.0000000    1.0000419  255.0000000    0.3674451    0.3674451    445282.2607562 
   0.0082444  256.0417698    0.0000133    1.0419000  255.0000000    0.3825081    0.3825081    433396.3056015 
   0.0000000  256.0838000   -0.0000000    1.0838000  255.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.508697703179    =  Time in days
   0.0165776  256.0000419   -0.0000000    1.0000419  255.0000000    0.2999630    0.2999630    459569.2514264 
   0.0082793  256.0418196    0.0000082    1.0419000  255.0000000    0.3122623    0.3122623    447239.7047135 
   0.0000000  256.0838000   -0.0000000    1.0838000  255.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.724937037565    =  Time in days
   0.0166371  256.0000419   -0.0000000    1.0000419  255.0000000    0.2622740    0.2622740    472502.4428963 
   0.0083093  256.0418465    0.0000055    1.0419000  255.0000000    0.2730293    0.2730293    459771.0843555 
   0.0000000  256.0838000   -0.0000000    1.0838000  255.0000000 -1 -1 -1
[End of Vertical Data at Time]
[Vertical Data at Time]
   8.000000000000    =  Time in days
   0.0166902  256.0000419   -0.0000000    1.0000419  255.0000000    0.2387479    0.2387479         0.0000000 
   0.0083361  256.0418627    0.0000038    1.0419000  255.0000000    0.2485392    0.2485392         0.0000000 
   0.0000000  256.0838000   -0.0000000    1.0838000  255.0000000 -1 -1 -1
[End of Vertical Data at Time]
[End of Time dependent Data]
[Time-dependent Data]
[Column Indication]
Depth
Settlement
[End of Column Indication]
[Vertical Data at Fixed Time]
   0.001000000000    =  Time in days
  -0.0000100    0.0000027
  -0.0010095    0.0000026
  -0.0020090    0.0000024
  -0.0030085    0.0000023
  -0.0040080    0.0000022
  -0.0050075    0.0000020
  -0.0060070    0.0000019
  -0.0070065    0.0000018
  -0.0080060    0.0000016
  -0.0090055    0.0000015
  -0.0100050    0.0000013
  -0.0110045    0.0000012
  -0.0120040    0.0000011
  -0.0130035    0.0000009
  -0.0140030    0.0000008
  -0.0150025    0.0000007
  -0.0160020    0.0000005
  -0.0170015    0.0000004
  -0.0180010    0.0000003
  -0.0190005    0.0000001
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000055
  -0.0010095    0.0000052
  -0.0020090    0.0000049
  -0.0030085    0.0000046
  -0.0040080    0.0000043
  -0.0050075    0.0000041
  -0.0060070    0.0000038
  -0.0070065    0.0000035
  -0.0080060    0.0000032
  -0.0090055    0.0000030
  -0.0100050    0.0000027
  -0.0110045    0.0000024
  -0.0120040    0.0000021
  -0.0130035    0.0000019
  -0.0140030    0.0000016
  -0.0150025    0.0000013
  -0.0160020    0.0000011
  -0.0170015    0.0000008
  -0.0180010    0.0000005
  -0.0190005    0.0000003
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0000136
  -0.0010095    0.0000129
  -0.0020090    0.0000122
  -0.0030085    0.0000116
  -0.0040080    0.0000109
  -0.0050075    0.0000102
  -0.0060070    0.0000095
  -0.0070065    0.0000088
  -0.0080060    0.0000081
  -0.0090055    0.0000074
  -0.0100050    0.0000067
  -0.0110045    0.0000060
  -0.0120040    0.0000054
  -0.0130035    0.0000047
  -0.0140030    0.0000040
  -0.0150025    0.0000034
  -0.0160020    0.0000027
  -0.0170015    0.0000020
  -0.0180010    0.0000013
  -0.0190005    0.0000007
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0000273
  -0.0010095    0.0000259
  -0.0020090    0.0000245
  -0.0030085    0.0000231
  -0.0040080    0.0000217
  -0.0050075    0.0000203
  -0.0060070    0.0000190
  -0.0070065    0.0000176
  -0.0080060    0.0000162
  -0.0090055    0.0000148
  -0.0100050    0.0000134
  -0.0110045    0.0000121
  -0.0120040    0.0000107
  -0.0130035    0.0000094
  -0.0140030    0.0000081
  -0.0150025    0.0000067
  -0.0160020    0.0000054
  -0.0170015    0.0000040
  -0.0180010    0.0000027
  -0.0190005    0.0000013
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
  -0.0000100    0.0000545
  -0.0010095    0.0000518
  -0.0020090    0.0000490
  -0.0030085    0.0000462
  -0.0040080    0.0000435
  -0.0050075    0.0000407
  -0.0060070    0.0000379
  -0.0070065    0.0000351
  -0.0080060    0.0000324
  -0.0090055    0.0000296
  -0.0100050    0.0000268
  -0.0110045    0.0000242
  -0.0120040    0.0000215
  -0.0130035    0.0000188
  -0.0140030    0.0000161
  -0.0150025    0.0000134
  -0.0160020    0.0000107
  -0.0170015    0.0000081
  -0.0180010    0.0000054
  -0.0190005    0.0000027
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
  -0.0000100    0.0001363
  -0.0010095    0.0001294
  -0.0020090    0.0001225
  -0.0030085    0.0001156
  -0.0040080    0.0001086
  -0.0050075    0.0001017
  -0.0060070    0.0000948
  -0.0070065    0.0000879
  -0.0080060    0.0000809
  -0.0090055    0.0000740
  -0.0100050    0.0000671
  -0.0110045    0.0000604
  -0.0120040    0.0000537
  -0.0130035    0.0000470
  -0.0140030    0.0000403
  -0.0150025    0.0000335
  -0.0160020    0.0000268
  -0.0170015    0.0000201
  -0.0180010    0.0000134
  -0.0190005    0.0000067
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0002727
  -0.0010095    0.0002588
  -0.0020090    0.0002450
  -0.0030085    0.0002311
  -0.0040080    0.0002173
  -0.0050075    0.0002034
  -0.0060070    0.0001896
  -0.0070065    0.0001757
  -0.0080060    0.0001619
  -0.0090055    0.0001480
  -0.0100050    0.0001342
  -0.0110045    0.0001208
  -0.0120040    0.0001074
  -0.0130035    0.0000939
  -0.0140030    0.0000805
  -0.0150025    0.0000671
  -0.0160020    0.0000537
  -0.0170015    0.0000403
  -0.0180010    0.0000268
  -0.0190005    0.0000134
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0002782
  -0.0010095    0.0002640
  -0.0020090    0.0002499
  -0.0030085    0.0002357
  -0.0040080    0.0002216
  -0.0050075    0.0002074
  -0.0060070    0.0001933
  -0.0070065    0.0001792
  -0.0080060    0.0001650
  -0.0090055    0.0001509
  -0.0100050    0.0001367
  -0.0110045    0.0001231
  -0.0120040    0.0001094
  -0.0130035    0.0000957
  -0.0140030    0.0000820
  -0.0150025    0.0000684
  -0.0160020    0.0000547
  -0.0170015    0.0000410
  -0.0180010    0.0000273
  -0.0190005    0.0000137
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0002942
  -0.0010095    0.0002792
  -0.0020090    0.0002642
  -0.0030085    0.0002492
  -0.0040080    0.0002342
  -0.0050075    0.0002192
  -0.0060070    0.0002042
  -0.0070065    0.0001892
  -0.0080060    0.0001742
  -0.0090055    0.0001592
  -0.0100050    0.0001442
  -0.0110045    0.0001297
  -0.0120040    0.0001153
  -0.0130035    0.0001009
  -0.0140030    0.0000865
  -0.0150025    0.0000721
  -0.0160020    0.0000577
  -0.0170015    0.0000432
  -0.0180010    0.0000288
  -0.0190005    0.0000144
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0003202
  -0.0010095    0.0003038
  -0.0020090    0.0002874
  -0.0030085    0.0002710
  -0.0040080    0.0002546
  -0.0050075    0.0002382
  -0.0060070    0.0002218
  -0.0070065    0.0002054
  -0.0080060    0.0001890
  -0.0090055    0.0001726
  -0.0100050    0.0001563
  -0.0110045    0.0001406
  -0.0120040    0.0001250
  -0.0130035    0.0001094
  -0.0140030    0.0000938
  -0.0150025    0.0000781
  -0.0160020    0.0000625
  -0.0170015    0.0000469
  -0.0180010    0.0000313
  -0.0190005    0.0000156
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100    0.0027286
  -0.0010095    0.0025875
  -0.0020090    0.0024464
  -0.0030085    0.0023052
  -0.0040080    0.0021641
  -0.0050075    0.0020230
  -0.0060070    0.0018819
  -0.0070065    0.0017407
  -0.0080060    0.0015996
  -0.0090055    0.0014585
  -0.0100050    0.0013174
  -0.0110045    0.0011857
  -0.0120040    0.0010539
  -0.0130035    0.0009222
  -0.0140030    0.0007904
  -0.0150025    0.0006587
  -0.0160020    0.0005270
  -0.0170015    0.0003952
  -0.0180010    0.0002635
  -0.0190005    0.0001317
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0124126
  -0.0010095    0.0117890
  -0.0020090    0.0111654
  -0.0030085    0.0105418
  -0.0040080    0.0099183
  -0.0050075    0.0092947
  -0.0060070    0.0086711
  -0.0070065    0.0080475
  -0.0080060    0.0074240
  -0.0090055    0.0068004
  -0.0100050    0.0061768
  -0.0110045    0.0055592
  -0.0120040    0.0049415
  -0.0130035    0.0043238
  -0.0140030    0.0037061
  -0.0150025    0.0030884
  -0.0160020    0.0024707
  -0.0170015    0.0018531
  -0.0180010    0.0012354
  -0.0190005    0.0006177
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
  -0.0200000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0166902
  -0.0010095    0.0158544
  -0.0020090    0.0150186
  -0.0030085    0.0141827
  -0.0040080    0.0133469
  -0.0050075    0.0125111
  -0.0060070    0.0116752
  -0.0070065    0.0108394
  -0.0080060    0.0100036
  -0.0090055    0.0091677
  -0.0100050    0.0083319
  -0.0110045    0.0074987
  -0.0120040    0.0066655
  -0.0130035    0.0058323
  -0.0140030    0.0049991
  -0.0150025    0.0041660
  -0.0160020    0.0033328
  -0.0170015    0.0024996
  -0.0180010    0.0016664
  -0.0190005    0.0008332
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
[End of Results]
