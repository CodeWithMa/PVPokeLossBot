import os


def capture_screenshot(filename):
    """
    Captures a screenshot of the Android screen using adb and saves it to a file.
    Returns True if the adb command was successful, False otherwise.
    """
    adb_command = "adb exec-out screencap -p > {}".format(filename)
    error_code = os.system(adb_command)
    return error_code == 0
