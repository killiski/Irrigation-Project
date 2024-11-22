from Data.globalData import SoilMoisturePins, BodyDetectionPins, systemExecute, systemConfigParameters
import _thread
import time
from machine import Pin, ADC
import re

# Configure ADC channels
# Initialize the pins
SMchannels = []
for pin in SoilMoisturePins:
    adc = ADC(Pin(pin))                # Initialize ADC on the specified pin
    adc.atten(ADC.ATTN_11DB)           # Set attenuation for 0-3.3V range
    adc.width(ADC.WIDTH_12BIT)         # Use 12-bit resolution (0-4095)
    SMchannels.append(adc)

# Configure Body Detection (Digital) Pins
BDchannels = []
for pin in BodyDetectionPins:
    bd_pin = Pin(pin, Pin.IN, Pin.PULL_UP)  # Use PULL_UP or PULL_DOWN as needed
    BDchannels.append(bd_pin)



# Constants
DATAPOINTS = 10
READPERIOD = 0.5  # in seconds

# Constants for counting before averaging
SM_AVERAGE_INTERVAL = 5  # Soil moisture average after 5 readings
BD_AVERAGE_INTERVAL = 2  # Body detection average after 5 readings

# Constant to control body detection read frequency (how many cycles of READFREQUENCY between BD reads)
BD_READ_FREQUENCY_MULTIPLIER = 1  # Body detection sensor is read every 2 READFREQUENCY cycles


#we need to create a function to convert adc value to percentage ------------------------------------------------

systemExecute["Zones"][0]["SMaverage"]
systemExecute["Zones"][0]["BDstate"]
systemConfigParameters # check for attached sensors???


# Lists to hold recent readings for each sensor

SMdatapoints = [[] for _ in range(len(SMchannels))]  # List of lists for soil moisture sensors
BDdatapoints = [[] for _ in range(len(BDchannels))]  # List of lists for body detection sensors

# Counters to track every N readings for each sensor (initialized to 0)
sm_counter = 0
bd_counter = 0

# Cycle counter to track how many cycles have passed (for controlling BD read frequency)
cycle_counter = 0


def read_sensors():
    global SMdatapoints, BDdatapoints, SMchannels, BDchannels, sm_counter, bd_counter, cycle_counter

    while True:
        # Increment cycle counter
        cycle_counter += 1
        
        #print(SMchannels)
        # Read soil moisture sensors (always)
        for i in range(len(SMchannels)):
            sm_counter += 1
            SMdatapoints[i].append(SMchannels[i].read())
            if len(SMdatapoints[i]) > DATAPOINTS:
                SMdatapoints[i].pop(0)

        # Body detection is read based on the multiplier (every x cycles of READFREQUENCY)
        if cycle_counter % BD_READ_FREQUENCY_MULTIPLIER == 0:  # Read body detection every x cycles
            bd_counter += 1
            for i in range(len(BDchannels)):
                BDdatapoints[i].append(BDchannels[i].value())
                if len(BDdatapoints[i]) > DATAPOINTS:
                    BDdatapoints[i].pop(0)


        # Track and calculate averages for soil moisture every SM_AVERAGE_INTERVAL readings
        
        # need to update so that it reads all the attached sensor and stores their average
        if sm_counter >= SM_AVERAGE_INTERVAL:
            for zone in range(systemConfigParameters["System Data"]["totalSolenoids"]):  
                systemExecute["Zones"][zone]["SMaverage"] = []  
                for sensor in systemConfigParameters["Zones"][zone]["MoistureManagement"]["Attached Soil Sensors"]:
                    #print(sum(SMdatapoints[int(re.search(r'\d+', sensor))]) / len(SMdatapoints[int(re.search(r'\d+', sensor))]))
                    sensNum = int(re.search(r'\d+', sensor).group(0)) - 1
                    
                    systemExecute["Zones"][zone]["SMaverage"].append(sum(SMdatapoints[sensNum]) / len(SMdatapoints[sensNum]))
            sm_counter = 0


        # Track and calculate averages for body detection every BD_AVERAGE_INTERVAL readings
        
        # need to update so that it reads all the attached sensor and stores their average
        if bd_counter >= BD_AVERAGE_INTERVAL:
            for zone in range(systemConfigParameters["System Data"]["totalSolenoids"]):
                
                systemExecute["Zones"][zone]["BDstate"] = []
                
                for sensor in systemConfigParameters["Zones"][zone]["BD Inhibiting"]["Attached BD Sensors"]:
                    
                    sensNum = int(re.search(r'\d+', sensor).group(0)) - 1

                    systemExecute["Zones"][zone]["BDstate"].append(round(sum(BDdatapoints[sensNum]) / len(BDdatapoints[sensNum])))
                    #if on and bd timer not timing set BD timer, if off reset bd timer timing
            bd_counter = 0
        
        #print(SMchannels)
        #print(BDchannels)
        #print(f"SM datapoints: {SMdatapoints}") => use to check soil moisture adc
        #print(f"BD datapoints: {BDdatapoints}") => use to check bd digital inputss
        time.sleep(READPERIOD)


def runInputCycle():
    _thread.start_new_thread(read_sensors, ())
    

# Start the sensor reading thread
