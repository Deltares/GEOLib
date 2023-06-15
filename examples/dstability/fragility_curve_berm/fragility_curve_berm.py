from geolib.geometry.one import Point
from geolib.models.dstability import DStabilityModel
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


def calculate_fragility_curve(input_file, fixed_berm_points, varying_berm_points, length_start, length_end, length_step) -> pd.DataFrame:
    '''
    Calculate the fragility curve for a given input file and berm length range.

    :param input_file: Input file
    :param fixed_berm_points: Fixed berm points
    :param varying_berm_points: Varying berm points
    :param length_start: Start of berm length range
    :param length_end: End of berm length range
    :param length_step: Step size of berm length range
    :return: Dataframe with results
    '''

    # Prepare dataframe
    df = pd.DataFrame(columns=["BermLength", "Beta", "Filename"])

    input_file_path = Path(input_file)
    output_folder = input_file_path.parent / "output"

    # Create output folder if not exists
    if not output_folder.exists():
        output_folder.mkdir()
    else:
        # Delete old results
        for file in output_folder.glob("*.*"):
            file.unlink()

    # Loop over water levels
    for i in range(int((length_end - length_start) / length_step)):
        dm = DStabilityModel()
        dm.parse(input_file_path)
        # Calculate new water level
        new_length = length_start + i * length_step

        updated_berm_points = [Point(x=point.x + new_length, z=point.z) for point in varying_berm_points]
        new_berm_points = fixed_berm_points + updated_berm_points
        dm.add_layer(new_berm_points, "Sand", "Berm")

        # Serialize and execute
        output_file = output_folder / (input_file_path.stem + "_" + str(new_length) + input_file_path.suffix)
        dm.serialize(Path(output_file))
        dm.execute()

        # Get result
        result = dm.get_result(0, 0)
        print("Result of berm length: " + str(new_length))
        print("Reliability index: " + str(result.ReliabilityIndex))

        # Add result to dataframe
        df.loc[i] = [
            new_length,
            result.ReliabilityIndex,
            output_file,
        ]

    return df


if __name__ == "__main__":
    # Define input file and water level range
    input_file = "examples\\dstability\\fragility_curve_berm\\fc.stix"
    z_start = 1
    z_end = 20
    z_step = 2

    fixed_berm_points = [
        Point(x=70, z=-10),
        Point(x=66, z=-6),
    ]

    varying_berm_points = [
        Point(x=66, z=-6),
        Point(x=70, z=-10),
    ]

    # Calculate fragility curve
    df = calculate_fragility_curve(input_file, fixed_berm_points, varying_berm_points, z_start, z_end, z_step)

    # Save dataframe to csv in subfolder of input file
    output_folder = Path(input_file).parent / "output"
    df.to_csv(output_folder / "fragility_curve.csv")

    # Plot fragility curve
    plt.plot(df["BermLength"], df["Beta"], "o-")
    plt.xlabel("Berm length [m]")
    plt.ylabel("Reliability index")
    plt.title("Fragility curve")
    plt.grid()
    plt.savefig(output_folder / "fragility_curve.png")
    plt.show()