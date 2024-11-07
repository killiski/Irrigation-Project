import socket
import json
import os
import time
from networkMan import scan_networks, connect_to_wifi


#Data file = /Data/data.json



# Load data from JSON file
def load_data():
    if 'data.json' in os.listdir():
        print(os.listdir())
        print(os.getcwd())
        #os.chdir("Data") # set cwd directory
        print(os.listdir("/Data"))


        with open('data.json', 'r') as f:
            return json.load(f)
    else:
        return {
            "value1": 0,
            "value2": 0,
        }



"""
{
    "value1": 0,
    "value2": 0
}
"""




# Save data to JSON file
def save_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def web_server():
    data = load_data()

    addr = socket.getaddrinfo('0.0.0.0', 80)[0][4]
    s = socket.socket()
    s.bind(addr)
    s.listen(3)
    print("Listening on", addr)

    while True:
        try:
            cl, addr = s.accept()
            print('Client connected from', addr)

            requestRaw = cl.recv(1024)
            request = requestRaw.decode()

            if '/updateWifi' in request:
                # Parse the incoming data for SSID and password
                data_str = request.split('\r\n\r\n')[1].split('\r\n')[0]
                ssid = data_str.split('&')[0].split('=')[1]
                password = data_str.split('&')[1].split('=')[1]
                connect_to_wifi(ssid, password)  # Add function to connect to the selected Wi-Fi
                response = json.dumps({"status": "connected", "ssid": ssid})
            elif '/valuesUpdate' in request:
                # Parse the incoming data for slider values
                data_str = request.split('\r\n\r\n')[1].split('\r\n')[0]
                value1 = int(data_str.split('&')[0].split('=')[1])
                value2 = int(data_str.split('&')[1].split('=')[1])
                
                # Update data with the new slider values
                data['value1'] = value1
                data['value2'] = value2
                save_data(data)
                response = json.dumps({"value1": value1, "value2": value2})
            elif '/values' in request:
                response = json.dumps(data)
            elif '/scan' in request:
                networks = scan_networks()  # Function to get available networks
                response = json.dumps({"networks": networks})
            else:
                response = html()

            cl.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
            cl.send(response.encode())
            cl.close()
        except Exception as e:
            print("Error:", e)
            cl.close()

def html():
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32 Web Server</title>
    <style>
        #wifiInput { display: none; }
        #popup { position: fixed; top: 10px; right: 10px; }
    </style>
    <script>
        function toggleWifiInput() { // show wifi pop up => i want it to display over the page not inline
            const wifiInputDiv = document.getElementById("wifiInput");
            wifiInputDiv.style.display = wifiInputDiv.style.display === "none" ? "block" : "none";
        }

        function updateWifiValues() { // input wifi values => I want to clear input boxes after to show feedback and disable submit until response
            const ssid = document.getElementById("ssid").value;
            const password = document.getElementById("password").value;
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/updateWifi", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    alert("Connected to " + response.ssid);
                    fetchValues(); // Fetch updated values
                }
            };
            xhr.send(`ssid=${ssid}&password=${password}`);
        }

        function fetchValues() {
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/values", true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    // Display fetched values
                    document.getElementById("displayValue1").innerText = response.value1;
                    document.getElementById("displayValue2").innerText = response.value2;

                    // Set slider values based on fetched values
                    // document.getElementById("sliderValue1").value = response.value1;
                    // document.getElementById("sliderValue2").value = response.value2;
                }
            };
            xhr.send();
        }

        function scanNetworks() {
            const xhr = new XMLHttpRequest();
            xhr.open("GET", "/scan", true);
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    const ssidSelector = document.getElementById("ssid");
                    ssidSelector.innerHTML = ''; // Clear previous SSIDs
                    response.networks.forEach(function(network) {
                        const option = document.createElement('option');
                        option.value = network;
                        option.textContent = network;
                        ssidSelector.appendChild(option);
                    });
                }
            };
            xhr.send();
        }

        function updateStoredValues() {
            const value1 = document.getElementById("sliderValue1").value;
            const value2 = document.getElementById("sliderValue2").value;
            const xhr = new XMLHttpRequest();
            xhr.open("POST", "/valuesUpdate", true);
            xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
            xhr.onreadystatechange = function() {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    fetchValues(); // Refresh displayed values after update
                }
            };
            xhr.send(`value1=${value1}&value2=${value2}`); // Send only slider values
        }

        setInterval(fetchValues, 5000);
    </script>
</head>
<body>
    <h3>MTR IrrI Sys</h3>
    <div id="popup">
        <button onclick="toggleWifiInput()">Toggle Wi-Fi Input</button>
    </div>
    
    <div id="wifiInput">
        <h2>Connect to Wi-Fi</h2>
        <label for="ssid">SSID:</label>
        <select id="ssid"></select><br>
        <label for="password">Password:</label>
        <input type="password" id="password" placeholder="Enter Password"><br>
        <button onclick="updateWifiValues()">Connect</button>
        <button onclick="scanNetworks()">Refresh Networks</button>
    </div>
    
    <h2>Stored Values:</h2>
    <p>Value 1: <span id="displayValue1">0</span></p>
    <input type="range" id="sliderValue1" min="0" max="100" value="0"><br>

    <p>Value 2: <span id="displayValue2">0</span></p>
    <input type="range" id="sliderValue2" min="0" max="100" value="0"><br>

    <button onclick="updateStoredValues()">Submit</button>
</body>
</html>"""






def webpage_deploy():
    #time.sleep(10)
    
    while True:
        print("Deploying server")
        web_server()











"""
"SoilMoistureSensors": [[[0.0, 0, 0] * 10,] * 5], # 5 possible zones with 10 max sensors each. each sensor has a location in the yard represented by the last two values in the sensor array element
"BodyDetectionSensors": [[False, 0] * 5], #five possible body detection sensors, with zone id
"Mode": "Manual", #or automatic
"waterQueue" : [[0] * 5],
"DateTime": {
    "localDate": "YYYY-MM-DD",
    "localTime": "HH:mm:ss",
    "Season": "winter"
},
"Zones": [['name', False, 0, 0] * 5], # 5 poissible zones with a name, watering request rectangluar area
"Esp32APCred": {
    "ssid": "",
    "password": ""

},
"Schedule": { # this is getting way to big
    "Daily": {
        "startHour": 0,
        "endHour": 23, # time
        "timeSlots": [["7:00", "9:30"], ["12:00", "13:00"], ["14:30", "15:30"], ["16:30", "19:30"]] #pick one this one is more detailed
    },
    "Seasonal": {
        "winterStart": 330,
        "springStart": 80,
        "summerStart": 150,
        "fallStart": 240,
        "springSP": 0.2 * 100,
        "summerSP": 0.25 * 100,
        "fallSP": 0.2 * 100,

    }
}"""