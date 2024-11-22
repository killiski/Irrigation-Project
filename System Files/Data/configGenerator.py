import os
import json


filePath = "./System Files/Data/irrigation_system_config.json"





def create_irrigation_system_config(num_sols, num_BD, file_path=filePath):
    # Check if the file exists
    # print(os.getcwd())
    print(f"my file path is {file_path}")

    if os.path.exists(file_path):
        print("File already exists.")
        return

    # Initialize the system data structure
    system_data = {
        "System Data": {
            "totalSolenoids": num_sols,
            "System Name": "myIrrigation_System",
            "System Disable": True,
            "Simultaneous Watering": 1,
            "Hourly Samples": 1,
            "Sensors": {
                "Soil Moiture": num_sols,
                "BD Detection": num_BD
            },
            "Time": {
                "LastNTP_Connection": "",
                "Start SZN": 0,
                "End SZN": 365
            }
        },
        "Zones": []
    }

    # Create the zones with duplicated structure and modify sensor attachments
    for i in range(num_sols):
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
                "BD Enable": True,
                "BD Alarm Alert": 30
            },
            "Schedule": {
                "On Time": "00:00",
                "Off Time": "23:59",
                "Enabled": False
            }
        }

        # Update the sensor names to match the zone index
        #zone_data["MoistureManagment"]["Attached Soil Sensors"] = [f"Sensor{i + 1}" for i in range(num_zones)]
        system_data["Zones"].append(zone_data)

    # Write the data to a JSON file
    with open(file_path, 'w') as f:
        json.dump(system_data, f, indent=4)

    print(f"Config file created at {file_path}.")





def load_json(file_path=filePath):
    with open(file_path, 'r') as f:
        data = json.load(f)  # Load JSON as a Python dictionary
    return data


def replace_json( newJson, file_path=filePath):
    with open(file_path, 'w') as f:
        json.dump(newJson, f, indent=4)
    return newJson



# Example usage
#create_irrigation_system_config(3, 2, filePath)

#myData = load_json()
#print(myData["Zones"][0]["MoistureManagement"]["Control Limits"]["LCL"])

