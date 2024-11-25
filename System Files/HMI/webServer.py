# webserver

#initialize data
    #client array
    #network connection flag


# webserver client deploying => thread




# client handling => thread
    # wait for revc() bytes, if conf update flag then run client update code which adds all the clients to a list and forces them to update

    # HTTP requests
        #get available networks => lock and make all client requesting to wait
        #connect to network => lock and make clients pass if in use

        #fetch monitoring values (wifi connected, mode, [zone watering flags], )
        #submit monitoring values (mode toggle, [zone watering flags]) => global variable
        #fetch logs
        #fetch 24 hour samples


        #Update Config file => get new config file, insert into html file, redirect clients to "send html" => locking
            #do i just remake the conf file or pop/append the zone list depending on the zones configured??
        #send HTML => in chunks of 10kb


import socket
import json
import _thread
import time
import os
from Data.globalData import systemConfigParameters, CONFIGFILEPATH

#MAX_CONNECTIONS = 3
HTML_FILE_PATH = "HMI/Irrigation System UI final.html"
socketTimeout = 10  # Timeout in seconds





def send_html_file_in_chunks(conn, file_path, chunk_size=256): 
    """
    Send HTML content from a file stored on disk in chunks.
    """
    try:
        file_size = os.stat(file_path)[6]
        # Send the initial response headers with chunked transfer encoding
        conn.send(b"HTTP/1.1 200 OK\r\n")
        conn.send(b"Content-Type: text/html; charset=UTF-8\r\n")  # Added charset
        conn.send(b"Transfer-Encoding: chunked\r\n")
        #conn.send(b"Cache-Control: no-store\r\n")  # Added caching headers
        #conn.send(b"Access-Control-Allow-Origin: *\r\n")
        #conn.send(b"Pragma: no-cache\r\n")
        #conn.send(b"Expires: 0\r\n")  # Added expiry headers
        conn.send(b"\r\n")


        # Open the file and send it in chunks
        with open(file_path, 'rb') as file:
            while (chunk := file.read(chunk_size)):
                # Send the size of the chunk in hexadecimal
                conn.send(f"{len(chunk):X}\r\n".encode())
                # Send the chunk data itself
                conn.send(chunk)
                # Send a new line to end the chunk
                conn.send(b"\r\n")

        # Send the last zero-length chunk to indicate the end
        conn.send(b"0\r\n\r\n")
    except:
        return -1


  




def handle_client(conn, IpAddr, port):
    #global active_clients
    #print(f"New client connected: {IpAddr}:{port}")
    
    conn.settimeout(socketTimeout)
    #conn.setblocking(False)
        
    
    try:
        data = conn.recv(4096).decode("utf-8")
        print("the data: ", data) #.decode("utf-8")
        
        
        if "GET / " in data:
            send_html_file_in_chunks(conn, HTML_FILE_PATH)
        elif "POST /configUpdate" in data:
            print("\n\nthe data: ", data.split("\r\n\r\n")[1])
            configUpdate(data.split("\r\n\r\n")[1])
            #call config update function
            pass
        elif "POST /solToggle" in data:
            #call config update function
            pass
        elif "POST /scanNetworks" in data:
            #call config update function
            pass
        elif "POST /submitNetworkID" in data:
            #call config update function
            pass
        else:
            pass
            #print("the data: ", data)

        
        print(f"Closing {IpAddr} Connection")
        
        #time.sleep(0.1)  # Prevent busy-waiting
    except:
        #print(f"Printing From {IpAddr} @ {port}")
        print(f"Closing {IpAddr} Connection")
        
    

def web_server_thread():
    #global active_clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #server_socket.settimeout(socketTimeout)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(2) #can only queue up to 5 connections
    
    print("Server started on port 80")

    
    while True:
        # Accept new client connections
        conn, addr = server_socket.accept() #socket connection and address info
        IpAddr, port = addr #addr = ip and port
        print(f"Connection from {IpAddr}:{port}")
        
        # handle client
        handle_client(conn, IpAddr, port)
        conn.close()










# http routes






#index route (GET /)
    #serve html



#config and exec update (/sysValUpdate) => periodic every 0.5 seconds
    #send systemConfig data
    #send exec data
    #on client side check if system config does not equal its own
        #store and update config pages if not equal
            #update zone modules
                #if system disabled then enabled is no
                #if bd for zone is disabled then inhibiting is off
    #on client side
        # display each attached soil moisture value in its own span tag with a colour depending: red for below ucl, green for between, yellow for above lcl
            #display N/A if no bd => contoller sets watering to inactive
        # in control logic watering status is set so client just displays
            # watering active
            # watering inactive
            # watering standing by (in the queue for automatic mode)




#historical soil moisture sensors (/getSMhistory) => every 10 minutes if ntpconnection
    #check for internet connection flag (updated in input loop)
    #send entire soil moisture log if internet connected
    #on client side we need to engage the graph


#wifi connect (/connectToWifi)
    #if connects return ssid name
        #turn off access point
    #if not then return connection error


#wifi scan (/scanNetorks)


#ap toggle (/APtoggle)
    #only if wifi connected
        #in input cycle if ntp fails then wifi will be started


# water toggle (/waterToggle)
    #recieve zone name parses the number and sets the flag


# mode toggle (/modetoggle)
    #recieve mode title sets the mode name
    #clears all the solenoids
        #sends response to client
            #client changes zone button colour and text



# get logs (/getLogs) => periodically every 2 minutes
    #send system logs





def configUpdate(data):
    #print(json.loads(data))
    systemConfigParameters = json.loads(data)
    #print(f"""new system config: {systemConfigParameters}""")
    
    
    with open(CONFIGFILEPATH, 'w') as f:
        json.dump(systemConfigParameters, f)
    


    