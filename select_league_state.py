import os
import sys
import time

import screenshot
import confirm_party_search_state


def run():
    while True:
        print("Running select leage state")

        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            print("Error capturing screenshot. Is your phone connected?")
            sys.exit(1)

        # Define the focus area as a tuple of coordinates (x1, y1, x2, y2)
        focus_area = (80, 1000, 1000, 1275)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/select_hypa_league.png", focus_area
        )

        # TODO Create checks for more pictures of the different leagues
        # Only hyper league works right now

        if image_matches:
            print("Image matches")
            # Click on the coordinate to select the first league
            adb_command = "adb shell input tap 555 1111"
            os.system(adb_command)

            return confirm_party_search_state

        time.sleep(1)
