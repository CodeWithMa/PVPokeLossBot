import os
import sys
import time

import screenshot
import select_league_state


def run():
    while True:
        print("Running start_state")

        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            print("Error capturing screenshot. Is your phone connected?")
            sys.exit(1)

        # Define the focus area as a tuple of coordinates (x1, y1, x2, y2)
        focus_area = (300, 2064, 783, 2181)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/start.png", focus_area
        )

        if image_matches:
            print("Image matches")
            # Click on the coordinate to start a new game
            adb_command = "adb shell input tap 400 2121"
            os.system(adb_command)

            return select_league_state

        # Define the focus area as a tuple of coordinates (x1, y1, x2, y2)
        focus_area = (300, 1980, 783, 2100)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/start2.png", focus_area
        )

        if image_matches:
            print("Image matches")
            # Click on the coordinate to start a new game
            adb_command = "adb shell input tap 400 2040"
            os.system(adb_command)

            return select_league_state

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/start3.png", focus_area
        )

        if image_matches:
            print("Image matches")
            # Click on the coordinate to start a new game
            adb_command = "adb shell input tap 400 2040"
            os.system(adb_command)

            return select_league_state

        time.sleep(1)
