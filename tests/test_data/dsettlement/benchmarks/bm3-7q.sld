Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 8-3-2019
TIME       : 16:04:04
FILENAME   : D:\DSettlement\Test Results DSettlement\Benchmarks Branch\bm3-7q.sld
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
Clay
SoilColor=9764853
SoilGamDry=15.00
SoilGamWet=18.00
SoilInitialVoidRatio=0.000000
SoilCohesion=10.00
SoilPhi=30.00
SoilPreconIsotacheType=2
SoilPreconKoppejanType=2
SoilUseEquivalentAge=0
SoilEquivalentAge=0.00E+00
SoilPc=8.00E+00
SoilOCR=1.20
SoilPOP=5.00
SoilLimitStress=0.00
SoilDrained=1
SoilApAsApproximationByCpCs=0
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
SoilStdOCR=0.30
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
Benchmark MSettle: bm3-7q
POP compression
Variable within the layer and corr. at t=0
[END OF RUN IDENTIFICATION]
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
0 : Waspan = FALSE
[END OF MODEL]
[VERTICALS]
    100 = total Mesh
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
[PORE PRESSURE METERS]
    0 = number of items
[END OF PORE PRESSURE METERS]
[NON-UNIFORM LOADS PORE PRESSURES]
    0 = number of items
[END OF NON-UNIFORM LOADS PORE PRESSURES]
[OTHER LOADS PORE PRESSURES]
   11 = number of items
Inital load top
       0.000 = Top of heightening
Inital load middle
       0.000 = Top of heightening
Inital load bottom
       0.000 = Top of heightening
1
       0.000 = Top of heightening
2
       0.000 = Top of heightening
3
       0.000 = Top of heightening
4
       0.000 = Top of heightening
5
       0.000 = Top of heightening
6
       0.000 = Top of heightening
7
       0.000 = Top of heightening
8
       0.000 = Top of heightening
