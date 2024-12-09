import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from collections import defaultdict

# Define the path to the XML file
file_path = "data/trip_info.xml"

# Parse the XML file
tree = ET.parse(file_path)
root = tree.getroot()

# Dictionary to store departure times and durations grouped by base route ID
route_data = defaultdict(lambda: {"departures": [], "durations": []})

# Process each tripinfo entry
for tripinfo in root.findall('tripinfo'):
    trip_id = tripinfo.get('id')
    departure = float(tripinfo.get('depart'))
    duration = float(tripinfo.get('duration'))

    # Extract the base route ID (disregard the number after the last underscore)
    base_id = "_".join(trip_id.split('_')[:-1])

    # Append data to the corresponding route
    route_data[base_id]["departures"].append(departure)
    route_data[base_id]["durations"].append(duration)

# Plot the data
plt.figure(figsize=(12, 8))
colors = plt.cm.tab10.colors  # Use a colormap for consistent coloring
for idx, (route, data) in enumerate(route_data.items()):
    color = colors[idx % len(colors)]  # Cycle through colors if there are more routes than colors
    plt.scatter(data["departures"], data["durations"], label=route, color=color, alpha=0.7)

# Customize the plot
plt.title("Departure Time vs Trip Duration by Route", fontsize=16)
plt.xlabel("Departure Time (seconds)", fontsize=14)
plt.ylabel("Trip Duration (seconds)", fontsize=14)
plt.legend(title="Routes", fontsize=10, loc="best")
plt.grid(True)
plt.tight_layout()

# Show the plot
plt.show()
