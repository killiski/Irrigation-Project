# boot.py -- run on boot-up
import network, time

# Replace the following with your WIFI Credentials
SSID = ""
SSI_PASSWORD = ""

def do_connect(timeout=4):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, SSI_PASSWORD)

        # Start a timer
        start_time = time.time()

        # Keep checking connection status until timeout
        while not sta_if.isconnected():
            if time.time() - start_time > timeout:
                print("Connection timed out!")
                return False  # Exit if connection fails within timeout
            time.sleep(0.1)  # Small delay to prevent busy-waiting

    print('Connected! Network config:', sta_if.ifconfig())
    return True  # Return success status

print("Connecting to your Wi-Fi...")
if do_connect(timeout=10):  # Set timeout to 10 seconds
    print("Successfully connected!")
else:
    print("Failed to connect to Wi-Fi.")