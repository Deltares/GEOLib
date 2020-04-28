Dump file for D-Settlement : Settlement of soil.
==============================================================================
COMPANY    : 

DATE       : 8-3-2019
TIME       : 16:04:02
FILENAME   : D:\DSettlement\Test Results DSettlement\Benchmarks Branch\bm3-7b.sld
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
SoilPreconKoppejanType=1
SoilUseEquivalentAge=0
SoilEquivalentAge=0.00E+00
SoilPc=8.00E+00
SoilOCR=2.00
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
Benchmark MSettle: bm3-7b
Pc compression
Constant within the layer and correction at t=0
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
1 : Precon. pressure within a layer = Constant, correction at t=0 [days]
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
   0.1000000      0.0031854      0.0031854      0.0031854      0.0031854      0.0031854      0.0031854      0.0031854      0.0031854   
   0.2050612      0.0031912      0.0031912      0.0031912      0.0031912      0.0031912      0.0031912      0.0031912      0.0031912   
   0.3387023      0.0031984      0.0031984      0.0031984      0.0031984      0.0031984      0.0031984      0.0031984      0.0031984   
   0.5086977      0.0032072      0.0032072      0.0032072      0.0032072      0.0032072      0.0032072      0.0032072      0.0032072   
   0.7249370      0.0032180      0.0032180      0.0032180      0.0032180      0.0032180      0.0032180      0.0032180      0.0032180   
   1.0000000      0.0032310      0.0032310      0.0032310      0.0032310      0.0032310      0.0032310      0.0032310      0.0032310   
   1.1000000      0.0032356      0.0018600      0.0018600      0.0018600      0.0018600      0.0018600      0.0018600      0.0018600   
   1.2050612      0.0032403      0.0018617      0.0018617      0.0018617      0.0018617      0.0018617      0.0018617      0.0018617   
   1.3387023      0.0032461      0.0018638      0.0018638      0.0018638      0.0018638      0.0018638      0.0018638      0.0018638   
   1.5086977      0.0032533      0.0018664      0.0018664      0.0018664      0.0018664      0.0018664      0.0018664      0.0018664   
   1.7249370      0.0032622      0.0018697      0.0018697      0.0018697      0.0018697      0.0018697      0.0018697      0.0018697   
   2.0000000      0.0032730      0.0018738      0.0018738      0.0018738      0.0018738      0.0018738      0.0018738      0.0018738   
   2.1000000      0.0032768      0.0018752      0.0050606      0.0050606      0.0050606      0.0050606      0.0050606      0.0050606   
   2.2050612      0.0032807      0.0018767      0.0050679      0.0050679      0.0050679      0.0050679      0.0050679      0.0050679   
   2.3387023      0.0032857      0.0018786      0.0050770      0.0050770      0.0050770      0.0050770      0.0050770      0.0050770   
   2.5086977      0.0032917      0.0018810      0.0050882      0.0050882      0.0050882      0.0050882      0.0050882      0.0050882   
   2.7249370      0.0032993      0.0018839      0.0051019      0.0051019      0.0051019      0.0051019      0.0051019      0.0051019   
   3.0000000      0.0033085      0.0018875      0.0051186      0.0051186      0.0051186      0.0051186      0.0051186      0.0051186   
   3.1000000      0.0033118      0.0018888      0.0051244      0.0074318      0.0074318      0.0074318      0.0074318      0.0074318   
   3.2050612      0.0033151      0.0018902      0.0051305      0.0074421      0.0074421      0.0074421      0.0074421      0.0074421   
   3.3387023      0.0033194      0.0018918      0.0051380      0.0074548      0.0074548      0.0074548      0.0074548      0.0074548   
   3.5086977      0.0033246      0.0018940      0.0051473      0.0074705      0.0074705      0.0074705      0.0074705      0.0074705   
   3.7249370      0.0033312      0.0018966      0.0051588      0.0074898      0.0074898      0.0074898      0.0074898      0.0074898   
   4.0000000      0.0033392      0.0018999      0.0051729      0.0075133      0.0075133      0.0075133      0.0075133      0.0075133   
   4.1000000      0.0033421      0.0019010      0.0051779      0.0075216      0.0065599      0.0065599      0.0065599      0.0065599   
   4.2050612      0.0033450      0.0019023      0.0051830      0.0075302      0.0065663      0.0065663      0.0065663      0.0065663   
   4.3387023      0.0033488      0.0019038      0.0051894      0.0075408      0.0065744      0.0065744      0.0065744      0.0065744   
   4.5086977      0.0033534      0.0019057      0.0051974      0.0075541      0.0065844      0.0065844      0.0065844      0.0065844   
   4.7249370      0.0033592      0.0019081      0.0052073      0.0075704      0.0065968      0.0065968      0.0065968      0.0065968   
   5.0000000      0.0033663      0.0019111      0.0052195      0.0075904      0.0066121      0.0066121      0.0066121      0.0066121   
   5.1000000      0.0033689      0.0019121      0.0052239      0.0075975      0.0066175      0.0089249      0.0089249      0.0089249   
   5.2050612      0.0033715      0.0019132      0.0052284      0.0076048      0.0066232      0.0089348      0.0089348      0.0089348   
   5.3387023      0.0033748      0.0019146      0.0052340      0.0076140      0.0066302      0.0089471      0.0089471      0.0089471   
   5.5086977      0.0033790      0.0019164      0.0052410      0.0076254      0.0066391      0.0089623      0.0089623      0.0089623   
   5.7249370      0.0033842      0.0019185      0.0052497      0.0076396      0.0066500      0.0089810      0.0089810      0.0089810   
   6.0000000      0.0033906      0.0019213      0.0052605      0.0076570      0.0066636      0.0090040      0.0090040      0.0090040   
   6.1000000      0.0033929      0.0019222      0.0052643      0.0076632      0.0066684      0.0090121      0.0122478      0.0122478   
   6.2050612      0.0033953      0.0019232      0.0052683      0.0076697      0.0066734      0.0090205      0.0122621      0.0122621   
   6.3387023      0.0033982      0.0019245      0.0052733      0.0076777      0.0066797      0.0090311      0.0122800      0.0122800   
   6.5086977      0.0034020      0.0019261      0.0052795      0.0076878      0.0066875      0.0090441      0.0123020      0.0123020   
   6.7249370      0.0034067      0.0019281      0.0052873      0.0077003      0.0066973      0.0090603      0.0123292      0.0123292   
   7.0000000      0.0034125      0.0019306      0.0052970      0.0077158      0.0067095      0.0090803      0.0123624      0.0123624   
   7.1000000      0.0034146      0.0019315      0.0053004      0.0077213      0.0067138      0.0090874      0.0123741      0.0164455   
   7.2050612      0.0034168      0.0019325      0.0053040      0.0077270      0.0067183      0.0090947      0.0123862      0.0164651   
   7.3387023      0.0034195      0.0019336      0.0053085      0.0077342      0.0067239      0.0091040      0.0124014      0.0164894   
   7.5086977      0.0034229      0.0019351      0.0053141      0.0077432      0.0067310      0.0091155      0.0124202      0.0165195   
   7.7249370      0.0034272      0.0019370      0.0053211      0.0077544      0.0067399      0.0091297      0.0124435      0.0165566   
   8.0000000      0.0034325      0.0019393      0.0053299      0.0077683      0.0067509      0.0091474      0.0124721      0.0166019   
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
   5.0001800      0.0001000      8.0000000     45.1661991      0.1661191   
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
      1     -0.0023323     -0.0004665      0.0000764      0.0000127      0.0181835      0.0030306   
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
   0.0031854   10.0000800
   0.0012955   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.205061218966    =  Time in days
   0.0031912   10.0000800
   0.0012979   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.338702261693    =  Time in days
   0.0031984   10.0000800
   0.0013008   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.508697703179    =  Time in days
   0.0032072   10.0000800
   0.0013044   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   0.724937037565    =  Time in days
   0.0032180   10.0000800
   0.0013088   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.000000000000    =  Time in days
   0.0032310   10.0000800
   0.0013141   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.100000000000    =  Time in days
   0.0018600    5.0000800
   0.0007760   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.205061218966    =  Time in days
   0.0018617    5.0000800
   0.0007767   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.338702261693    =  Time in days
   0.0018638    5.0000800
   0.0007776   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.508697703179    =  Time in days
   0.0018664    5.0000800
   0.0007787   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   1.724937037565    =  Time in days
   0.0018697    5.0000800
   0.0007801   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.000000000000    =  Time in days
   0.0018738    5.0000800
   0.0007819   10.4000000
   0.0000000   15.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.100000000000    =  Time in days
   0.0050606   10.0000800
   0.0020780   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.205061218966    =  Time in days
   0.0050679   10.0000800
   0.0020810   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.338702261693    =  Time in days
   0.0050770   10.0000800
   0.0020848   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.508697703179    =  Time in days
   0.0050882   10.0000800
   0.0020894   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   2.724937037565    =  Time in days
   0.0051019   10.0000800
   0.0020950   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.000000000000    =  Time in days
   0.0051186   10.0000800
   0.0021019   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.100000000000    =  Time in days
   0.0074318   15.0000800
   0.0030817   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.205061218966    =  Time in days
   0.0074421   15.0000800
   0.0030860   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.338702261693    =  Time in days
   0.0074548   15.0000800
   0.0030913   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.508697703179    =  Time in days
   0.0074705   15.0000800
   0.0030978   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   3.724937037565    =  Time in days
   0.0074898   15.0000800
   0.0031059   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.000000000000    =  Time in days
   0.0075133   15.0000800
   0.0031157   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.100000000000    =  Time in days
   0.0065599   10.0000800
   0.0027117   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.205061218966    =  Time in days
   0.0065663   10.0000800
   0.0027144   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.338702261693    =  Time in days
   0.0065744   10.0000800
   0.0027177   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.508697703179    =  Time in days
   0.0065844   10.0000800
   0.0027218   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   4.724937037565    =  Time in days
   0.0065968   10.0000800
   0.0027270   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.000000000000    =  Time in days
   0.0066121   10.0000800
   0.0027333   15.4000000
   0.0000000   20.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.100000000000    =  Time in days
   0.0089249   15.0000800
   0.0037130   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.205061218966    =  Time in days
   0.0089348   15.0000800
   0.0037171   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.338702261693    =  Time in days
   0.0089471   15.0000800
   0.0037222   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.508697703179    =  Time in days
   0.0089623   15.0000800
   0.0037286   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   5.724937037565    =  Time in days
   0.0089810   15.0000800
   0.0037365   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.000000000000    =  Time in days
   0.0090040   15.0000800
   0.0037461   20.4000000
   0.0000000   25.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.100000000000    =  Time in days
   0.0122478   25.0000800
   0.0051908   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.205061218966    =  Time in days
   0.0122621   25.0000800
   0.0051970   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.338702261693    =  Time in days
   0.0122800   25.0000800
   0.0052046   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.508697703179    =  Time in days
   0.0123020   25.0000800
   0.0052141   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   6.724937037565    =  Time in days
   0.0123292   25.0000800
   0.0052257   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.000000000000    =  Time in days
   0.0123624   25.0000800
   0.0052400   30.4000000
   0.0000000   35.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.100000000000    =  Time in days
   0.0164455   45.0000800
   0.0071390   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.205061218966    =  Time in days
   0.0164651   45.0000800
   0.0071476   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.338702261693    =  Time in days
   0.0164894   45.0000800
   0.0071584   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.508697703179    =  Time in days
   0.0165195   45.0000800
   0.0071717   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   7.724937037565    =  Time in days
   0.0165566   45.0000800
   0.0071881   50.4000000
   0.0000000   55.8000000
