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
CONFIGFILEPATH = "Data/irrigation_system_config.json"
BDSENSORLOG = "System Files/Data/BDSensor.csv"
SMSENSORLOG = "System Files/Data/SoilMoistureSensor.csv"
SYSLOGS = "System Files/Data/SystemLogs.csv"
SMDATAPOINTS = 10
BDDATAPOINTS = 10
HARDWAREINPUTFREQUENCY = 4








SoilMoisturePins = [32, 33, 34]  # Replace with your ADC pin numbers
BodyDetectionPins = [25, 26]  # Replace with your digital pin numbers

solenoidControlPins = [12, 13, 14] 



SMSENSORS = len(SoilMoisturePins)
ZONES = SMSENSORS
BDSENSORS = len(BodyDetectionPins)


systemConfigParameters = {

} # holds all the current config paramters for comparison

# data points




# Define the default zone structure
default_zone = {
    "SMaverage": None,
    "BDstate": "OFF",
    "WateringState": "OFF",
    "WateringWatch": "watch dog here",
    "BDwatch": "watch dog here"
}

# Create a list of zones based on the number of zones (length of the pin array)
systemExecute = {
    "Mode": "man",  # Or "auto", depending on your mode
    "Zones": [default_zone.copy() for _ in range(len(SoilMoisturePins))]  # Duplicate the zone for each pin
}

"""
systemExecute = {
    "Mode": "man", #or "man"
    "Zones": [
        {
            "SMaverage": null,
            "BDstate": "OFF",
            "WateringState": "OFF",
            "WateringWatch": "watch dog here",
            "BDwatch": "watch dog here"
        }, #make one for each zone
        {
            "SMaverage": 20,
            "BDstate": "ON",
            "WateringState": "OFF",
            "WateringWatch": "watch dog here",
            "BDwatch": "watch dog here"
        }, #make one for each zone
        {
            "SMaverage": 20,
            "BDstate": "ON",
            "WateringState": "OFF",
            "WateringWatch": "watch dog here",
            "BDwatch": "watch dog here"
        }, #make one for each zone
    ]
}
"""





serverRequests = [] #[(modeToggle), (zone1Toggle), (zone2Toggle), ...]
serverUpdates = []



def systemExecParamsInit():
    return



def systemExecuteInit():
    return





# initialize the data when imported by main
    # initialize server requests with number of zeros corresponding to config update, zone toggle,  
    
    # initialize system config parameters with json library