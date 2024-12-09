import os
import argparse
from generateVehicles import generate_random_vehicles  # Import the function

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

if __name__ == '__main__':
    main()
