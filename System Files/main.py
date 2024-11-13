import time
import sys
import select
import _thread
from HMI import networkMan, webServer
from Data import globalData
import uasyncio as asyncio






# we will use a circular buffer for logs and 24hour samples


# Main function to initiate the connection and access point setup
if __name__ == '__main__':
    networkMan.setup_access_point() #so solid
    #initilize system data
    #initilize web page thread
    #asyncio.run(webServer.start_server())
    #webServer.start_server()
    _thread.start_new_thread(webServer.web_server_thread, ())
    




    while True:
        # run sampling and control
        print("the date is: " + str(time.localtime()[0]) + "-" + str(time.localtime()[1]) + "-" + str(time.localtime()[2]))
        #pass
        #webpage.webpage_deploy()
        print("Program Running")
        time.sleep(10)