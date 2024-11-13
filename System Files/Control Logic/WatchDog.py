import threading
import time

class WatchdogTimer:
    def __init__(self, timeout, check_func, on_timeout, poll_interval=0.5):
        """
        Initialize the watchdog timer.

        :param timeout: Timeout duration in seconds
        :param check_func: Function that checks the condition (should return True if condition met)
        :param on_timeout: Function to call if timeout occurs (when condition not met in time)
        :param poll_interval: How frequently to poll/check the condition in seconds
        """
        self.timeout = timeout
        self.check_func = check_func
        self.on_timeout = on_timeout
        self.poll_interval = poll_interval
        self.start_time = None
        self._timer_thread = threading.Thread(target=self._watch)
        self._stop_event = threading.Event()
        self._timeout_lock = threading.Lock()  # Lock for safe timeout update

    def start(self):
        """Start the watchdog timer."""
        self.start_time = time.time()
        self._stop_event.clear()
        if not self._timer_thread.is_alive():
            self._timer_thread = threading.Thread(target=self._watch)
            self._timer_thread.start()

    def stop(self):
        """Stop the watchdog timer."""
        self._stop_event.set()

    def update_timeout(self, new_timeout):
        """Safely update the timeout while the timer is running."""
        with self._timeout_lock:
            self.timeout = new_timeout
            print(f"Timeout updated to {new_timeout} seconds.")

    def _watch(self):
        """The internal method that runs in a thread to watch the variable."""
        while not self._stop_event.is_set():
            if self.check_func():
                # Condition met, stop the watchdog
                print("Condition met, stopping the watchdog timer.")
                self.stop()
                return
            
            # Check if timeout is reached
            with self._timeout_lock:
                current_timeout = self.timeout
            if time.time() - self.start_time > current_timeout:
                print("Timeout reached, triggering on_timeout.")
                self.on_timeout()
                self.stop()
                return

            time.sleep(self.poll_interval)

# Example usage
my_var = 0  # Variable to monitor

def check_variable():
    """Check if `my_var` has changed to a specific state, e.g., value of 1."""
    return my_var == 1

def on_timeout_action():
    """Action to take if the timeout is reached."""
    print("Watchdog timeout! Variable did not reach the desired state in time.")

#watchdog = WatchdogTimer(timeout=5, check_func=check_variable, on_timeout=on_timeout_action)
#watchdog.start()