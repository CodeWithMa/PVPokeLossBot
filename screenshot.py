import os


def capture_screenshot(filename):
    """
    Captures a screenshot of the Android screen using adb and saves it to a file.
    Returns True if the adb command was successful, False otherwise.
    """
    adb_command = "adb exec-out screencap -p > {} 2> /dev/null".format(filename)
    error_code = os.system(adb_command)
    return error_code == 0


def preprocess_screenshot(img_screenshot, image_file_coords):
    """Preprocess the screenshot and crop it to the focus areas."""
    img_screenshot_cropped = {}
    for _, (focus_area, _) in image_file_coords.items():
        x1, y1, x2, y2 = focus_area
        img_screenshot_cropped[focus_area] = img_screenshot[y1:y2, x1:x2]
    return img_screenshot_cropped
