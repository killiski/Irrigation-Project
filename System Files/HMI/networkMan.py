import network
import time
import ntptime



# Network credentials
HOSTNAME = "mbesp32"
HOME_SSID = "BELL904"




def connect_to_wifi(ssid, password):
    """Connect to the specified Wi-Fi network."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while not wlan.isconnected():
        pass
    print(f"Connected to {ssid}. IP Address: {wlan.ifconfig()[0]}")

def scan_networks():
    """Scan for available Wi-Fi networks."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()  # List of tuples (ssid, bssid, channel, RSSI, authmode, hidden)
    return [net[0].decode('utf-8') for net in networks] if networks else []



def set_hostname(wlan):
    """Set the same hostname for all network types."""
    try:
        wlan.config(dhcp_hostname=HOSTNAME)  # Set hostname
        print(f"Hostname set to: {HOSTNAME}")
    except Exception as e:
        print(f"Failed to set hostname: {e}")

def connect_to_wifi(ssid, password=None):
    """Try connecting to a network with appropriate settings."""
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    set_hostname(wlan)  # Set the hostname

    try:
        print(f"Connecting to {ssid}.")
        wlan.connect(ssid, password)

        # Wait for connection
        start = time.time()
        while not wlan.isconnected():
            if time.time() - start > 10:  # Timeout after 10 seconds
                raise TimeoutError(f"Connection to {ssid} timed out.")
            time.sleep(1)


        
        print(f"Connected to {ssid}!")
        print("IP Address:", wlan.ifconfig()[0])
        
        
        ntptime.settime()
        return True  # Success

    except Exception as e:
        print(f"Error connecting to {ssid}: {e}")
        return False  # Failure


def setup_access_point():
    """Set up the ESP32 as an access point."""
    print("Setting up Access Point...")
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32-AccessPoint', password='123456789', authmode=network.AUTH_WPA_WPA2_PSK)
    set_hostname(ap)  # Set the same hostname for AP
    print("Access Point is active. IP:", ap.ifconfig()[0])  # Default IP