[End of Vertical Data at Time]
[Vertical Data at Time]
   8.000000000000    =  Time in days
   0.0166019   45.0000800
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
  -0.0000100    0.0000319
  -0.0050095    0.0000300
  -0.0100090    0.0000281
  -0.0150085    0.0000262
  -0.0200080    0.0000243
  -0.0250075    0.0000224
  -0.0300070    0.0000205
  -0.0350065    0.0000186
  -0.0400060    0.0000167
  -0.0450055    0.0000148
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
  -0.0000100    0.0000637
  -0.0050095    0.0000599
  -0.0100090    0.0000561
  -0.0150085    0.0000524
  -0.0200080    0.0000486
  -0.0250075    0.0000448
  -0.0300070    0.0000410
  -0.0350065    0.0000372
  -0.0400060    0.0000335
  -0.0450055    0.0000297
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
  -0.0000100    0.0001593
  -0.0050095    0.0001498
  -0.0100090    0.0001404
  -0.0150085    0.0001309
  -0.0200080    0.0001215
  -0.0250075    0.0001120
  -0.0300070    0.0001026
  -0.0350065    0.0000931
  -0.0400060    0.0000837
  -0.0450055    0.0000742
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
  -0.0000100    0.0003185
  -0.0050095    0.0002996
  -0.0100090    0.0002807
  -0.0150085    0.0002618
  -0.0200080    0.0002429
  -0.0250075    0.0002240
  -0.0300070    0.0002051
  -0.0350065    0.0001862
  -0.0400060    0.0001673
  -0.0450055    0.0001484
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
  -0.0000100    0.0006371
  -0.0050095    0.0005993
  -0.0100090    0.0005615
  -0.0150085    0.0005237
  -0.0200080    0.0004859
  -0.0250075    0.0004481
  -0.0300070    0.0004103
  -0.0350065    0.0003725
  -0.0400060    0.0003347
  -0.0450055    0.0002969
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
  -0.0000100    0.0015927
  -0.0050095    0.0014982
  -0.0100090    0.0014037
  -0.0150085    0.0013092
  -0.0200080    0.0012147
  -0.0250075    0.0011202
  -0.0300070    0.0010257
  -0.0350065    0.0009312
  -0.0400060    0.0008367
  -0.0450055    0.0007422
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
  -0.0000100    0.0031854
  -0.0050095    0.0029964
  -0.0100090    0.0028074
  -0.0150085    0.0026184
  -0.0200080    0.0024294
  -0.0250075    0.0022403
  -0.0300070    0.0020513
  -0.0350065    0.0018623
  -0.0400060    0.0016733
  -0.0450055    0.0014843
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
  -0.0000100    0.0031910
  -0.0050095    0.0030017
  -0.0100090    0.0028123
  -0.0150085    0.0026230
  -0.0200080    0.0024336
  -0.0250075    0.0022443
  -0.0300070    0.0020550
  -0.0350065    0.0018656
  -0.0400060    0.0016763
  -0.0450055    0.0014869
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
  -0.0000100    0.0032069
  -0.0050095    0.0030166
  -0.0100090    0.0028263
  -0.0150085    0.0026360
  -0.0200080    0.0024457
  -0.0250075    0.0022555
  -0.0300070    0.0020652
  -0.0350065    0.0018749
  -0.0400060    0.0016846
  -0.0450055    0.0014943
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
  -0.0000100    0.0032310
  -0.0050095    0.0030393
  -0.0100090    0.0028476
  -0.0150085    0.0026559
  -0.0200080    0.0024642
  -0.0250075    0.0022725
  -0.0300070    0.0020808
  -0.0350065    0.0018890
  -0.0400060    0.0016973
  -0.0450055    0.0015056
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
  -0.0000100    0.0018738
  -0.0050095    0.0017646
  -0.0100090    0.0016554
  -0.0150085    0.0015462
  -0.0200080    0.0014370
  -0.0250075    0.0013278
  -0.0300070    0.0012186
  -0.0350065    0.0011094
  -0.0400060    0.0010002
  -0.0450055    0.0008910
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
  -0.0000100    0.0066121
  -0.0050095    0.0062242
  -0.0100090    0.0058363
  -0.0150085    0.0054484
  -0.0200080    0.0050604
  -0.0250075    0.0046725
  -0.0300070    0.0042846
  -0.0350065    0.0038967
  -0.0400060    0.0035088
  -0.0450055    0.0031208
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
  -0.0000100    0.0166019
  -0.0050095    0.0156624
  -0.0100090    0.0147230
  -0.0150085    0.0137835
  -0.0200080    0.0128440
  -0.0250075    0.0119045
  -0.0300070    0.0109651
  -0.0350065    0.0100256
  -0.0400060    0.0090861
  -0.0450055    0.0081466
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
