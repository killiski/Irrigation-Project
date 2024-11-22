import os
#import configGenerator
import json
from ControlLogic.WatchDog import WatchdogTimer
from Data.configGenerator import create_irrigation_system_config
import machine
from time import sleep

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

def replace_json( newJson, file_path):
    with open(file_path, 'w') as f:
        json.dump(newJson, f, indent=4)
    return newJson

def load_json(file_path):
    print(os.listdir())

    with open(file_path, 'r') as f:
        data = json.load(f)  # Load JSON as a Python dictionary
    return data



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
CONFIGFILEPATH = "/Data/irrigation_system_config.json"
BDSENSORLOG = "Data/BDSensor.csv"
SMSENSORLOG = "Data/SoilMoistureSensor.csv"
SYSLOGS = "Data/SystemLogs.csv"
SMDATAPOINTS = 10
BDDATAPOINTS = 10
HARDWAREINPUTFREQUENCY = 4







#SoilMoisturePins = [36, 39]
SoilMoisturePins = [36, 39, 34]  # Replace with your ADC pin numbers
BodyDetectionPins = [18, 4]  # Replace with your digital pin numbers

solenoidControlPins = [27, 26, 25] 
#solenoidControlPins = [27, 26]

if len(SoilMoisturePins) < len(solenoidControlPins):
    led = machine.Pin(2, machine.Pin.OUT)
    while True:
        print("number of moisture sensors must be greater than solenoids")
        led.value(not led.value())
        sleep(5)
# trap in forever while loop with print saying SMsensors must match number of slenoids


SMSENSORS = len(SoilMoisturePins)
ZONES = SMSENSORS
BDSENSORS = len(BodyDetectionPins)


systemConfigParameters = load_json(CONFIGFILEPATH)
 # holds all the current config paramters for comparison

# data points

if len(solenoidControlPins) != systemConfigParameters["System Data"]["totalSolenoids"]:
    # reconfigure and reboot
    create_irrigation_system_config(len(solenoidControlPins), len(BodyDetectionPins), file_path=CONFIGFILEPATH)
    machine.reset()




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
    "Mode": "Manual",  # Or "auto", depending on your mode that is set by server but defaults to manual on boot
    "WateringList": [], 
    "ntpConnectionNeeded": 0,
    "NewConfig": 0, #server sets and system logic unsets
    "Zones": [default_zone.copy() for _ in range(len(solenoidControlPins))]  # Duplicate the zone for each pin
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
        # Define the placeholder for the JSON content
        script_start = '<script id="persistentSystemData">'
        script_end = '</script>'
        
        # Prepare the new script content
        new_script = f"{script_start}\njsonData = `{json.dumps(new_json)}`\n\npersistentSystemData = JSON.parse(jsonData){script_end}"

        # Temporary file path
        temp_file_path = HTML_FILE_PATH + ".tmp"

        # Open the original file for reading and a temporary file for writing
        with open(HTML_FILE_PATH, 'r') as f:
            with open(temp_file_path, 'w') as temp_f:
                inside_target = False
                for line in f:
                    if script_start in line:
                        # Write the new script block and skip lines until the end of the target block
                        temp_f.write(new_script + '\n')
                        inside_target = True
                    elif script_end in line and inside_target:
                        # Stop skipping lines after the end of the target block
                        inside_target = False
                    elif not inside_target:
                        # Copy lines as is
                        temp_f.write(line)

        # Remove the original file
        os.remove(HTML_FILE_PATH)

        # Rename the temporary file to the original file
        os.rename(temp_file_path, HTML_FILE_PATH)
        print("HTML file updated successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")






replace_json_in_html(systemConfigParameters)