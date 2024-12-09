import random

def generate_vehicle_routes_sorted(output_file, num_vehicles):
    vehicles = []

    # Generate vehicle data
    for i in range(1, num_vehicles + 1):
        depart_time = round(random.uniform(1.0, 100.0), 2)  # Random depart time between 1.00 and 100.00 seconds
        route = "E2 E4" if random.choice([True, False]) else "E0 E3 E4"
        vehicles.append((i, depart_time, route))

    # Sort vehicles by departure time
    vehicles.sort(key=lambda x: x[1])

    # Write sorted vehicles to the XML file
    with open(output_file, 'w') as file:
        # Write the XML header
        file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        file.write('<routes xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://sumo.dlr.de/xsd/routes_file.xsd">\n')

        for vehicle_id, depart_time, route in vehicles:
            file.write(f'    <vehicle id="{vehicle_id}" depart="{depart_time}">\n')
            file.write(f'        <route edges="{route}"/>\n')
            file.write(f'    </vehicle>\n')

        # Close the routes tag
        file.write('</routes>\n')

# Generate the file with 100 sorted vehicles
generate_vehicle_routes_sorted("mergeTrafficCustom.rou.xml", 100)