[END OF OTHER LOADS PORE PRESSURES]
[CALCULATION OPTIONS PORE PRESSURES]
1 : Shear stress = TRUE
1 : calculation method of lateral stress ratio (k0) = Nu
[END OF CALCULATION OPTIONS PORE PRESSURES]
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
     49  =  Time step count 
      8  =  Load step count 
   0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000      0.0000000   
   0.1000000      0.0008251      0.0008251      0.0008251      0.0008251      0.0008251      0.0008251      0.0008251      0.0008251   
   0.2050612      0.0008266      0.0008266      0.0008266      0.0008266      0.0008266      0.0008266      0.0008266      0.0008266   
   0.3387023      0.0008284      0.0008284      0.0008284      0.0008284      0.0008284      0.0008284      0.0008284      0.0008284   
   0.5086977      0.0008307      0.0008307      0.0008307      0.0008307      0.0008307      0.0008307      0.0008307      0.0008307   
   0.7249370      0.0008335      0.0008335      0.0008335      0.0008335      0.0008335      0.0008335      0.0008335      0.0008335   
   1.0000000      0.0008369      0.0008369      0.0008369      0.0008369      0.0008369      0.0008369      0.0008369      0.0008369   
   1.1000000      0.0008381     -0.0005375     -0.0005375     -0.0005375     -0.0005375     -0.0005375     -0.0005375     -0.0005375   
   1.2050612      0.0008393     -0.0005393     -0.0005393     -0.0005393     -0.0005393     -0.0005393     -0.0005393     -0.0005393   
   1.3387023      0.0008408     -0.0005415     -0.0005415     -0.0005415     -0.0005415     -0.0005415     -0.0005415     -0.0005415   
   1.5086977      0.0008427     -0.0005442     -0.0005442     -0.0005442     -0.0005442     -0.0005442     -0.0005442     -0.0005442   
   1.7249370      0.0008450     -0.0005475     -0.0005475     -0.0005475     -0.0005475     -0.0005475     -0.0005475     -0.0005475   
   2.0000000      0.0008478     -0.0005515     -0.0005515     -0.0005515     -0.0005515     -0.0005515     -0.0005515     -0.0005515   
   2.1000000      0.0008487     -0.0005529      0.0002722      0.0002722      0.0002722      0.0002722      0.0002722      0.0002722   
   2.2050612      0.0008498     -0.0005543      0.0002723      0.0002723      0.0002723      0.0002723      0.0002723      0.0002723   
   2.3387023      0.0008510     -0.0005560      0.0002724      0.0002724      0.0002724      0.0002724      0.0002724      0.0002724   
   2.5086977      0.0008526     -0.0005582      0.0002725      0.0002725      0.0002725      0.0002725      0.0002725      0.0002725   
   2.7249370      0.0008545     -0.0005608      0.0002727      0.0002727      0.0002727      0.0002727      0.0002727      0.0002727   
   3.0000000      0.0008569     -0.0005640      0.0002728      0.0002728      0.0002728      0.0002728      0.0002728      0.0002728   
   3.1000000      0.0008578     -0.0005652      0.0002729      0.0025803      0.0025803      0.0025803      0.0025803      0.0025803   
   3.2050612      0.0008587     -0.0005663      0.0002730      0.0025846      0.0025846      0.0025846      0.0025846      0.0025846   
   3.3387023      0.0008598     -0.0005678      0.0002730      0.0025898      0.0025898      0.0025898      0.0025898      0.0025898   
   3.5086977      0.0008611     -0.0005696      0.0002731      0.0025963      0.0025963      0.0025963      0.0025963      0.0025963   
   3.7249370      0.0008628     -0.0005718      0.0002732      0.0026042      0.0026042      0.0026042      0.0026042      0.0026042   
   4.0000000      0.0008649     -0.0005745      0.0002733      0.0026138      0.0026138      0.0026138      0.0026138      0.0026138   
   4.1000000      0.0008656     -0.0005754      0.0002733      0.0026171      0.0016553      0.0016553      0.0016553      0.0016553   
   4.2050612      0.0008664     -0.0005764      0.0002734      0.0026205      0.0016567      0.0016567      0.0016567      0.0016567   
   4.3387023      0.0008674     -0.0005776      0.0002734      0.0026248      0.0016583      0.0016583      0.0016583      0.0016583   
   4.5086977      0.0008686     -0.0005791      0.0002735      0.0026301      0.0016604      0.0016604      0.0016604      0.0016604   
   4.7249370      0.0008701     -0.0005810      0.0002735      0.0026366      0.0016630      0.0016630      0.0016630      0.0016630   
   5.0000000      0.0008719     -0.0005834      0.0002736      0.0026444      0.0016662      0.0016662      0.0016662      0.0016662   
   5.1000000      0.0008726     -0.0005842      0.0002736      0.0026472      0.0016673      0.0039747      0.0039747      0.0039747   
   5.2050612      0.0008733     -0.0005850      0.0002736      0.0026501      0.0016685      0.0039801      0.0039801      0.0039801   
   5.3387023      0.0008741     -0.0005861      0.0002737      0.0026537      0.0016699      0.0039867      0.0039867      0.0039867   
   5.5086977      0.0008752     -0.0005874      0.0002737      0.0026581      0.0016718      0.0039950      0.0039950      0.0039950   
   5.7249370      0.0008765     -0.0005891      0.0002737      0.0026636      0.0016740      0.0040051      0.0040051      0.0040051   
   6.0000000      0.0008782     -0.0005911      0.0002738      0.0026703      0.0016769      0.0040173      0.0040173      0.0040173   
   6.1000000      0.0008788     -0.0005918      0.0002738      0.0026727      0.0016779      0.0040216      0.0072573      0.0072573   
   6.2050612      0.0008794     -0.0005926      0.0002738      0.0026752      0.0016789      0.0040261      0.0072677      0.0072677   
   6.3387023      0.0008802     -0.0005935      0.0002738      0.0026783      0.0016802      0.0040316      0.0072805      0.0072805   
   6.5086977      0.0008812     -0.0005947      0.0002739      0.0026821      0.0016818      0.0040385      0.0072964      0.0072964   
   6.7249370      0.0008824     -0.0005962      0.0002739      0.0026869      0.0016839      0.0040469      0.0073158      0.0073158   
   7.0000000      0.0008839     -0.0005980      0.0002739      0.0026928      0.0016864      0.0040573      0.0073394      0.0073394   
   7.1000000      0.0008844     -0.0005986      0.0002739      0.0026948      0.0016873      0.0040609      0.0073476      0.0114190   
   7.2050612      0.0008850     -0.0005993      0.0002740      0.0026970      0.0016882      0.0040647      0.0073562      0.0114350   
   7.3387023      0.0008857     -0.0006002      0.0002740      0.0026997      0.0016894      0.0040694      0.0073668      0.0114549   
   7.5086977      0.0008866     -0.0006012      0.0002740      0.0027031      0.0016909      0.0040753      0.0073801      0.0114794   
   7.7249370      0.0008877     -0.0006025      0.0002740      0.0027073      0.0016927      0.0040826      0.0073963      0.0115095   
   8.0000000      0.0008891     -0.0006042      0.0002740      0.0027125      0.0016950      0.0040916      0.0074163      0.0115461   
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
   5.0001800      0.0001000     12.7000400     45.1156406      0.1155606   
  10.9000000      0.5000000     18.1000000     50.9512686      0.5512686   
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
      1     -0.0023323     -0.0004665      0.0016472      0.0002745      0.0119006      0.0019834   
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
   0.0008251   10.0000800
   0.0003239   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.205061218966    =  Time in days
   0.0008266   10.0000800
   0.0003245   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.338702261693    =  Time in days
   0.0008284   10.0000800
   0.0003252   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.508697703179    =  Time in days
   0.0008307   10.0000800
   0.0003261   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.724937037565    =  Time in days
   0.0008335   10.0000800
   0.0003272   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.000000000000    =  Time in days
   0.0008369   10.0000800
   0.0003285   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.100000000000    =  Time in days
  -0.0005375    5.0000800
  -0.0002110   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.205061218966    =  Time in days
  -0.0005393    5.0000800
  -0.0002117   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.338702261693    =  Time in days
  -0.0005415    5.0000800
  -0.0002126   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.508697703179    =  Time in days
  -0.0005442    5.0000800
  -0.0002136   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.724937037565    =  Time in days
  -0.0005475    5.0000800
  -0.0002149   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.000000000000    =  Time in days
  -0.0005515    5.0000800
  -0.0002165   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.100000000000    =  Time in days
   0.0002722   10.0000800
   0.0001068   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.205061218966    =  Time in days
   0.0002723   10.0000800
   0.0001069   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.338702261693    =  Time in days
   0.0002724   10.0000800
   0.0001069   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.508697703179    =  Time in days
   0.0002725   10.0000800
   0.0001070   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.724937037565    =  Time in days
   0.0002727   10.0000800
   0.0001070   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.000000000000    =  Time in days
   0.0002728   10.0000800
   0.0001071   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.100000000000    =  Time in days
   0.0025803   15.0000800
   0.0010846   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.205061218966    =  Time in days
   0.0025846   15.0000800
   0.0010864   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.338702261693    =  Time in days
   0.0025898   15.0000800
   0.0010886   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.508697703179    =  Time in days
   0.0025963   15.0000800
   0.0010913   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.724937037565    =  Time in days
   0.0026042   15.0000800
   0.0010947   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.000000000000    =  Time in days
   0.0026138   15.0000800
   0.0010987   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.100000000000    =  Time in days
   0.0016553   10.0000800
   0.0006927   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.205061218966    =  Time in days
   0.0016567   10.0000800
   0.0006933   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.338702261693    =  Time in days
   0.0016583   10.0000800
   0.0006940   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.508697703179    =  Time in days
   0.0016604   10.0000800
   0.0006949   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.724937037565    =  Time in days
   0.0016630   10.0000800
   0.0006960   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.000000000000    =  Time in days
   0.0016662   10.0000800
   0.0006973   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.100000000000    =  Time in days
   0.0039747   15.0000800
   0.0016752   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.205061218966    =  Time in days
   0.0039801   15.0000800
   0.0016775   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.338702261693    =  Time in days
   0.0039867   15.0000800
   0.0016803   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.508697703179    =  Time in days
   0.0039950   15.0000800
   0.0016838   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.724937037565    =  Time in days
   0.0040051   15.0000800
   0.0016881   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.000000000000    =  Time in days
   0.0040173   15.0000800
   0.0016933   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.100000000000    =  Time in days
   0.0072573   25.0000800
   0.0031365   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.205061218966    =  Time in days
   0.0072677   25.0000800
   0.0031410   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.338702261693    =  Time in days
   0.0072805   25.0000800
   0.0031466   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.508697703179    =  Time in days
   0.0072964   25.0000800
   0.0031535   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.724937037565    =  Time in days
   0.0073158   25.0000800
   0.0031620   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.000000000000    =  Time in days
   0.0073394   25.0000800
   0.0031722   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.100000000000    =  Time in days
   0.0114190   45.0000800
   0.0050698   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.205061218966    =  Time in days
   0.0114350   45.0000800
   0.0050770   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.338702261693    =  Time in days
   0.0114549   45.0000800
   0.0050859   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.508697703179    =  Time in days
   0.0114794   45.0000800
   0.0050969   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.724937037565    =  Time in days
   0.0115095   45.0000800
   0.0051104   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   8.000000000000    =  Time in days
   0.0115461   45.0000800
   0.0051269   50.4000000
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
  -0.0000100    0.0000083
  -0.0050095    0.0000077
  -0.0100090    0.0000072
  -0.0150085    0.0000067
  -0.0200080    0.0000062
  -0.0250075    0.0000057
  -0.0300070    0.0000052
  -0.0350065    0.0000047
  -0.0400060    0.0000042
  -0.0450055    0.0000037
  -0.0500050    0.0000032
  -0.0550045    0.0000029
  -0.0600040    0.0000026
  -0.0650035    0.0000023
  -0.0700030    0.0000019
  -0.0750025    0.0000016
  -0.0800020    0.0000013
  -0.0850015    0.0000010
  -0.0900010    0.0000006
  -0.0950005    0.0000003
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000165
  -0.0050095    0.0000155
  -0.0100090    0.0000145
  -0.0150085    0.0000135
  -0.0200080    0.0000125
  -0.0250075    0.0000115
  -0.0300070    0.0000105
  -0.0350065    0.0000095
  -0.0400060    0.0000085
  -0.0450055    0.0000075
  -0.0500050    0.0000065
  -0.0550045    0.0000058
  -0.0600040    0.0000052
  -0.0650035    0.0000045
  -0.0700030    0.0000039
  -0.0750025    0.0000032
  -0.0800020    0.0000026
  -0.0850015    0.0000019
  -0.0900010    0.0000013
  -0.0950005    0.0000006
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0000413
  -0.0050095    0.0000387
  -0.0100090    0.0000362
  -0.0150085    0.0000337
  -0.0200080    0.0000312
  -0.0250075    0.0000287
  -0.0300070    0.0000262
  -0.0350065    0.0000237
  -0.0400060    0.0000212
  -0.0450055    0.0000187
  -0.0500050    0.0000162
  -0.0550045    0.0000146
  -0.0600040    0.0000130
  -0.0650035    0.0000113
  -0.0700030    0.0000097
  -0.0750025    0.0000081
  -0.0800020    0.0000065
  -0.0850015    0.0000049
  -0.0900010    0.0000032
  -0.0950005    0.0000016
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0000825
  -0.0050095    0.0000775
  -0.0100090    0.0000725
  -0.0150085    0.0000675
  -0.0200080    0.0000625
  -0.0250075    0.0000574
  -0.0300070    0.0000524
  -0.0350065    0.0000474
  -0.0400060    0.0000424
  -0.0450055    0.0000374
  -0.0500050    0.0000324
  -0.0550045    0.0000291
  -0.0600040    0.0000259
  -0.0650035    0.0000227
  -0.0700030    0.0000194
  -0.0750025    0.0000162
  -0.0800020    0.0000130
  -0.0850015    0.0000097
  -0.0900010    0.0000065
  -0.0950005    0.0000032
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
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
   0.050000000000    =  Time in days
  -0.0000100    0.0004125
  -0.0050095    0.0003875
  -0.0100090    0.0003624
  -0.0150085    0.0003373
  -0.0200080    0.0003123
  -0.0250075    0.0002872
  -0.0300070    0.0002622
  -0.0350065    0.0002371
  -0.0400060    0.0002120
  -0.0450055    0.0001870
  -0.0500050    0.0001619
  -0.0550045    0.0001457
  -0.0600040    0.0001295
  -0.0650035    0.0001133
  -0.0700030    0.0000972
  -0.0750025    0.0000810
  -0.0800020    0.0000648
  -0.0850015    0.0000486
  -0.0900010    0.0000324
  -0.0950005    0.0000162
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0008251
  -0.0050095    0.0007749
  -0.0100090    0.0007248
  -0.0150085    0.0006747
  -0.0200080    0.0006246
  -0.0250075    0.0005744
  -0.0300070    0.0005243
  -0.0350065    0.0004742
  -0.0400060    0.0004241
  -0.0450055    0.0003739
  -0.0500050    0.0003238
  -0.0550045    0.0002915
  -0.0600040    0.0002591
  -0.0650035    0.0002267
  -0.0700030    0.0001943
  -0.0750025    0.0001619
  -0.0800020    0.0001295
  -0.0850015    0.0000972
  -0.0900010    0.0000648
  -0.0950005    0.0000324
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0008265
  -0.0050095    0.0007763
  -0.0100090    0.0007261
  -0.0150085    0.0006759
  -0.0200080    0.0006257
  -0.0250075    0.0005755
  -0.0300070    0.0005252
  -0.0350065    0.0004750
  -0.0400060    0.0004248
  -0.0450055    0.0003746
  -0.0500050    0.0003244
  -0.0550045    0.0002920
  -0.0600040    0.0002595
  -0.0650035    0.0002271
  -0.0700030    0.0001946
  -0.0750025    0.0001622
  -0.0800020    0.0001298
  -0.0850015    0.0000973
  -0.0900010    0.0000649
  -0.0950005    0.0000324
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0008306
  -0.0050095    0.0007802
  -0.0100090    0.0007297
  -0.0150085    0.0006792
  -0.0200080    0.0006288
  -0.0250075    0.0005783
  -0.0300070    0.0005279
  -0.0350065    0.0004774
  -0.0400060    0.0004269
  -0.0450055    0.0003765
  -0.0500050    0.0003260
  -0.0550045    0.0002934
  -0.0600040    0.0002608
  -0.0650035    0.0002282
  -0.0700030    0.0001956
  -0.0750025    0.0001630
  -0.0800020    0.0001304
  -0.0850015    0.0000978
  -0.0900010    0.0000652
  -0.0950005    0.0000326
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0008369
  -0.0050095    0.0007860
  -0.0100090    0.0007352
  -0.0150085    0.0006844
  -0.0200080    0.0006335
  -0.0250075    0.0005827
  -0.0300070    0.0005318
  -0.0350065    0.0004810
  -0.0400060    0.0004302
  -0.0450055    0.0003793
  -0.0500050    0.0003285
  -0.0550045    0.0002956
  -0.0600040    0.0002628
  -0.0650035    0.0002299
  -0.0700030    0.0001971
  -0.0750025    0.0001642
  -0.0800020    0.0001314
  -0.0850015    0.0000985
  -0.0900010    0.0000657
  -0.0950005    0.0000328
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100   -0.0005515
  -0.0050095   -0.0005180
  -0.0100090   -0.0004845
  -0.0150085   -0.0004510
  -0.0200080   -0.0004175
  -0.0250075   -0.0003840
  -0.0300070   -0.0003505
  -0.0350065   -0.0003170
  -0.0400060   -0.0002835
  -0.0450055   -0.0002500
  -0.0500050   -0.0002165
  -0.0550045   -0.0001948
  -0.0600040   -0.0001732
  -0.0650035   -0.0001515
  -0.0700030   -0.0001299
  -0.0750025   -0.0001082
  -0.0800020   -0.0000866
  -0.0850015   -0.0000649
  -0.0900010   -0.0000433
  -0.0950005   -0.0000216
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0016662
  -0.0050095    0.0015693
  -0.0100090    0.0014724
  -0.0150085    0.0013755
  -0.0200080    0.0012786
  -0.0250075    0.0011817
  -0.0300070    0.0010848
  -0.0350065    0.0009879
  -0.0400060    0.0008910
  -0.0450055    0.0007941
  -0.0500050    0.0006972
  -0.0550045    0.0006275
  -0.0600040    0.0005578
  -0.0650035    0.0004881
  -0.0700030    0.0004183
  -0.0750025    0.0003486
  -0.0800020    0.0002789
  -0.0850015    0.0002092
  -0.0900010    0.0001394
  -0.0950005    0.0000697
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0115461
  -0.0050095    0.0109041
  -0.0100090    0.0102621
  -0.0150085    0.0096201
  -0.0200080    0.0089781
  -0.0250075    0.0083361
  -0.0300070    0.0076942
  -0.0350065    0.0070522
  -0.0400060    0.0064102
  -0.0450055    0.0057682
  -0.0500050    0.0051263
  -0.0550045    0.0046137
  -0.0600040    0.0041011
  -0.0650035    0.0035884
  -0.0700030    0.0030758
  -0.0750025    0.0025632
  -0.0800020    0.0020505
  -0.0850015    0.0015379
  -0.0900010    0.0010253
  -0.0950005    0.0005126
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
