import subprocess
import logging
from typing import Optional


def send_adb_tap(x: int, y: int) -> bool:
    """
    Send a tap command to the Android device via ADB.
    Returns True if the command was successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["adb", "shell", "input", "tap", str(x), str(y)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            logging.error(f"ADB tap command failed: {result.stderr}")
            return False
        
        logging.debug(f"ADB tap sent to coordinates ({x}, {y})")
        return True
    
    except subprocess.TimeoutExpired:
        logging.error(f"ADB tap command timed out for coordinates ({x}, {y})")
        return False
    except (FileNotFoundError, OSError) as e:
        logging.error(f"ADB tap command failed: {e}")
        return False


def turn_screen_off() -> bool:
    """
    Turn off the Android device screen using power button keyevent.
    Returns True if the command was successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["adb", "shell", "input", "keyevent", "26"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            logging.error(f"ADB screen off command failed: {result.stderr}")
            return False
        
        logging.debug("Screen turned off via ADB")
        return True
    
    except subprocess.TimeoutExpired:
        logging.error("ADB screen off command timed out")
        return False
    except (FileNotFoundError, OSError) as e:
        logging.error(f"ADB screen off command failed: {e}")
        return False


def send_adb_keyevent(keycode: int) -> bool:
    """
    Send a keyevent to the Android device via ADB.
    Returns True if the command was successful, False otherwise.
    """
    try:
        result = subprocess.run(
            ["adb", "shell", "input", "keyevent", str(keycode)],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode != 0:
            logging.error(f"ADB keyevent {keycode} command failed: {result.stderr}")
            return False
        
        logging.debug(f"ADB keyevent {keycode} sent")
        return True
    
    except subprocess.TimeoutExpired:
        logging.error(f"ADB keyevent {keycode} command timed out")
        return False
    except (FileNotFoundError, OSError) as e:
        logging.error(f"ADB keyevent {keycode} command failed: {e}")
        return False
