from Data import globalData
import _thread
import time
from machine import Pin, ADC

# Configure ADC channels
# Initialize the pins
SMchannels = [ADC(Pin(pin)) for pin in globalData.SoilMoisturePins]  # Create ADC objects
BDchannels = [Pin(pin, Pin.IN) for pin in globalData.BodyDetectionPins]

# Constants
DATAPOINTS = 10
READPERIOD = 2  # in seconds

# Constants for counting before averaging
SM_AVERAGE_INTERVAL = 5  # Soil moisture average after 5 readings
BD_AVERAGE_INTERVAL = 5  # Body detection average after 5 readings

# Constant to control body detection read frequency (how many cycles of READFREQUENCY between BD reads)
BD_READ_FREQUENCY_MULTIPLIER = 2  # Body detection sensor is read every 2 READFREQUENCY cycles


#we need to create a function to convert adc value to percentage ------------------------------------------------

globalData.systemExecute["Zones"][0]["SMaverage"]
globalData.systemExecute["Zones"][0]["BDstate"]
globalData.systemConfigParameters # check for attached sensors???


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
            for i in range(len(BDchannels)):
                BDdatapoints[i].append(BDchannels[i].value())
                if len(BDdatapoints[i]) > DATAPOINTS:
                    BDdatapoints[i].pop(0)


        # Track and calculate averages for soil moisture every SM_AVERAGE_INTERVAL readings
        if sm_counter >= SM_AVERAGE_INTERVAL:
            for i in range(len(SMchannels)):
                globalData.systemExecute["Zones"][i]["SMaverage"] = sum(SMdatapoints[i]) / len(SMdatapoints[i])
            sm_counter = 0


        # Track and calculate averages for body detection every BD_AVERAGE_INTERVAL readings
        if bd_counter >= BD_AVERAGE_INTERVAL:
            for i in range(len(BDchannels)):
                if round(sum(SMdatapoints[i]) / len(SMdatapoints[i])) == 1:
                    globalData.systemExecute["Zones"][i]["BDstate"] = "ON" 
                else:
                    globalData.systemExecute["Zones"][i]["BDstate"] = "OFF"
                #if on and bd timer not timing set BD timer, if off reset bd timer timing
            bd_counter = 0
        
        #print(f"SM datapoints: {SMdatapoints}")
        #print(f"BD datapoints: {BDdatapoints}")
        time.sleep(READPERIOD)


def runInputCycle():
    _thread.start_new_thread(read_sensors, ())
    

# Start the sensor reading thread