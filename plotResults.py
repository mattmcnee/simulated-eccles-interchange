import argparse
from utils import plot_results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Plot results from trip data.")
    parser.add_argument('--savepath', type=str, required=True, help="Path to save the plot image")
    args = parser.parse_args()

    base_path = "data/trip_"

    plot_results(base_path, save_path=args.savepath)

    # plot_difference_from_csv("interchange_results.csv", "interchange-variation-1_results.csv", "imgC.png")

    # plot_table_from_csv("interchange_results.csv", "interchange-variation-1_results.csv")
