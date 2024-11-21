import time
import sys
import select
import _thread
import ControlLogic.Inputs
from HMI import networkMan, webServer
from Data import globalData
import ControlLogic






# we will use a circular buffer for logs and 24hour samples


# Main function to initiate the connection and access point setup
if __name__ == '__main__':
    networkMan.setup_access_point() #so solid
    #_thread.start_new_thread(ControlLogic.Inputs.read_sensors, ())
    #initilize system data
    #initilize web page thread
    #asyncio.run(webServer.start_server())
    #webServer.start_server()
    ControlLogic.Inputs.runInputCycle()
    #time.sleep(10) #let sensor arrays fill can comment out for testing
   
    _thread.start_new_thread(webServer.web_server_thread, ())
    



    
    while True:
        # run sampling and control
        print("the date is: " + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]))
        print(f"System Executing Data: {globalData.systemExecute}")
        #pass
        #webpage.webpage_deploy()
        print("Program Running")
        time.sleep(10)
    