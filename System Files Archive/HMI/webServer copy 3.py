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

MAX_CONNECTIONS = 3
HTML_FILE_PATH = "HMI/Irrigation System UI final.html"
socketTimeout = 10  # Timeout in seconds

# Global client tracking
active_clients = set()
update_clients = set()  # Clients waiting for update
config_update_lock = _thread.allocate_lock()  # Use _thread's lock

def flush_client_buffer(conn):
    """
    Flush the recv() buffer for a client to discard any unread data.
    """
    try:
        while True:
            data = conn.recv(1024)
            if not data:  # No more data
                break
    except Exception as e:
        print(f"Error during buffer flush: {e}")

def send_html_file_in_chunks(conn, file_path, chunk_size=512):
    """
    Send HTML content from a file stored on disk in chunks.
    """
    try:
        with open(file_path, 'rb') as file:
            while (chunk := file.read(chunk_size)):
                conn.send(chunk)
    except OSError as e:
        print(f"Error opening file: {e}")
        conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError opening file.")
    except Exception as e:
        print(f"Error sending file: {e}")
        conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError sending file.")

def handle_client(conn, addr):
    print("Entering client handler for:", addr)

    global update_clients, active_clients
    print(f"{addr[0]} in active_clients: {active_clients}")

    if len(active_clients) >= MAX_CONNECTIONS:
        print("Maximum connections reached. Denying new connection.")
        conn.send(html_response("Server full. Try again later."))
        print("Closing connection from:", addr)
        conn.close()
        return
        

    # Accept a new client connection if within limit
    if addr[0] in active_clients:
        print("Already connected.")
        print("Closing new connection from:", addr)
        conn.close()
        return
        

    active_clients.add(addr[0])
    print(f"Active clients: {active_clients}")

    # Record the start time to handle timeouts
    start_time = time.time()

    while True:
        try:
            # Check for timeout by comparing the elapsed time
            if time.time() - start_time > socketTimeout:
                print(f"Timeout with client {addr}. Closing connection.")
                break  # Timeout

            request = conn.recv(1024).decode()
            print("My request: ", request)

            if not request:  # Client disconnected
                print("Closing connection from:", addr)
                conn.close()
                return

            # If client is part of the update list, flush their recv buffer
            if addr in update_clients:
                print(f"Client {addr} is in the update list. Flushing buffer.")
                flush_client_buffer(conn)
                conn.send(html_response("Config update in progress. Please wait."))
                continue

            # Handle /configUpdate request
            if "GET /configUpdate" in request:
                send_html_file_in_chunks(conn, HTML_FILE_PATH)

                # Lock and update clients except the requesting one
                with config_update_lock:
                    print(f"Initiating config update for client {addr}")
                    update_clients = {client for client in active_clients if client != addr}

                continue  # Restart loop after processing update request

            # Default behavior for normal requests
            send_html_file_in_chunks(conn, HTML_FILE_PATH)

        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break  # Break on error

        finally:
            active_clients.discard(addr)
            print("Closing connection from:", addr)
            conn.close()

def html_response(content):
    """
    Return a basic HTML response.
    """
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>{content}</h1></body></html>
""".encode('utf-8')

def start_server():
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        print('Client connected from', addr)

        # Start a new thread for each client connection using _thread
        _thread.start_new_thread(handle_client, (conn, addr))
        print(f"Thread started for client {addr}")

