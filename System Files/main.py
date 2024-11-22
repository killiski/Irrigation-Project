import time
import sys
import select
import _thread
from ControlLogic.Inputs import runInputCycle
from HMI.networkMan import setup_access_point
from HMI.webServer import web_server_thread

from Data.globalData import systemExecute






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
        print(f"System Executing Data: {systemExecute}")
        #pass
        #webpage.webpage_deploy()
        print("Program Running")
        time.sleep(10)
    