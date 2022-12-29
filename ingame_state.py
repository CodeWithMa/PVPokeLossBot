import os
import sys
import time
import cv2

import screenshot

def preprocess_screenshot(img_screenshot, image_file_coords):
    """Preprocess the screenshot and crop it to the focus areas."""
    # Crop the screenshot to the focus areas
    img_screenshot_cropped = {}
    for _, (focus_area, _) in image_file_coords.items():
        x1, y1, x2, y2 = focus_area
        img_screenshot_cropped[focus_area] = img_screenshot[y1:y2, x1:x2]
    return img_screenshot_cropped

def run():
    # Initialize a dictionary to store the image file paths, focus areas, and corresponding coordinates
    image_file_coords = {
        "./images/ingame_opponent_3_pokemon_left.png": ((875, 311, 875 + 173, 311 + 50), (555, 1965)),
        "./images/ingame_opponent_2_pokemon_left.png": ((875, 311, 875 + 173, 311 + 50), (555, 1965)),
        "./images/ingame_opponent_1_pokemon_left.png": ((875, 311, 875 + 173, 311 + 50), (555, 1965)),
        "./images/enemy_charge_attack.png": ((474, 1893, 474 + 153, 1893 + 141), (555, 1965)),
        "./images/win.png": ((297, 1740, 297 + 489, 1740 + 87), (525, 1785)),
    }

    # Preprocess the template images
    template_images = {}
    for image_file, (focus_area, _) in image_file_coords.items():
        # Load the image file as an image
        img_template = cv2.imread(image_file, cv2.IMREAD_COLOR)

        # Crop the template image to the focus area
        x1, y1, x2, y2 = focus_area
        img_template_cropped = img_template[y1:y2, x1:x2]

        # Add the preprocessed template image to the dictionary
        template_images[image_file] = img_template_cropped

    while True:
        print("Running ingame state")

        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            print("Error capturing screenshot. Is your phone connected?")
            sys.exit(1)

        # Load the screenshot as an image
        img_screenshot = cv2.imread("screenshot.png", cv2.IMREAD_COLOR)

        # Preprocess the screenshot and crop it to the focus areas
        img_screenshot_cropped = preprocess_screenshot(img_screenshot, image_file_coords)

        # Check if any of the image files match the screenshot
        max_val = 0
        max_image_file = None
        max_coords = None
        for image_file, (focus_area, coords) in image_file_coords.items():
            # Get the preprocessed template image and cropped screenshot image
            img_template = template_images[image_file]
            img_screenshot_focus_area = img_screenshot_cropped[focus_area]

            # Check if the cropped screenshot and template image match using the find_template function
            result = cv2.matchTemplate(img_screenshot_focus_area, img_template, cv2.TM_CCOEFF_NORMED)
            min_val, val, min_loc, loc = cv2.minMaxLoc(result)

            # Update the maximum value and corresponding image file and coordinates if necessary
            if val > max_val:
                max_val = val
                max_image_file = image_file
                max_coords = coords
                # print(f"New max matching: {max_image_file} with {max_val}%")

        # Check if the maximum value is above a certain threshold
        if max_val > 0.95:
            print(f"Ingame image {max_image_file} matches with {max_val}%")
            # Send an ADB command to tap on the corresponding coordinates
            adb_command = f"adb shell input tap {max_coords[0]} {max_coords[1]}"
            os.system(adb_command)

        time.sleep(1)
