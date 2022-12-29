import os
from PIL import Image
import imagehash


def capture_screenshot(filename):
    """
    Captures a screenshot of the Android screen using adb and saves it to a file.
    Returns True if the adb command was successful, False otherwise.
    """
    adb_command = "adb exec-out screencap -p > {}".format(filename)
    error_code = os.system(adb_command)
    return error_code == 0


def compare_screenshots(screenshot_filename, image_filename, focus_area):
    """
    Compares a screenshot with an image file using image hashing.
    The focus_area parameter is a tuple of coordinates (x1, y1, x2, y2) that defines
    the region of interest (ROI) to be compared.
    Returns True if the images match, False otherwise.
    """
    # Open the screenshot and the image file for comparison
    screenshot = Image.open(screenshot_filename)
    image_file = Image.open(image_filename)

    # Extract the ROI from each image
    x1, y1, x2, y2 = focus_area
    screenshot_roi = screenshot.crop((x1, y1, x2, y2))
    image_file_roi = image_file.crop((x1, y1, x2, y2))

    # Calculate the hash values for the two images
    screenshot_hash = imagehash.average_hash(screenshot_roi)
    image_file_hash = imagehash.average_hash(image_file_roi)

    # Check if the images
    return screenshot_hash == image_file_hash


def preprocess_screenshot(img_screenshot, image_file_coords):
    """Preprocess the screenshot and crop it to the focus areas."""
    img_screenshot_cropped = {}
    for _, (focus_area, _) in image_file_coords.items():
        x1, y1, x2, y2 = focus_area
        img_screenshot_cropped[focus_area] = img_screenshot[y1:y2, x1:x2]
    return img_screenshot_cropped
