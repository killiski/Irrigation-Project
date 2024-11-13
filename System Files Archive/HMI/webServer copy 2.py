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
import uasyncio as asyncio

MAX_CONNECTIONS = 3
HTML_FILE_PATH = "HMI/Irrigation System UI final.html"
socketTimeout = 10

# Global client tracking
active_clients = set()
update_clients = set()  # Clients waiting for update
config_update_lock = asyncio.Lock()

async def flush_client_buffer(conn):
    """
    Flush the recv() buffer for a client to discard any unread data.
    """
    try:
        while True:
            data = await asyncio.wait_for(conn.recv(1024), timeout=1)
            if not data:  # No more data
                break
    except asyncio.TimeoutError:
        pass  # Timeout is expected when flushing

async def send_html_file_in_chunks(conn, file_path, chunk_size=512):
    """
    Send HTML content from a file stored on disk in chunks.
    """
    try:
        with open(file_path, 'rb') as file:
            while (chunk := file.read(chunk_size)):
                await asyncio.wait_for(conn.send(chunk), timeout=socketTimeout)
    except OSError as e:
        print(f"Error opening file: {e}")
        await conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError opening file.")
    except Exception as e:
        print(f"Error sending file: {e}")
        await conn.send(b"HTTP/1.1 500 Internal Server Error\r\n\r\nError sending file.")

async def handle_client(conn, addr):
    print("entering async")

    global update_clients, active_clients
    print(f"{addr[0]} in {active_clients}")
    

    if len(active_clients) >= MAX_CONNECTIONS:
        print("Maximum connections reached. New connection attempts will be denied.")
        await conn.send(html_response("Server full. Try again later."))
        print("Closing connection from: ", addr)
        conn.close()
        return

    # Accept a new client connection if within limit
    

    if addr[0] in active_clients:
        print("already connected.")
        print("Closing new connection from: ", addr)
        conn.close()
        return
        


    active_clients.add(addr)
    print(active_clients)


    

    while True:
        try:
            #request = await asyncio.wait_for(conn.recv(1024), timeout=socketTimeout)
            request = conn.recv(1024).decode()
                                             
            if not request:  # Client disconnected
                print("Closing connection from: ", addr)
                conn.close()
                return

            # If client is part of the update list, flush their recv buffer
            if addr in update_clients:
                print(f"Client {addr} is in the update list. Flushing buffer.")
                await flush_client_buffer(conn)
                await conn.send(html_response("Config update in progress. Please wait."))
                continue

            # Handle /configUpdate request
            if "GET /configUpdate" in request:
                await send_html_file_in_chunks(conn, HTML_FILE_PATH)

                # Lock and update clients except the requesting one
                async with config_update_lock:
                    print(f"Initiating config update for client {addr}")
                    update_clients = {client for client in active_clients if client != addr}

                continue  # Restart loop after processing update request

            # Default behavior for normal requests
            await send_html_file_in_chunks(conn, HTML_FILE_PATH)
        
        except asyncio.TimeoutError:
            if addr in update_clients:
                print(f"Client {addr} is in the update list. Skipping recv.")
                await conn.send(html_response("Config update in progress."))
                continue
            else:
                print(f"Timeout with client {addr}: {e}")
                break  # Break on timeout

        finally:
            active_clients.discard(addr)
            print("Closing connection from: ", addr)
            conn.close()

def html_response(content):
    """
    Return a basic HTML response.
    """
    return f"""HTTP/1.1 200 OK
Content-Type: text/html

<html><body><h1>{content}</h1></body></html>
""".encode('utf-8')

async def start_server():
    #server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket = socket.socket()
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    
    while True:
        conn, addr = server_socket.accept()
        print('Client connected from', addr)

        
        
        # Start a new task for each client connection
        asyncio.create_task(handle_client(conn, addr))
        print("task created for: ", addr)

# Start the server using asyncio event loop

