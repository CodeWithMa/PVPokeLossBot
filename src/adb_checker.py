import subprocess
import logging
from typing import Tuple, Optional


def is_adb_installed() -> bool:
    """
    Check if ADB (Android Debug Bridge) is installed and available in PATH.
    Returns True if ADB is installed, False otherwise.
    """
    try:
        result = subprocess.run(
            ["adb", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def get_connected_devices() -> Tuple[bool, list]:
    """
    Get list of connected ADB devices.
    Returns (success, devices_list) where devices_list contains device IDs.
    """
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            return False, []
        
        # Parse adb devices output
        lines = result.stdout.strip().split('\n')
        devices = []
        
        for line in lines[1:]:  # Skip "List of devices attached" header
            if line.strip() and '\t' in line:
                device_id, status = line.split('\t')
                if status.strip() == 'device':  # Only count devices that are ready
                    devices.append(device_id.strip())
        
        return True, devices
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False, []


def check_adb_connectivity() -> bool:
    """
    Test if ADB can execute a simple command on the connected device.
    Returns True if ADB is working properly, False otherwise.
    """
    try:
        result = subprocess.run(
            ["adb", "shell", "echo", "test"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0 and "test" in result.stdout
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        return False


def check_adb_status() -> Tuple[bool, str]:
    """
    Comprehensive ADB status check.
    Returns (is_ready, status_message) where is_ready indicates if ADB is ready to use.
    """
    # Check if ADB is installed
    if not is_adb_installed():
        return False, "ADB (Android Debug Bridge) is not installed or not in PATH. Please install Android SDK platform tools."
    
    # Check for connected devices
    success, devices = get_connected_devices()
    if not success:
        return False, "Failed to query ADB devices. ADB may not be working properly."
    
    if not devices:
        return False, "No Android devices connected. Please connect your Android device and enable USB debugging."
    
    if len(devices) > 1:
        logging.warning(f"Multiple devices detected: {devices}. Using the first one.")
    
    # Test ADB connectivity
    if not check_adb_connectivity():
        return False, "ADB is installed and devices are connected, but unable to communicate with device. Check USB debugging permissions."
    
    device_count = len(devices)
    device_word = "device" if device_count == 1 else "devices"
    return True, f"ADB is ready. {device_count} {device_word} connected: {', '.join(devices)}"


def wait_for_device(timeout_seconds: int = 30) -> bool:
    """
    Wait for an ADB device to be connected and ready.
    Returns True if device becomes available within timeout, False otherwise.
    """
    import time
    
    start_time = time.time()
    while time.time() - start_time < timeout_seconds:
        is_ready, message = check_adb_status()
        if is_ready:
            logging.info(message)
            return True
        
        logging.info("Waiting for ADB device...")
        time.sleep(2)
    
    return False