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

        if image_matches:
            print("Image select_hypa_league matches")
            # Click on the coordinate to select the first league
            adb_command = "adb shell input tap 555 1111"
            os.system(adb_command)

            return confirm_party_search_state

        # TODO Create checks for more pictures of the different leagues
        # Only hyper league works right now

        # There are two possibilities after clicking on start, if no game has been played
        # the welcome to gbl screen is shown before the select league screen pops up.
        # So just press the button here and stay in this state.
        # Define the focus area for the button
        focus_area = (245, 2085, 245+590, 2085+100)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/welcome_to_gbl.png", focus_area
        )

        if image_matches:
            print("Image welcome_to_gbl matches")
            # Click on the coordinate to access battle league
            adb_command = "adb shell input tap 555 2133"
            os.system(adb_command)

        time.sleep(1)
