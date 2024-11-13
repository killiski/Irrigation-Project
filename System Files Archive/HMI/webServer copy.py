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

# Global lock and client tracking
config_update_lock = _thread.allocate_lock()
update_clients = set()  # Clients waiting for update
active_clients = set()  # All active clients

MAX_CONNECTIONS = 3  # Limit to 3 connections
HTML_FILE_PATH = "HMI/Irrigation System UI final.html"  # Path to your HTML file
socketTimeout = 10


def flush_client_buffer(conn):
    """
    Flush the recv() buffer for a client to discard any unread data.
    """
    try:
        while True:
            # Set a short timeout so it doesn't block forever
            data = conn.recv(1024)
            if not data:  # If no more data, break the loop
                break
            # Optionally, log or print discarded data for debugging
            # print(f"Discarded data: {data}")
    except OSError as e:
        if e.args[0] == -1:  # Timeout error code in MicroPython
            pass  # Expected timeout, no data to flush

def send_html_file_in_chunks(conn, file_path, chunk_size=512):
    """
    Send HTML content from a file stored on disk in chunks.
    """
    conn.settimeout(None)
    conn.setblocking(False)
    try:
        try:
            with open(file_path, 'rb') as file:
                while True:
                    chunk = file.read(chunk_size)
                    #print(chunk)
                    if not chunk:  # End of file
                        break
                    conn.send(chunk)
                    #time.sleep(0.1)  # Optional delay to smoothen chunk sending
        except OSError as e:
            print(f"Error opening file: {e}")
            conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError opening file.")
        except Exception as e:
            print(f"Error reading and sending file: {e}")
            conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError sending file.")
    
    except Exception as e:
        print(f"Error in sending HTML file: {e}")
        conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError sending file.")
    finally:
        # Restore the original timeout value
        conn.settimeout(socketTimeout)
        conn.setblocking(True)

def handle_client(conn, addr):
    global update_clients, active_clients
    try:
        active_clients.add(addr)  # Track the client in active connections
        conn.settimeout(socketTimeout)  # Set timeout for socket operations


        while True:
            try:
                request = conn.recv(1024).decode('utf-8')
                
                if not request:  # Client disconnected
                    break

                # If client is part of the update list, flush their recv buffer
                if addr in update_clients:
                    print(f"Client {addr} is in the update list. Flushing buffer.")
                    flush_client_buffer(conn)  # Flush the buffer
                    conn.send(html_response("Config update in progress. Please wait."))
                    continue  # Restart the loop instead of breaking it

                # Handle /configUpdate request
                if "GET /configUpdate" in request:
                    # Send a refresh page before initiating the update
                    send_html_file_in_chunks(conn, HTML_FILE_PATH)  # Send file in chunks

                    # Lock and update clients except the requesting one
                    if config_update_lock.acquire(blocking=False):
                        try:
                            print(f"Initiating config update for client {addr}")
                            update_clients = {client for client in active_clients if client != addr}
                        finally:
                            config_update_lock.release()
                    continue  # Restart the loop after processing the update request

                # Default behavior for normal requests
                send_html_file_in_chunks(conn, HTML_FILE_PATH)
            
            except OSError as e:
                if e.args[0] == -1:  # Timeout error code in MicroPython
                    if addr in update_clients:
                        print(f"Client {addr} is in the update list. Skipping recv.")
                        conn.send(html_response("Config update in progress."))
                        continue  # Skip further processing and restart the loop
                else:
                    print(f"Error with client {addr}: {e}")
                    break  # Break the loop if other errors occur

    finally:
        active_clients.discard(addr)
        conn.close()

def html_response(content):
    """
    Return a basic HTML response.
    """
    return """HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>{}</h1></body></html>
""".format(content).encode('utf-8')

def start_server():
    # Set up the server socket

    """addr = socket.getaddrinfo('0.0.0.0', 80)[0][4]
    s = socket.socket()
    s.bind(addr)
    s.listen(3)"""



    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    print("Server started, waiting for connections...")
    
    while True:
        if len(active_clients) >= MAX_CONNECTIONS:
            print("Maximum connections reached. New connection attempts will be denied.")
            conn, addr = server_socket.accept()
            conn.send(html_response("Server full. Try again later."))
            conn.close()
            continue

        # Accept a new client connection if within limit
        conn, addr = server_socket.accept()
        print("New connection from:", addr)
        
        # Start a new thread for each client connection
        _thread.start_new_thread(handle_client, (conn, addr))

# Start the server in a separate thread
#_thread.start_new_thread(start_server, ())

# Keep the main thread running
