from machine import Pin
from Data.globalData import solenoidControlPins, systemExecute

# Initialize solenoid control pins as digital outputs
solenoid_pins = [Pin(pin, Pin.OUT) for pin in solenoidControlPins]
PINACTIVE = "ON"


# Function to clear (set LOW) all solenoid control pins
def clear_solenoids():
    for pin in solenoid_pins:
        pin.value(0)  # Set pin to LOW (inactive)

# Function to check the watering status in each zone and activate the corresponding pin
def update_solenoids():
    # Iterate through the 'zones' list in globalData
    for i, zone in enumerate(systemExecute["Zones"]):
        watering_status = zone["WateringState"]  # Get the watering status

        # Find the index of the zone in the solenoid pins list
        # Assuming zones and solenoid_pins are aligned by index

        # Check if watering status is "Active"
        if watering_status == "Active":
            solenoid_pins[i].value(1)  # Set the corresponding pin HIGH
        else:
            solenoid_pins[i].value(0)  # Set the pin LOW if status is not "Active"
    
# Example usage
#clear_solenoids()  # Clear (set LOW) all solenoid control pins
#update_solenoids()  # Check the watering status and set the corresponding pins