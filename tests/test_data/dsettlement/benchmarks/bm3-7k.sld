Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 8-3-2019
TIME       : 16:04:03
FILENAME   : D:\DSettlement\Test Results DSettlement\Benchmarks Branch\bm3-7k.sld
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
SoilPreconKoppejanType=0
SoilUseEquivalentAge=0
SoilEquivalentAge=0.00E+00
SoilPc=8.00E+00
SoilOCR=1.20
SoilPOP=7.72
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
Benchmark MSettle: bm3-7k
OCR compression
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
   0.1000000      0.0022044      0.0022044      0.0022044      0.0022044      0.0022044      0.0022044      0.0022044      0.0022044   
   0.2050612      0.0022085      0.0022085      0.0022085      0.0022085      0.0022085      0.0022085      0.0022085      0.0022085   
   0.3387023      0.0022134      0.0022134      0.0022134      0.0022134      0.0022134      0.0022134      0.0022134      0.0022134   
   0.5086977      0.0022196      0.0022196      0.0022196      0.0022196      0.0022196      0.0022196      0.0022196      0.0022196   
   0.7249370      0.0022270      0.0022270      0.0022270      0.0022270      0.0022270      0.0022270      0.0022270      0.0022270   
   1.0000000      0.0022360      0.0022360      0.0022360      0.0022360      0.0022360      0.0022360      0.0022360      0.0022360   
   1.1000000      0.0022392      0.0008636      0.0008636      0.0008636      0.0008636      0.0008636      0.0008636      0.0008636   
   1.2050612      0.0022424      0.0008638      0.0008638      0.0008638      0.0008638      0.0008638      0.0008638      0.0008638   
   1.3387023      0.0022465      0.0008642      0.0008642      0.0008642      0.0008642      0.0008642      0.0008642      0.0008642   
   1.5086977      0.0022515      0.0008646      0.0008646      0.0008646      0.0008646      0.0008646      0.0008646      0.0008646   
   1.7249370      0.0022576      0.0008651      0.0008651      0.0008651      0.0008651      0.0008651      0.0008651      0.0008651   
   2.0000000      0.0022651      0.0008658      0.0008658      0.0008658      0.0008658      0.0008658      0.0008658      0.0008658   
   2.1000000      0.0022677      0.0008661      0.0030705      0.0030705      0.0030705      0.0030705      0.0030705      0.0030705   
   2.2050612      0.0022704      0.0008664      0.0030749      0.0030749      0.0030749      0.0030749      0.0030749      0.0030749   
   2.3387023      0.0022738      0.0008668      0.0030802      0.0030802      0.0030802      0.0030802      0.0030802      0.0030802   
   2.5086977      0.0022780      0.0008673      0.0030868      0.0030868      0.0030868      0.0030868      0.0030868      0.0030868   
   2.7249370      0.0022832      0.0008679      0.0030949      0.0030949      0.0030949      0.0030949      0.0030949      0.0030949   
   3.0000000      0.0022896      0.0008687      0.0031047      0.0031047      0.0031047      0.0031047      0.0031047      0.0031047   
   3.1000000      0.0022919      0.0008689      0.0031081      0.0054155      0.0054155      0.0054155      0.0054155      0.0054155   
   3.2050612      0.0022942      0.0008692      0.0031117      0.0054233      0.0054233      0.0054233      0.0054233      0.0054233   
   3.3387023      0.0022972      0.0008696      0.0031161      0.0054329      0.0054329      0.0054329      0.0054329      0.0054329   
   3.5086977      0.0023008      0.0008701      0.0031216      0.0054448      0.0054448      0.0054448      0.0054448      0.0054448   
   3.7249370      0.0023053      0.0008708      0.0031284      0.0054594      0.0054594      0.0054594      0.0054594      0.0054594   
   4.0000000      0.0023109      0.0008715      0.0031366      0.0054771      0.0054771      0.0054771      0.0054771      0.0054771   
   4.1000000      0.0023129      0.0008718      0.0031395      0.0054833      0.0045216      0.0045216      0.0045216      0.0045216   
   4.2050612      0.0023149      0.0008721      0.0031426      0.0054897      0.0045259      0.0045259      0.0045259      0.0045259   
   4.3387023      0.0023175      0.0008725      0.0031463      0.0054977      0.0045313      0.0045313      0.0045313      0.0045313   
   4.5086977      0.0023207      0.0008730      0.0031510      0.0055077      0.0045380      0.0045380      0.0045380      0.0045380   
   4.7249370      0.0023247      0.0008736      0.0031569      0.0055199      0.0045463      0.0045463      0.0045463      0.0045463   
   5.0000000      0.0023297      0.0008744      0.0031640      0.0055349      0.0045566      0.0045566      0.0045566      0.0045566   
   5.1000000      0.0023314      0.0008747      0.0031666      0.0055402      0.0045602      0.0068676      0.0068676      0.0068676   
   5.2050612      0.0023332      0.0008750      0.0031692      0.0055457      0.0045640      0.0068756      0.0068756      0.0068756   
   5.3387023      0.0023355      0.0008753      0.0031725      0.0055525      0.0045687      0.0068856      0.0068856      0.0068856   
   5.5086977      0.0023384      0.0008758      0.0031766      0.0055610      0.0045747      0.0068979      0.0068979      0.0068979   
   5.7249370      0.0023420      0.0008764      0.0031817      0.0055716      0.0045820      0.0069130      0.0069130      0.0069130   
   6.0000000      0.0023464      0.0008771      0.0031880      0.0055846      0.0045911      0.0069316      0.0069316      0.0069316   
   6.1000000      0.0023480      0.0008774      0.0031903      0.0055892      0.0045943      0.0069381      0.0101738      0.0101738   
   6.2050612      0.0023497      0.0008777      0.0031926      0.0055940      0.0045977      0.0069449      0.0101865      0.0101865   
   6.3387023      0.0023517      0.0008780      0.0031955      0.0056000      0.0046019      0.0069533      0.0102022      0.0102022   
   6.5086977      0.0023543      0.0008785      0.0031992      0.0056074      0.0046072      0.0069638      0.0102217      0.0102217   
   6.7249370      0.0023576      0.0008790      0.0032038      0.0056167      0.0046137      0.0069768      0.0102456      0.0102456   
   7.0000000      0.0023616      0.0008797      0.0032094      0.0056282      0.0046219      0.0069927      0.0102748      0.0102748   
   7.1000000      0.0023631      0.0008800      0.0032114      0.0056323      0.0046248      0.0069984      0.0102851      0.0143565   
   7.2050612      0.0023646      0.0008803      0.0032135      0.0056366      0.0046278      0.0070043      0.0102958      0.0143746   
   7.3387023      0.0023665      0.0008806      0.0032161      0.0056419      0.0046316      0.0070116      0.0103090      0.0143971   
   7.5086977      0.0023688      0.0008810      0.0032194      0.0056485      0.0046364      0.0070208      0.0103255      0.0144249   
   7.7249370      0.0023718      0.0008816      0.0032236      0.0056568      0.0046423      0.0070322      0.0103459      0.0144590   
   8.0000000      0.0023755      0.0008822      0.0032287      0.0056671      0.0046497      0.0070462      0.0103709      0.0145007   
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
   5.0001800      0.0001000      9.2400480     45.1451871      0.1451071   
  10.9000000      0.5000000     15.7200000     50.9603441      0.5603441   
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
      1     -0.0023323     -0.0004665      0.0007292      0.0001215      0.0155724      0.0025954   
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
   0.0022044   10.0000800
   0.0007476   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.205061218966    =  Time in days
   0.0022085   10.0000800
   0.0007489   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.338702261693    =  Time in days
   0.0022134   10.0000800
   0.0007506   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.508697703179    =  Time in days
   0.0022196   10.0000800
   0.0007527   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.724937037565    =  Time in days
   0.0022270   10.0000800
   0.0007552   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.000000000000    =  Time in days
   0.0022360   10.0000800
   0.0007583   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.100000000000    =  Time in days
   0.0008636    5.0000800
   0.0002194   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.205061218966    =  Time in days
   0.0008638    5.0000800
   0.0002193   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.338702261693    =  Time in days
   0.0008642    5.0000800
   0.0002192   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.508697703179    =  Time in days
   0.0008646    5.0000800
   0.0002191   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.724937037565    =  Time in days
   0.0008651    5.0000800
   0.0002190   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.000000000000    =  Time in days
   0.0008658    5.0000800
   0.0002189   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.100000000000    =  Time in days
   0.0030705   10.0000800
   0.0009664   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.205061218966    =  Time in days
   0.0030749   10.0000800
   0.0009677   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.338702261693    =  Time in days
   0.0030802   10.0000800
   0.0009694   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.508697703179    =  Time in days
   0.0030868   10.0000800
   0.0009714   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.724937037565    =  Time in days
   0.0030949   10.0000800
   0.0009739   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.000000000000    =  Time in days
   0.0031047   10.0000800
   0.0009769   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.100000000000    =  Time in days
   0.0054155   15.0000800
   0.0019554   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.205061218966    =  Time in days
   0.0054233   15.0000800
   0.0019583   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.338702261693    =  Time in days
   0.0054329   15.0000800
   0.0019619   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.508697703179    =  Time in days
   0.0054448   15.0000800
   0.0019663   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.724937037565    =  Time in days
   0.0054594   15.0000800
   0.0019717   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.000000000000    =  Time in days
   0.0054771   15.0000800
   0.0019782   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.100000000000    =  Time in days
   0.0045216   10.0000800
   0.0015731   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.205061218966    =  Time in days
   0.0045259   10.0000800
   0.0015746   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.338702261693    =  Time in days
   0.0045313   10.0000800
   0.0015764   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.508697703179    =  Time in days
   0.0045380   10.0000800
   0.0015787   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.724937037565    =  Time in days
   0.0045463   10.0000800
   0.0015816   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.000000000000    =  Time in days
   0.0045566   10.0000800
   0.0015851   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.100000000000    =  Time in days
   0.0068676   15.0000800
   0.0025638   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.205061218966    =  Time in days
   0.0068756   15.0000800
   0.0025669   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.338702261693    =  Time in days
   0.0068856   15.0000800
   0.0025707   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.508697703179    =  Time in days
   0.0068979   15.0000800
   0.0025755   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.724937037565    =  Time in days
   0.0069130   15.0000800
   0.0025813   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.000000000000    =  Time in days
   0.0069316   15.0000800
   0.0025884   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.100000000000    =  Time in days
   0.0101738   25.0000800
   0.0040323   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.205061218966    =  Time in days
   0.0101865   25.0000800
   0.0040375   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.338702261693    =  Time in days
   0.0102022   25.0000800
   0.0040440   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.508697703179    =  Time in days
   0.0102217   25.0000800
   0.0040520   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.724937037565    =  Time in days
   0.0102456   25.0000800
   0.0040619   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.000000000000    =  Time in days
   0.0102748   25.0000800
   0.0040739   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.100000000000    =  Time in days
   0.0143565   45.0000800
   0.0059721   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.205061218966    =  Time in days
   0.0143746   45.0000800
   0.0059799   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.338702261693    =  Time in days
   0.0143971   45.0000800
   0.0059896   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.508697703179    =  Time in days
   0.0144249   45.0000800
   0.0060017   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.724937037565    =  Time in days
   0.0144590   45.0000800
   0.0060164   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   8.000000000000    =  Time in days
   0.0145007   45.0000800
   0.0060344   50.4000000
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
  -0.0000100    0.0000220
  -0.0050095    0.0000206
  -0.0100090    0.0000191
  -0.0150085    0.0000177
  -0.0200080    0.0000162
  -0.0250075    0.0000148
  -0.0300070    0.0000133
  -0.0350065    0.0000118
  -0.0400060    0.0000104
  -0.0450055    0.0000089
  -0.0500050    0.0000075
  -0.0550045    0.0000067
  -0.0600040    0.0000060
  -0.0650035    0.0000052
  -0.0700030    0.0000045
  -0.0750025    0.0000037
  -0.0800020    0.0000030
  -0.0850015    0.0000022
  -0.0900010    0.0000015
  -0.0950005    0.0000007
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.002000000000    =  Time in days
  -0.0000100    0.0000441
  -0.0050095    0.0000412
  -0.0100090    0.0000383
  -0.0150085    0.0000353
  -0.0200080    0.0000324
  -0.0250075    0.0000295
  -0.0300070    0.0000266
  -0.0350065    0.0000237
  -0.0400060    0.0000208
  -0.0450055    0.0000179
  -0.0500050    0.0000149
  -0.0550045    0.0000135
  -0.0600040    0.0000120
  -0.0650035    0.0000105
  -0.0700030    0.0000090
  -0.0750025    0.0000075
  -0.0800020    0.0000060
  -0.0850015    0.0000045
  -0.0900010    0.0000030
  -0.0950005    0.0000015
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.005000000000    =  Time in days
  -0.0000100    0.0001102
  -0.0050095    0.0001029
  -0.0100090    0.0000957
  -0.0150085    0.0000884
  -0.0200080    0.0000811
  -0.0250075    0.0000738
  -0.0300070    0.0000665
  -0.0350065    0.0000592
  -0.0400060    0.0000519
  -0.0450055    0.0000447
  -0.0500050    0.0000374
  -0.0550045    0.0000336
  -0.0600040    0.0000299
  -0.0650035    0.0000262
  -0.0700030    0.0000224
  -0.0750025    0.0000187
  -0.0800020    0.0000149
  -0.0850015    0.0000112
  -0.0900010    0.0000075
  -0.0950005    0.0000037
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.010000000000    =  Time in days
  -0.0000100    0.0002204
  -0.0050095    0.0002059
  -0.0100090    0.0001913
  -0.0150085    0.0001767
  -0.0200080    0.0001622
  -0.0250075    0.0001476
  -0.0300070    0.0001330
  -0.0350065    0.0001185
  -0.0400060    0.0001039
  -0.0450055    0.0000893
  -0.0500050    0.0000747
  -0.0550045    0.0000673
  -0.0600040    0.0000598
  -0.0650035    0.0000523
  -0.0700030    0.0000448
  -0.0750025    0.0000374
  -0.0800020    0.0000299
  -0.0850015    0.0000224
  -0.0900010    0.0000149
  -0.0950005    0.0000075
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.020000000000    =  Time in days
  -0.0000100    0.0004409
  -0.0050095    0.0004117
  -0.0100090    0.0003826
  -0.0150085    0.0003535
  -0.0200080    0.0003243
  -0.0250075    0.0002952
  -0.0300070    0.0002660
  -0.0350065    0.0002369
  -0.0400060    0.0002078
  -0.0450055    0.0001786
  -0.0500050    0.0001495
  -0.0550045    0.0001345
  -0.0600040    0.0001196
  -0.0650035    0.0001046
  -0.0700030    0.0000897
  -0.0750025    0.0000747
  -0.0800020    0.0000598
  -0.0850015    0.0000448
  -0.0900010    0.0000299
  -0.0950005    0.0000149
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.050000000000    =  Time in days
  -0.0000100    0.0011022
  -0.0050095    0.0010294
  -0.0100090    0.0009565
  -0.0150085    0.0008837
  -0.0200080    0.0008108
  -0.0250075    0.0007380
  -0.0300070    0.0006651
  -0.0350065    0.0005923
  -0.0400060    0.0005194
  -0.0450055    0.0004466
  -0.0500050    0.0003737
  -0.0550045    0.0003364
  -0.0600040    0.0002990
  -0.0650035    0.0002616
  -0.0700030    0.0002242
  -0.0750025    0.0001869
  -0.0800020    0.0001495
  -0.0850015    0.0001121
  -0.0900010    0.0000747
  -0.0950005    0.0000374
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.100000000000    =  Time in days
  -0.0000100    0.0022044
  -0.0050095    0.0020587
  -0.0100090    0.0019130
  -0.0150085    0.0017673
  -0.0200080    0.0016216
  -0.0250075    0.0014759
  -0.0300070    0.0013302
  -0.0350065    0.0011845
  -0.0400060    0.0010388
  -0.0450055    0.0008931
  -0.0500050    0.0007475
  -0.0550045    0.0006727
  -0.0600040    0.0005980
  -0.0650035    0.0005232
  -0.0700030    0.0004485
  -0.0750025    0.0003737
  -0.0800020    0.0002990
  -0.0850015    0.0002242
  -0.0900010    0.0001495
  -0.0950005    0.0000747
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.200000000000    =  Time in days
  -0.0000100    0.0022083
  -0.0050095    0.0020624
  -0.0100090    0.0019164
  -0.0150085    0.0017704
  -0.0200080    0.0016245
  -0.0250075    0.0014785
  -0.0300070    0.0013326
  -0.0350065    0.0011866
  -0.0400060    0.0010407
  -0.0450055    0.0008947
  -0.0500050    0.0007488
  -0.0550045    0.0006739
  -0.0600040    0.0005990
  -0.0650035    0.0005242
  -0.0700030    0.0004493
  -0.0750025    0.0003744
  -0.0800020    0.0002995
  -0.0850015    0.0002246
  -0.0900010    0.0001498
  -0.0950005    0.0000749
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   0.500000000000    =  Time in days
  -0.0000100    0.0022193
  -0.0050095    0.0020726
  -0.0100090    0.0019259
  -0.0150085    0.0017793
  -0.0200080    0.0016326
  -0.0250075    0.0014859
  -0.0300070    0.0013392
  -0.0350065    0.0011925
  -0.0400060    0.0010458
  -0.0450055    0.0008991
  -0.0500050    0.0007525
  -0.0550045    0.0006773
  -0.0600040    0.0006020
  -0.0650035    0.0005268
  -0.0700030    0.0004515
  -0.0750025    0.0003763
  -0.0800020    0.0003010
  -0.0850015    0.0002258
  -0.0900010    0.0001505
  -0.0950005    0.0000753
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   1.000000000000    =  Time in days
  -0.0000100    0.0022360
  -0.0050095    0.0020882
  -0.0100090    0.0019405
  -0.0150085    0.0017927
  -0.0200080    0.0016449
  -0.0250075    0.0014971
  -0.0300070    0.0013493
  -0.0350065    0.0012015
  -0.0400060    0.0010537
  -0.0450055    0.0009059
  -0.0500050    0.0007582
  -0.0550045    0.0006824
  -0.0600040    0.0006066
  -0.0650035    0.0005307
  -0.0700030    0.0004549
  -0.0750025    0.0003791
  -0.0800020    0.0003033
  -0.0850015    0.0002275
  -0.0900010    0.0001516
  -0.0950005    0.0000758
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   2.000000000000    =  Time in days
  -0.0000100    0.0008658
  -0.0050095    0.0008011
  -0.0100090    0.0007364
  -0.0150085    0.0006717
  -0.0200080    0.0006070
  -0.0250075    0.0005423
  -0.0300070    0.0004776
  -0.0350065    0.0004129
  -0.0400060    0.0003482
  -0.0450055    0.0002835
  -0.0500050    0.0002188
  -0.0550045    0.0001970
  -0.0600040    0.0001751
  -0.0650035    0.0001532
  -0.0700030    0.0001313
  -0.0750025    0.0001094
  -0.0800020    0.0000875
  -0.0850015    0.0000657
  -0.0900010    0.0000438
  -0.0950005    0.0000219
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
   5.000000000000    =  Time in days
  -0.0000100    0.0045566
  -0.0050095    0.0042594
  -0.0100090    0.0039622
  -0.0150085    0.0036651
  -0.0200080    0.0033679
  -0.0250075    0.0030707
  -0.0300070    0.0027735
  -0.0350065    0.0024764
  -0.0400060    0.0021792
  -0.0450055    0.0018820
  -0.0500050    0.0015850
  -0.0550045    0.0014265
  -0.0600040    0.0012680
  -0.0650035    0.0011095
  -0.0700030    0.0009510
  -0.0750025    0.0007925
  -0.0800020    0.0006340
  -0.0850015    0.0004755
  -0.0900010    0.0003170
  -0.0950005    0.0001585
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  10.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  20.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
  50.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 100.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 200.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
 500.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
1000.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
2000.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
5000.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
  -0.1000000    0.0000000
[End of Vertical Data at Fixed Time]
[Vertical Data at Fixed Time]
10000.000000000000    =  Time in days
  -0.0000100    0.0145007
  -0.0050095    0.0136540
  -0.0100090    0.0128073
  -0.0150085    0.0119606
  -0.0200080    0.0111139
  -0.0250075    0.0102671
  -0.0300070    0.0094204
  -0.0350065    0.0085737
  -0.0400060    0.0077270
  -0.0450055    0.0068803
  -0.0500050    0.0060338
  -0.0550045    0.0054304
  -0.0600040    0.0048270
  -0.0650035    0.0042237
  -0.0700030    0.0036203
  -0.0750025    0.0030169
  -0.0800020    0.0024135
  -0.0850015    0.0018101
  -0.0900010    0.0012068
  -0.0950005    0.0006034
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
