import os
import sys
import time

import screenshot
import ingame_state


def run():
    while True:
        print("Running confirm party search state")

        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            print("Error capturing screenshot. Is your phone connected?")
            sys.exit(1)

        # Define the focus area as a tuple of coordinates (x1, y1, x2, y2)
        focus_area = (350, 2000, 720, 2175)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/confirm_party_search.png", focus_area
        )

        if image_matches:
            print("Image matches")
            # Click on the coordinate to confirm team and start search for opponent
            adb_command = "adb shell input tap 540 2100"
            os.system(adb_command)

            return ingame_state

        time.sleep(1)
