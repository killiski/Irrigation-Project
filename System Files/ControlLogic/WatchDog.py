import time

class WatchdogTimer:
    def __init__(self, timeout=0):
        """
        Initialize the watchdog timer.

        :param timeout: Timeout duration in seconds (default is 0, meaning no timeout set)
        """
        self.timeout = timeout
        self.start_time = None

    def start(self):
        """Start the watchdog timer."""
        self.start_time = time.time()

    def stop(self):
        """Stop the watchdog timer."""
        self.start_time = None

    def is_running(self):
        """Check if the timer is running."""
        return self.start_time is not None

    def is_expired(self):
        """Check if the timer has expired."""
        if not self.is_running():
            return False
        return time.time() - self.start_time > self.timeout

    def set_timeout(self, timeout):
        """Set a new timeout value."""
        self.timeout = timeout


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