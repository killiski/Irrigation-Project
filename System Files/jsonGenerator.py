import os
import json

def create_irrigation_system_config(num_zones, file_path="irrigation_system_config.json"):
    # Check if the file exists
    if os.path.exists(file_path):
        print("File already exists.")
        return

    # Initialize the system data structure
    system_data = {
        "System Data": {
            "Configured Zones": num_zones,
            "System Name": "myIrrigation_System",
            "System Disable": True,
            "Mode": "Manual",
            "Simultaneous Watering": False,
            "Sample Rate": 1,
            "log pointer": 40,
            "24hr sample pointer": 248,
            "Time": {
                "LastNTP_Connection": "",
                "Start SZN": 0,
                "End SZN": 0
            }
        },
        "Zones": []
    }

    # Create the zones with duplicated structure and modify sensor attachments
    for i in range(num_zones):
        zone_data = {
            "MoistureManagement": {
                "Attached Soil Sensors": [f"Sensor{i + 1}"],
                "Manual Water Time": 20,
                "Watering Timeout Minutes": 30,
                "Timeout Cooldown": 20,
                "Watering Disabled": False,
                "Control Limits": {
                    "UCL": 25,
                    "LCL": 20
                }
            },
            "BD Inhibiting": {
                "Attached BD Sensors": [ ],
                "BD enable": True,
                "BD alarm alert": 30
            },
            "Schedule": {
                "On": True,
                "Times": ["00:00", "24:00"],
                "Enabled": False
            }
        }

        # Update the sensor names to match the zone index
        system_data["Zones"].append(zone_data)

    # Write the data to a JSON file
    with open(file_path, 'w') as f:
        json.dump(system_data, f, indent=4)

    print(f"Config file created at {file_path}.")





def load_json(file_path="irrigation_system_config.json"):
    with open(file_path, 'r') as f:
        data = json.load(f)  # Load JSON as a Python dictionary
    return data

# Example usage
#create_irrigation_system_config(2)

#myData = load_json()
#print(myData["Zones"][0]["MoistureManagement"]["Control Limits"]["LCL"])