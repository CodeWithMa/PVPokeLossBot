import os
import platform


def capture_screenshot(filename: str) -> bool:
    """
    Captures a screenshot of the Android screen using adb and saves it to a file.
    Returns True if the adb command was successful, False otherwise.
    """
    if platform.system() == "Windows":
        adb_command = f"adb exec-out screencap -p > {filename}"
    else:
        adb_command = f"adb exec-out screencap -p > {filename} 2> /dev/null"
    error_code = os.system(adb_command)
    return error_code == 0
