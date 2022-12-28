import os
import sys
import time

import screenshot

# import ingame_state


def run():
    while True:
        print("Running ingame state")

        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            print("Error capturing screenshot. Is your phone connected?")
            sys.exit(1)

        # Area where the 3 Pokeballs of opponent are
        focus_area = (875, 311, 875 + 173, 311 + 50)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/ingame.png", focus_area
        )

        if image_matches:
            print("Ingame image enemy 3 Pokemon matches")
            # Click on the coordinate to block enemy charge attack
            adb_command = "adb shell input tap 555 1965"
            os.system(adb_command)

            # TODO
            # return ingame_state

        # Area where the shield to block is
        focus_area = (474, 1893, 474 + 153, 1893 + 141)

        # Compare the screenshot with an image file
        image_matches = screenshot.compare_screenshots(
            "screenshot.png", "./images/enemy_charge_attack.png", focus_area
        )

        if image_matches:
            print("Ingame image enemy charge attack matches")
            # Click on the coordinate to block enemy charge attack
            adb_command = "adb shell input tap 555 1965"
            os.system(adb_command)

            # TODO
            # return ingame_state

        time.sleep(1)
