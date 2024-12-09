import random

def generate_random_vehicles(output_file, num_vehicles, duration = 100):

    # Dictionary of routes with start node options and density attribute
    routes = {
        "m602-m60": {
            "start_nodes": ["E3", "E4", "E5"],
            "route": (
                "145868728 145876496 611356040 145876499 "
                "158470844#1-AddedOnRampEdge 158470844#1 145852821 "
                "145852815 145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 1
        },
        "m60-north": {
            "start_nodes": ["E9 E1", "E10 E1", "E11 E0", "E12 E0", "E13 E2", "E14 E2"],
            "route": (
                "146417963 146417963-AddedOffRampEdge 158470844#0 "
                "158470844#1-AddedOnRampEdge 158470844#1 145852821 "
                "145852815 145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 2
        },
        "m60-worsley": {
            "start_nodes": ["E9 E1", "E10 E1", "E11 E0", "E12 E0", "E13 E2", "E14 E2"],
            "route": (
                "146417963 146417963-AddedOffRampEdge 158470844#0 "
                "158470844#1-AddedOnRampEdge 158470844#1 145852821 "
                "145852815 145852815-AddedOffRampEdge 145852856"
            ),
            "density": 0.5
        },
        "m62-m60": {
            "start_nodes": ["E6", "E7", "E8"],
            "route": (
                "46372495 111538044 296702213 145852821 145852815 "
                "145852815-AddedOffRampEdge 1066957350 145852800#1"
            ),
            "density": 1
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
        full_route = f"{start_node} " + route
        
        # Append the vehicle data
        vehicles.append((i, depart_time, full_route))

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

generate_random_vehicles("interchangeTrafficCustom.rou.xml", 1200, 200)
