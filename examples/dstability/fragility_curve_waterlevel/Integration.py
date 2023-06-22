from geolib.models.dstability import DStabilityModel
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


import numpy as np # for array calculations
import scipy.stats as st # for statisitcal functions
import pandas as pd # for reading excel files
from scipy.interpolate import interp1d # for linear interpolation and extrapolation outside the range
import matplotlib.pyplot as plt

from scipy.stats import norm
from scipy.stats import gumbel_r



from geolib.models.dstability.internal import PersistableHeadLine, Waternet


def find_phreatic_line(waternet: Waternet) -> PersistableHeadLine:
    '''
    Find the phreatic line in a given waternet.

    :param waternet: Waternet to search in
    :return: Phreatic line
    '''
    for headline in waternet.HeadLines:
        if headline.Id == waternet.PhreaticLineId:
            return headline
    raise ValueError("No phreatic line found")


def calculate_fragility_curve(input_file, z_start, z_end, z_step) -> pd.DataFrame:
    '''
    Calculate the fragility curve for a given input file and a range of water levels.

    This method will raise the first point of the water level by the given step size.

    :param input_file: Path to the input file
    :param z_start: Start of the water level range
    :param z_end: End of the water level range
    :param z_step: Step size of the water level range
    :return: Dataframe with the water level and the corresponding reliability index
    '''

    # Prepare dataframe
    df = pd.DataFrame(columns=["Waterlevel", "Beta", "Filename"])

    # Parse input file
    dm = DStabilityModel()
    input_file_path = Path(input_file)
    dm.parse(input_file_path)

    output_folder = input_file_path.parent / "output"

    # Create output folder if not exists
    if not output_folder.exists():
        output_folder.mkdir()
    else:
        # Delete old results
        for file in output_folder.glob("*.*"):
            file.unlink()

    # Loop over water levels
    for i in range(int((z_end - z_start) / z_step)):
        # Calculate new water level
        new_z = z_start + i * z_step

        # Find phreatic line and set new water level
        phreatic_line = find_phreatic_line(dm.datastructure.waternets[0])
        headline_points = phreatic_line.Points
        if headline_points is not None and headline_points[0] is not None:
            headline_points[0].Z = new_z

            # Serialize and execute
            output_file = output_folder / (input_file_path.stem + "_" + str(new_z) + input_file_path.suffix)
            dm.serialize(Path(output_file))
            dm.execute()

            # Get result
            result = dm.get_result(0, 0)
            print("Result of Z level: " + str(phreatic_line.Points[0].Z))
            print("Reliability index: " + str(result.ReliabilityIndex))

            # Add result to dataframe
            df.loc[i] = [
                phreatic_line.Points[0].Z,
                result.ReliabilityIndex,
                output_file,
            ]

    return df


if __name__ == "__main__":
    # Define input file and water level range
    input_file = "examples\\dstability\\fragility_curve_waterlevel\\fc.stix"
    z_start = -9
    z_end = 3
    z_step = 6

    # Calculate fragility curve
    df = calculate_fragility_curve(input_file, z_start, z_end, z_step)

    # Save dataframe to csv in subfolder of input file
    output_folder = Path(input_file).parent / "output"
    df.to_csv(output_folder / "fragility_curve.csv")

    # Plot fragility curve
    plt.plot(df["Waterlevel"], df["Beta"], "o-", label='FC')
    print(df["Waterlevel"], df["Beta"])
    #plt.ylabel("Reliability index")
    #plt.title("Fragility curve")
    plt.grid()
    #plt.savefig(output_folder / "fragility_curve.png")
    #plt.show()


range_h = [-10,2]
delta_h = 0.1
b = df["Beta"].to_numpy()
h = df["Waterlevel"].to_numpy()   
print("A =", h)  


def densify_extrapolate(x, y, xrange, xdelta):
    xnew = np.arange(xrange[0], xrange[1] + xdelta, xdelta)
    f = interp1d(x, y, kind='linear', bounds_error=False, fill_value='extrapolate')
    ynew = f(xnew)
    return xnew, ynew   

H, B = densify_extrapolate(h, b, range_h, delta_h)

#print("H =", H)  
print("Beta =", B)

mu= -5 
std = 0.2
xnew = np.arange(range_h[0], range_h[1]+delta_h, delta_h)

fh = np.empty(len(xnew), dtype=object)



for h in range(len(xnew)):
    fh[h]=gumbel_r.pdf(xnew[h], loc=mu, scale=std)   #Gumbel distribution

print('f(h) = ', fh)    
sumFh = sum(fh)*delta_h


plt.plot(xnew , fh,'r-', lw=5, alpha=0.6, label='f_h')
plt.legend(loc='best', frameon=False)

#gumbel_r.pdf(x, loc=5, scale=2)


P_fh = norm.cdf(-1*B) #P(f|h)        *I coloumn


Pf = P_fh* fh * delta_h  #P(f/h)*f(h)*delta     *K coloumn
sumPf = sum(Pf)/sumFh  #K3   cell




Beta = -1*norm.ppf(sumPf)                        #K2
print('finalBeta after integration = ', Beta)


plt.show()

