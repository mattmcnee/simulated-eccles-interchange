import random
import os
import subprocess
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from collections import defaultdict
import numpy as np

def generate_random_vehicles(output_file, num_vehicles, duration=100):
    # Dictionary of routes with start node options and density attribute
    routes = {
        "m602-m60": {
            "start_nodes": ["E3", "E4", "E5"],
            "route": (
                "145868728 145876496 611356040 145876499 "
                "158470844#1-AddedOnRampEdge 158470844#1 145852821 145852821.67 "
                "145852815 145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 1
        },
        "m60-north": {
            "start_nodes": ["E9 E1", "E10 E1", "E11 E0", "E12 E0", "E13 E2", "E14 E2"],
            "route": (
                "146417963 146417963-AddedOffRampEdge 158470844#0 "
                "158470844#1-AddedOnRampEdge 158470844#1 145852821 145852821.67 "
                "145852815 145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 2
        },
        "m60-worsley": {
            "start_nodes": ["E9 E1", "E10 E1", "E11 E0", "E12 E0", "E13 E2", "E14 E2"],
            "route": (
                "146417963 146417963-AddedOffRampEdge 158470844#0 "
                "158470844#1-AddedOnRampEdge 158470844#1 145852821 145852821.67 "
                "145852815 145852815-AddedOffRampEdge 145852856"
            ),
            "density": 0.5
        },
        "m62-m60-a": {
            "start_nodes": ["E6", "E7", "E8"],
            "route": (
                "46372495 111538044 296702213 296702213.417 145852821 145852821.67 "
                "145852815 145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 0.5
        },
        "m62-m60-b": {
            "start_nodes": ["E6", "E7", "E8"],
            "route": (
                "46372495 111538044 296702213 E15 145852821.67 "
                "145852815 145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 0.5
        },
    }

    # Generate vehicle data
    vehicles = []
    for i in range(1, num_vehicles + 1):
        # Random depart time between 1.00 and "duration" seconds
        depart_time = round(random.uniform(1.0, duration), 2)
        
        # Select a route key based on the density
        route_key = random.choices(
            list(routes.keys()), 
            weights=[routes[key]["density"] for key in routes], 
            k=1
        )[0]
        
        # Add a random start node to the route
        start_node = random.choice(routes[route_key]["start_nodes"])
        route = routes[route_key]["route"]
        full_route = f"{start_node} {route}"
        
        # Generate vehicle ID with route key and index
        vehicle_id = f"{route_key}_{i}"
        
        # Append the vehicle data
        vehicles.append((vehicle_id, depart_time, full_route))

    # Sort vehicles by departure time
    vehicles.sort(key=lambda x: x[1])

    # Write sorted vehicles to the XML file
    with open(output_file, 'w') as file:
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')

        for vehicle_id, depart_time, route in vehicles:
            file.write(f'    <vehicle id="{vehicle_id}" depart="{depart_time}">\n')
            file.write(f'        <route edges="{route}"/>\n')
            file.write(f'    </vehicle>\n')

        file.write('</routes>\n')

# generate_random_vehicles("interchangeTrafficCustom.rou.xml", 1200, 200)

def create_config_file(num_vehicles, net_file, output_dir):
    # Generate the config file path
    config_file = os.path.join(output_dir, f'config_{num_vehicles}.cfg')

    # Define paths for the route file and tripinfo output file
    route_file = os.path.join(output_dir, f'density_{num_vehicles}.xml')
    tripinfo_file = os.path.join('data', f'trip_{num_vehicles}.xml')

    # Write the configuration to the file
    with open(config_file, 'w') as f:
        f.write(f"""<configuration>
    <input>
        <net-file value="../{net_file}" />
        <route-files value="../{route_file}" />
    </input>
    <time>
        <begin value="0"/>
        <end value="1000"/>
    </time>
    <output>
        <tripinfo-output value="../{tripinfo_file}" />
    </output>
</configuration>
""")
        
    return config_file
        
def run_sumo_simulation(config_file):
    """
    Runs the SUMO simulation using the given config file.
    """
    # Execute the SUMO simulation using the provided .cfg file
    command = ['sumo', '-c', config_file, '--step-length', '0.1']
    
    try:
        subprocess.run(command, check=True)
        print(f"Simulation completed with config: {config_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during simulation with config: {config_file}")
        print(e)

def plot_results(base_path, save_path=None):
    # Create a dictionary to store data for each route and its trip durations per density
    route_data = defaultdict(lambda: defaultdict(lambda: {"durations": [], "density": []}))

    # Loop over densities from 100 to 1000 in steps of 100
    for density in range(100, 1001, 100):
        file_path = f"{base_path}{density}.xml"

        print(f"Processing file: {file_path}")
        
        # Parse the XML file
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Error parsing {file_path}: {e}")
            continue

        # Process each tripinfo entry
        for tripinfo in root.findall('tripinfo'):
            trip_id = tripinfo.get('id')
            duration = float(tripinfo.get('duration'))

            # Extract the base route ID (disregard the number after the last underscore)
            base_id = "_".join(trip_id.split('_')[:-1])
            
            # Store the duration and density information
            route_data[base_id][density]["durations"].append(duration)
            route_data[base_id][density]["density"].append(density)

    # Calculate the average durations for each route and density
    avg_durations = defaultdict(list)

    # Loop over each route and compute the average duration for each density
    for route, densities in route_data.items():
        for density, data in densities.items():
            avg_duration = np.mean(data["durations"])
            avg_durations[route].append((density, avg_duration))

    # Plot the data
    plt.figure(figsize=(12, 8))

    # Loop through each route and plot the average duration against density
    colors = plt.cm.tab10.colors  # Use a colormap for consistent coloring
    for idx, (route, data) in enumerate(avg_durations.items()):
        density_values, avg_duration_values = zip(*data)
        plt.plot(density_values, avg_duration_values, label=f'Route {route}', color=colors[idx % len(colors)], marker='o')

    # Customize the plot
    plt.title("Average Trip Duration vs Traffic Density by Route", fontsize=16)
    plt.xlabel("Traffic Density", fontsize=14)
    plt.ylabel("Average Trip Duration (seconds)", fontsize=14)
    plt.legend(title="Routes", fontsize=10, loc="best")
    plt.grid(True)
    plt.tight_layout()

    # Save the plot as a file if a save path is provided
    if save_path:
        plt.savefig(save_path)
        print(f"Plot saved to: {save_path}")

    # Show the plot
    plt.show()
