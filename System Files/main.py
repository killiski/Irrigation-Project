import time
import os
import sys
import select
import _thread
from ControlLogic.Inputs import runInputCycle
from HMI.networkMan import setup_access_point
from HMI.webServer import web_server_thread

from Data.globalData import systemExecute, systemConfigParameters, replace_json_in_html
#replace_json_in_html(systemConfigParameters)





# we will use a circular buffer for logs and 24hour samples


# Main function to initiate the connection and access point setup
if __name__ == '__main__':
    setup_access_point() #so solid
    #_thread.start_new_thread(ControlLogic.Inputs.read_sensors, ())
    #initilize system data
    #initilize web page thread
    #asyncio.run(webServer.start_server())
    #webServer.start_server()
    runInputCycle()
    #time.sleep(10) #let sensor arrays fill can comment out for testing
   
    _thread.start_new_thread(web_server_thread, ())
    



    
    while True:
        # run sampling and control
        print("the date is: " + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]))
        #print(f"System Executing Data: {systemExecute}")
        


        outputCharacters = f"""\n\n------------------System Executing Data:
Mode: {systemExecute["Mode"]}
Watering List: {systemExecute["WateringList"]}
New Configuration: {systemExecute["NewConfig"]}
NTP connection flag: {systemExecute["ntpConnectionNeeded"]}
Zone Data: {systemExecute["Zones"]}\n\n
"""
        print(outputCharacters)
        #pass
        #webpage.webpage_deploy()
        print("Program Running")
        time.sleep(4)

        print("\b" * len(outputCharacters))
    