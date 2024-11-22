import os
from configGenerator import load_json
# data file paths

# generate data strcutures
    # convert json system conf file to dict


    # create or reinitialize program data => zones correspond with number of zones in conf file
        # each zone gets => {"Average Zone Moisture": 0 - 100, "Watering Watch Dog": object, "BD Watch Dog": object}
        # webpage => control logic {"ModeToggleFlag": 0 - 1, "WateringToggleFlags" (initilize array with zero for each zone): []}
        # periodic control logic => webpage {"networkConnectionFlag": , "Zones": {"WateringStatus": ,"Zone Moisture"}} => inhibiting and enable will be set from config file client recieves
        # requested control logic => webpage {"system logs": [], "24 hour samples": [], "available networks": []}
        # system wide variables include
            # networkConnectionFlag
            # UpdateConfigFlag
            # 


#-----------------------------Web Server--------------------------#
MAX_CONNECTIONS = 3
HTML_FILE_PATH = "HMI/Irrigation System UI final.html"
socketTimeout = 10  # Timeout in seconds

# Global list to store active clients and their ports
active_clients = []




#-----------------------------Networking---------------------------
# Network credentials
HOSTNAME = "mbesp32"
HOME_SSID = "BELL904"

APSSID='ESP32-AccessPoint'
APPASSWORD='123456789'




#-------------------------------SYSTEM data ---------------------------#
CONFIGFILEPATH = "./System Files/Data/irrigation_system_config.json"
BDSENSORLOG = "./System Files/Data/BDSensor.csv"
SMSENSORLOG = "./System Files/Data/SoilMoistureSensor.csv"
SYSLOGS = "./System Files/Data/SystemLogs.csv"
SMDATAPOINTS = 10
BDDATAPOINTS = 10
HARDWAREINPUTFREQUENCY = 4








SoilMoisturePins = [36, 39, 34]  # Replace with your ADC pin numbers
BodyDetectionPins = [18, 4]  # Replace with your digital pin numbers

solenoidControlPins = [27, 26, 25] 



SMSENSORS = len(SoilMoisturePins)
ZONES = SMSENSORS
BDSENSORS = len(BodyDetectionPins)


systemConfigParameters = load_json()
 # holds all the current config paramters for comparison

# data points




# Define the default zone structure
default_zone = {
    "SMaverage": None,
    "BDstate": "OFF",
    "WateringState": "OFF",
    "WateringWatch": None,
    "WateringCooldown": None, #or none for forcing user to clear
    "BDwatch": None,
    "tog-clr": 0
}

# Create a list of zones based on the number of zones (length of the pin array)
systemExecute = {
    "Mode": "man",  # Or "auto", depending on your mode that is set by server but defaults to manual on boot
    "WateringList": [], 
    "ntpConnectionNeeded": 0,
    "NewConfig": 0, #server sets and system logic unsets
    "Zones": [default_zone.copy() for _ in range(len(SoilMoisturePins))]  # Duplicate the zone for each pin
}






serverUpdates = []



def systemExecParamsInit():
    return



def systemExecuteInit():
    return





# initialize the data when imported by main
    # initialize server requests with number of zeros corresponding to config update, zone toggle,  
    
    # initialize system config parameters with json library




def replace_json_in_html(new_json):
    
    try:
        # Open the HTML file
        with open(CONFIGFILEPATH, 'r') as f:
            content = f.read()

        # Define the placeholder for the JSON content
        script_start = '<script id="persistentSystemData">'
        script_end = '</script>'
        
        # Find the position of the script block and the JSON structure
        start_index = content.find(script_start)
        end_index = content.find(script_end, start_index)

        if start_index == -1 or end_index == -1:
            raise ValueError("The script with id='persistentSystemData' was not found in the HTML file.")

        # The new JSON data will replace everything between the <script> tags
        new_script = f"{script_start}\njsonData = `{new_json}`\n{script_end}"

        # Replace the old JSON structure with the new one
        updated_content = content[:start_index] + new_script + content[end_index + len(script_end):]

        # Write the modified content back to the file
        with open(CONFIGFILEPATH, 'w') as f:
            f.write(updated_content)
        print("HTML file updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")




replace_json_in_html(systemConfigParameters)