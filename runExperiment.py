import os
import argparse
from utils import generate_random_vehicles, create_config_file, run_sumo_simulation, plot_results, save_results_to_csv, plot_results_from_csv, plot_difference_from_csv, plot_table_from_csv

def main():
    parser = argparse.ArgumentParser(description="Generate random vehicles for simulations")
    parser.add_argument(
        '--net-file',
        type=str,
        default='interchange.net.xml',
        help='Path to the net file (default: interchange.net.xml)'
    )
    args = parser.parse_args()

    # Print the selected net-file for confirmation
    print(f"Using net file: {args.net_file}")

    # Directory to store the output files
    output_dir = 'sims'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Loop through the range of vehicle counts (100 to 1000, with step 100)
    for num_vehicles in range(100, 1100, 100):
        # Set the output file path based on the number of vehicles
        output_file = os.path.join(output_dir, f'density_{num_vehicles}.xml')

        # Call the imported function to generate random vehicles
        generate_random_vehicles(output_file, num_vehicles)

        # Create the configuration file for the simulation
        config_file = create_config_file(num_vehicles, args.net_file, output_dir)

        run_sumo_simulation(config_file) 

    # of the format: defaultdict(lambda: defaultdict(lambda: {"durations": [], "density": []}))
    route_data = plot_results("data/trip_")

    csv_filename = f"{args.net_file.split('.')[0]}_results.csv"
    save_results_to_csv(route_data, csv_filename)
    print(f"Results saved to {csv_filename}")




if __name__ == '__main__':
    main()

    # plot_difference_from_csv("interchange_results.csv", "interchange-variation-1_results.csv", "imgC.png")

    # plot_table_from_csv("interchange_results.csv", "interchange-variation-1_results.csv")