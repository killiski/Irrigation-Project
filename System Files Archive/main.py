import networkMan
import time
import sys
import select
import _thread
import webpage


systemParamters = {
    "sampleFrequency": 2,
    "24Hsamples": 48,
    "WPA2ENT": False,
}

solenoidRelays = 3
soilMoistureSensors = solenoidRelays
BDSensors= 2





class MoistureSensor:
  def __init__(self, pin):
    self.pin = pin



class Logs:
   def __init__(self, pin):
    self.pin = pin


# we will use a circular buffer for logs and 24hour samples


# Main function to initiate the connection and access point setup
if __name__ == '__main__':
    networkMan.setup_access_point() #so solid
    #initilize system data
    #initilize web page thread
    





    
    _thread.start_new_thread(webpage.webpage_deploy, ())

    while True:
        # run sampling and control
        print("the date is: " + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]))
        #pass
        #webpage.webpage_deploy()
        print("Program Running")
        time.sleep(10)