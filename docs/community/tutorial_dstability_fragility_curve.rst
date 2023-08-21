.. tutorialdstabilityfragilitycurve:

Tutorial Fragility Curve D-Stability
====================================

The main purpose of this example is to demonstrate how to utilize the GEOLib Python package to construct 
a fragility curve depending on various water levels. 

To undertake failure probability studies (or reliability analyses) for levee 
macrostability `Handreiking Faalkansanalyse <https://www.helpdeskwater.nl/publish/pages/144404/11200575-016-geo-0005-v02-r-handreiking_faalkansanalyses_macrostabiliteit_-_definitief.pdf>`_, 
the designer should provide fragility curves. A Fragility Curve represents the (conditional) probability 
of failure as a function of load. In the case of levee macrostability, the water level (h) is usually 
used for this purpose. These curves will later be used to include the uncertainties in the water level 
in the reliability measures of the dike.

After establishing the base macrostability model as a .stix file, the designer may manually evaluate a 
few situations and generate the associated reliability index (:math:`\beta`) as fragility points. In this 
section, we describe an alternative method in which the GEOLib Python package can automate these 
operations and extract the fragility curve. The syntax has been enhanced to incorporate water level 
uncertainty into the fragility curve and calculate the dike's final dependability index. 

The user must first prepare the basis model in D-Stability software and install the GEOLib package. 
The next step is to load the necessary packages.

.. code-block:: python

    from pathlib import Path

    import numpy as np # for array calculations
    import scipy.stats as st # for statisitcal functions
    import pandas as pd # for reading excel files
    from scipy.interpolate import interp1d # for linear interpolation and extrapolation outside the range
    import matplotlib.pyplot as plt #for ploting the results

    from scipy.stats import norm      
    from scipy.stats import gumbel_r #the distribution function of water level

    from geolib.models.dstability import DStabilityModel
    from geolib.models.dstability.internal import PersistableHeadLine, Waternet

In order to change the water level, the phreatic line should be find to be later modified. 
The next line of codes define a function to do this task. 

.. code-block:: python

    def find_phreatic_line(waternet: Waternet) -> PersistableHeadLine:
    """
    Find the phreatic line in a given waternet.

    :param waternet: Waternet to search in
    :return: Phreatic line
    """
    for headline in waternet.HeadLines:
        if headline.Id == waternet.PhreaticLineId:
            return headline
    raise ValueError("No phreatic line found")

The function below computes the fragility curve for a given input file and a range of water levels.

.. code-block:: python

    def calculate_fragility_curve(input_file, z_start, z_end, z_step) -> pd.DataFrame:
    """
    
    This method will raise the first point of the water level by the given step size.

    :param input_file: Path to the input file
    :param z_start: Start of the water level range
    :param z_end: End of the water level range
    :param z_step: Step size of the water level range
    :return: Dataframe with the water level and the corresponding reliability index
    """

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
            output_file = output_folder / (
                input_file_path.stem + "_" + str(new_z) + input_file_path.suffix
            )
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

In the following syntax, the address of base model i.e., ``fc.stix`` is introduced. 
The user should also provide the interested water level range through `z_start` and `z_end`. 
The user may also indicate a folder where the outcomes of different scenarios and the graphs shall be 
saved. 

.. code-block:: python

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
    plt.plot(df["Waterlevel"], df["Beta"], "o-")
    plt.xlabel("Water level [m]")
    plt.ylabel("Reliability index")
    plt.title("Fragility curve")
    plt.grid()
    plt.savefig(output_folder / "fragility_curve.png")
    plt.show()

This tutorial's base file fc.stix and source code can be 
obtained `here <https://github.com/Deltares/GEOLib/tree/master/examples/dstability/fragility_curve_berm>`_.

Determining final failure probability ("integrating out" load uncertainty)
--------------------------------------------------------------------------

As a final step, the reliability measure of the levee is calculated by combining the conditional failure probability (fragility curve) with the load statistics (in this case, water level statistics). This step is often called "integrating out" because the next integral must be solved: 

.. math:: 
    
    P_f=\int \Phi[-\beta(h)] f_h(h) d_h

where :math:`f_h(h)` is the probability density function of the water level (or other load variable) 
and :math:`\Phi` is the standard normal cumulative probability function. This integral can be quickly 
solved using numerical integration as follows.

Note: In this example, Gumbel distribution is assigned as the PDF for waterlevel 

.. code-block:: python

    # Define water level range
    range_h = [-10,2] 

    # Define bin width for integration water level distribution, 𝑑ℎ 
    delta_h = 0.1

    # Define the distribution parameters of the load (water level) uncertainty distribution
    mu= -5 
    std = 0.2

    # indicating the obtained fragility points (𝛽 - h) from the above calculations
    b = df["Beta"].to_numpy()
    h = df["Waterlevel"].to_numpy()

    # function to intepolate the FC curve between fragility points
    def densify_extrapolate(x, y, xrange, xdelta):
        xnew = np.arange(xrange[0], xrange[1] + xdelta, xdelta)
        f = interp1d(x, y, kind='linear', bounds_error=False, fill_value='extrapolate')
        ynew = f(xnew)
        return xnew, ynew   

    # intepolate the fragility curve
    H, B = densify_extrapolate(h, b, range_h, delta_h)


    # breaking the probability density function of load into bins with width of 𝑑ℎ

    xnew = np.arange(range_h[0], range_h[1]+delta_h, delta_h)

    fh = np.empty(len(xnew), dtype=object)

    for h in range(len(xnew)):
        fh[h]=gumbel_r.pdf(xnew[h], loc=mu, scale=std)   #Gumbel distribution is assumed for 𝑓ℎ(ℎ)
    
        
    sumFh = sum(fh)*delta_h

    # calculating Φ[−𝛽(ℎ)]
    P_fh = norm.cdf(-1*B)  

    Pf = P_fh* fh * delta_h  

    sumPf = sum(Pf)/sumFh  

    # evaluating the relevant relaibiltiy index for th eobtained failure probbaility
    Beta = -1*norm.ppf(sumPf)      

    print('Final Beta after integration = ', Beta)
