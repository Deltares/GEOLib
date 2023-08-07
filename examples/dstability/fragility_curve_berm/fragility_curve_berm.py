from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from geolib.geometry.one import Point
from geolib.models.dstability import DStabilityModel
from geolib.models.dstability.analysis import (
    DStabilityBishopAnalysisMethod,
    DStabilityCircle,
)
from geolib.models.dstability.internal import CalculationTypeEnum


def calculate_fragility_curve(
    input_file,
    fixed_berm_points,
    varying_berm_points,
    length_start,
    length_end,
    length_step,
) -> pd.DataFrame:
    """
    Calculate the fragility curve for a given input file and berm length range.

    :param input_file: Input file
    :param fixed_berm_points: Fixed berm points
    :param varying_berm_points: Varying berm points
    :param length_start: Start of berm length range
    :param length_end: End of berm length range
    :param length_step: Step size of berm length range
    :return: Dataframe with results
    """

    # Prepare dataframe
    df = pd.DataFrame(columns=["BermLength", "Circle", "Layers", "Beta", "Filename"])

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

        # Calculate new berm length
        new_length = length_start + i * length_step

        # Add new berm
        updated_berm_points = [
            Point(x=point.x + new_length, z=point.z) for point in varying_berm_points
        ]
        new_berm_points = fixed_berm_points + updated_berm_points
        dm.add_layer(new_berm_points, "Sand", "Berm")

        # Serialize and execute
        output_file = output_folder / (
            input_file_path.stem + "_" + str(new_length) + input_file_path.suffix
        )
        dm.serialize(Path(output_file))
        dm.execute()

        # Calculate result using Bishop Brute Force method configured in fc.stix
        result = dm.get_result(0, 0)
        circle = result.Circle

        # Set resulting circle on Bishop Single Probabilistic calculation
        bishop_analysis_method = DStabilityBishopAnalysisMethod(
            circle=DStabilityCircle(
                center=Point(x=circle.Center.X, z=circle.Center.Z), radius=circle.Radius
            )
        )
        dm.set_model(bishop_analysis_method)
        dm.datastructure.calculationsettings[
            0
        ].CalculationType = CalculationTypeEnum.PROBABILISTIC

        # Re-calculate to get Reliability Index
        dm.serialize(Path(output_file))
        dm.execute()
        result = dm.get_result(0, 0)

        print("Result of berm length: " + str(new_length))
        print("Reliability index: " + str(result.ReliabilityIndex))

        # Add result to dataframe
        df.loc[i] = [
            new_length,
            circle,
            dm.datastructure.geometries[0],
            result.ReliabilityIndex,
            output_file,
        ]

    return df


if __name__ == "__main__":
    # Define input file and water level range
    input_file = "examples\\dstability\\fragility_curve_berm\\fc.stix"
    z_start = 1
    z_end = 20
    z_step = 4

    fixed_berm_points = [
        Point(x=70, z=-10),
        Point(x=66, z=-6),
    ]

    varying_berm_points = [
        Point(x=66, z=-6),
        Point(x=70, z=-10),
    ]

    # Calculate fragility curve
    df = calculate_fragility_curve(
        input_file, fixed_berm_points, varying_berm_points, z_start, z_end, z_step
    )

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
    plt.clf()

    # Draw geometry and circle for each berm length
    for i in range(len(df)):
        layers = df.loc[i, "Layers"]
        x_min = 9999
        x_max = -9999
        z_min = 9999
        z_max = -9999

        for layer in layers.Layers:
            df_points = pd.DataFrame(columns=["X", "Z"])
            for point in layer.Points:
                df_points.loc[len(df_points)] = [point.X, point.Z]
            df_points.loc[len(df_points)] = [layer.Points[0].X, layer.Points[0].Z]

            plt.plot(df_points["X"], df_points["Z"], color="black")

            x_min = min(x_min, df_points["X"].min())
            x_max = max(x_max, df_points["X"].max())
            z_min = min(z_min, df_points["Z"].min())
            z_max = max(z_max, df_points["Z"].max())

        # zoom to extent of all layers
        plt.xlim(x_min - 5, x_max + 5)
        plt.ylim(z_min - 5, z_max + 5)

        circle = df.loc[i, "Circle"]
        plt.plot(circle.Center.X, circle.Center.Z, "o", color="black")
        plt.gca().add_patch(
            plt.Circle(
                (circle.Center.X, circle.Center.Z),
                circle.Radius,
                color="black",
                fill=False,
            )
        )

        plt.xlabel("X [m]")
        plt.ylabel("Z [m]")
        plt.title("Fragility curve")
        plt.grid()
        filename = "fragility_curve_layers_" + str(df.loc[i, "BermLength"]) + ".png"
        plt.savefig(output_folder / filename)
        plt.clf()
