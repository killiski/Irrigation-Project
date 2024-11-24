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
import _thread
import time
import os
from Data.globalData import clients

MAX_CONNECTIONS = 3
HTML_FILE_PATH = "HMI/Irrigation System UI final.html"
socketTimeout = 1  # Timeout in seconds
sources = {}

# Global list to store active clients and their ports
#active_clients = {}
#clients = {}

# Lock for managing access to active_clients
client_lock = _thread.allocate_lock()

def client_thread(ip_address):
    send_html_file_in_chunks(clients[ip_address][0], HTML_FILE_PATH)
    
    while True:
        # Check if the IP address has any active clients
        

        
        
        clientEpoch = sources[ip_address]
        clientEpoch.setblocking(False)
        
        
        if len(clients[ip_address]) < 1:
            #print("clientEpoch")
            try:
                if clientEpoch.recv(1024).decode('utf-8') == "":
                    print("disconnecting client")

                    del sources[ip_address]
                    del clients[ip_address]
                    break
                time.sleep(0.05)
            except:
                continue

        client_sock = clients[ip_address][0]  # Get the first socket for that IP address
        
        print(f"printing client socket and epoch {client_sock}  :  {clientEpoch}")


        try:
            if clientEpoch == client_sock:
                print("first time around")
                request = client_sock.recv(1024).decode('utf-8')
            else:
                request = client_sock.recv(1024).decode('utf-8')
                    
            

            chechVar = (client_sock == clientEpoch)
            print(f"did client socket equal epoch socket {chechVar}")
            



            # Read from the client socket
            #request = client_sock.read().decode('utf-8')
            #if len(request) < 10:
            print(request)
            
            
            


            if request:
                pass
                #print(f"Client Sent:\n{request}")
                # Handle the request (here we send a simple response for demo)
                if "GET /" in request:
                    send_html_file_in_chunks(clients[ip_address][0], HTML_FILE_PATH)
    
                #client_sock.send("HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello from ESP32!")
                
            
            if client_sock == clientEpoch:
                clients[ip_address].remove(client_sock)
                continue
            clients[ip_address].remove(client_sock)
            client_sock.close()
            

        except Exception as e:
            print(f"Error with client {ip_address}: {e}")
            client_sock.close()
            del clients[ip_address]
            
        


def web_server_thread():
    #accept clients and spawn threads
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    server_socket.settimeout(socketTimeout)
    print("Server started on port 80")

    while True:
        try:
            client_sock, client_addr = server_socket.accept()
            ip_address = client_addr[0]  # Get the IP address from the client address
            
            # Add the client socket to the dictionary for the corresponding IP address
            if ip_address not in clients.keys():
                clients[ip_address] = []
                
            else:
                if len(clients[ip_address]) > 3:
                    clients[ip_address].remove(client_sock)
                    print(f"Client handling busy. discarding {client_addr[1]}")
                    continue
                
                clients[ip_address].append(client_sock)
                print(clients)
                print("redirecting to client thread")
                continue
            
            clients[ip_address].append(client_sock)
            sources[ip_address] = client_sock
            #sources[ip_address].setblocking(0)
            
            
            # Start a new thread to handle this client IP address
            _thread.start_new_thread(client_thread, (ip_address, ))
        
        except Exception as e:
            pass
            #print(f"Error accepting client: {e}")
























def flush_buffer(client_socket, flush_timeout=1.0):
    """Flush the recv buffer with a temporary timeout."""
    # Store the original timeout
    
    try:
        # Set a temporary timeout for flushing
        client_socket.settimeout(flush_timeout)
        while True:
            try:
                # Attempt to read data
                print("Flushing the buffer")
                data = client_socket.recv(1024)
                if not data:  # No more data to read
                    break
            except OSError:
                # Timeout reached or other recv error
                break
    finally:
        # Restore the original timeout
        print("exiting")
        client_socket.settimeout(None)


















def send_html_file_in_chunks(conn, file_path, chunk_size=256):
    """
    Send HTML content from a file stored on disk in chunks.
    """
    try:
        #file_size = os.stat(file_path)[6]
        conn.send(b"HTTP/1.1 200 OK\r\n")
        conn.send(b"Content-Type: text/html; charset=UTF-8\r\n")
        #conn.send(b"Connection: close\r\n")
        #conn.send(b"Keep-Alive: timeout=60, max=100\r\n")
        conn.send(b"Transfer-Encoding: chunked\r\n")
        conn.send(b"\r\n")

        with open(file_path, 'rb') as file:
            while (chunk := file.read(chunk_size)):
                conn.send(f"{len(chunk):X}\r\n".encode())
                conn.send(chunk)
                conn.send(b"\r\n")

        conn.send(b"0\r\n\r\n")
    except:
        return -1

