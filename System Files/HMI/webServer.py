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

# Global list to store active clients and their ports
active_clients = []

# Lock for managing access to active_clients
client_lock = _thread.allocate_lock()

def client_thread(conn, addr, port):
    global active_clients
    print(f"New client connected: {addr}:{port}")
    
    # Add client to active clients list
    with client_lock:
        # Check if client IP already exists in the list
        existing_client = None
        for client in active_clients:
            if client['ip'] == addr:
                existing_client = client
                break
        
        if existing_client:
            # If another connection from the same client exists, remove the old one
            existing_client['conn'].close()
            existing_client['thread'].exit()
            active_clients.remove(existing_client)

        # Add the new connection as the active client
        client_data = {'ip': addr, 'port': port, 'conn': conn, 'thread': _thread.get_ident()}
        active_clients.append(client_data)

    try:
        while True:
            # Here, you would handle client requests
            data = conn.recv(1024)
            if not data:
                break
            print(f"Received from {addr}:{port}: {data.decode()}")
            conn.send(data)  # Echo data back to client

            # Check for reconnection from the same client
            with client_lock:
                if len([c for c in active_clients if c['ip'] == addr]) > 1 and client_data != active_clients[-1]:
                    print(f"Ending duplicate connection for {addr}:{port}")
                    break  # Exit thread if it's an older connection from the same client
            

            
            time.sleep(0.1)  # Prevent busy-waiting

    finally:
        # Cleanup on disconnection
        with client_lock:
            if client_data in active_clients:
                active_clients.remove(client_data)
        conn.close()
        print(f"Client {addr}:{port} disconnected")

def web_server_thread():
    global active_clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 80))
    server_socket.listen(5)
    print("Server started on port 80")

    while True:
        # Accept new client connections
        conn, addr = server_socket.accept()
        addr, port = addr
        print(f"Connection from {addr}:{port}")
        
        # Start a new thread for each client connection
        _thread.start_new_thread(client_thread, (conn, addr, port))

