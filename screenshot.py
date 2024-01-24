import os
import platform


def capture_screenshot(filename):
    """
    Captures a screenshot of the Android screen using adb and saves it to a file.
    Returns True if the adb command was successful, False otherwise.
    """
    if platform.system() == "Windows":
        adb_command = "adb exec-out screencap -p > {}".format(filename)
    else:
        adb_command = "adb exec-out screencap -p > {} 2> /dev/null".format(filename)
    error_code = os.system(adb_command)
    return error_code == 0
