import os
import sys
import time
import cv2

import screenshot


def is_ingame(image_file):
    return (
        image_file == "./images/ingame_opponent_3_pokemon_left.png"
        or image_file == "./images/ingame_opponent_2_pokemon_left.png"
        or image_file == "./images/ingame_opponent_1_pokemon_left.png"
        or image_file == "./images/enemy_charge_attack.png"
    )


def run():
    # Time the bot will stay in game until it forfeits
    time_to_stay_in_game = 15

    # Start the timer until bot forfeits the game
    start_time = time.time()

    # Initialize a dictionary to store the image file paths, focus areas, and corresponding coordinates
    image_file_coords = {
        "./images/ingame_opponent_3_pokemon_left.png": (
            (875, 311, 875 + 173, 311 + 50),
            (555, 1965),
        ),
        "./images/ingame_opponent_2_pokemon_left.png": (
            (875, 311, 875 + 173, 311 + 50),
            (555, 1965),
        ),
        "./images/ingame_opponent_1_pokemon_left.png": (
            (875, 311, 875 + 173, 311 + 50),
            (555, 1965),
        ),
        "./images/enemy_charge_attack.png": (
            (474, 1893, 474 + 153, 1893 + 141),
            (555, 1965),
        ),
        "./images/win.png": ((297, 1740, 297 + 489, 1740 + 87), (525, 1785)),
        "./images/win2.png": ((357, 1173, 357 + 357, 1173 + 123), (531, 2193)),
        "./images/loss.png": ((297, 1740, 297 + 489, 1740 + 87), (525, 1785)),
        "./images/loss2.png": ((180, 1167, 180 + 729, 1167 + 138), (531, 2193)),
        # This has to be before start. If it is after, then start matches with 100% and this will never match with more than 100%.
        "./images/max_number_of_games_played.png": (
            (90, 1167, 90 + 909, 1167 + 114),
            (537, 2196),
        ),
        "./images/start.png": ((300, 2064, 783, 2181), (400, 2121)),
        "./images/start2.png": ((300, 1980, 783, 2100), (400, 2040)),
        "./images/start3.png": ((300, 1980, 783, 2100), (400, 2040)),
        "./images/select_hypa_league.png": ((80, 1000, 1000, 1275), (555, 1111)),
        "./images/select_master_league.png": ((80, 1000, 1000, 1275), (555, 1111)),
        "./images/welcome_to_gbl.png": (
            (245, 2085, 245 + 590, 2085 + 100),
            (555, 2133),
        ),
        "./images/confirm_party_search.png": ((350, 2000, 720, 2175), (540, 2100)),
        "./images/rewards1.png": ((141, 1749, 141 + 213, 1749 + 138), (245, 1800)),
        "./images/rewards1.1.png": ((141, 1749, 141 + 213, 1749 + 138), (245, 1800)),
        "./images/rewards1.2.png": ((141, 1749, 141 + 213, 1749 + 138), (245, 1800)),
        "./images/rewards2.png": ((306, 1749, 306 + 213, 1749 + 138), (414, 1800)),
        "./images/claim_rewards.png": ((138, 1980, 138 + 807, 1980 + 96), (336, 2022)),
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

    game_entered = False
    waiting_for_device = False

    while True:
        # Check if the timer has run out
        elapsed_time = time.time() - start_time
        if game_entered and elapsed_time > time_to_stay_in_game:
            print("Timer has run out. Forfeit the game.")
            os.system("adb shell input tap 75 460")
            time.sleep(1)
            os.system("adb shell input tap 429 1254")
            time.sleep(1)

        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            if waiting_for_device:
                print(".", end="", flush=True)
            else:
                print("Error capturing screenshot. Waiting until phone is connected.")
                waiting_for_device = True

            # sys.exit(1)
            time.sleep(5)
            continue

        if waiting_for_device:
            waiting_for_device = False
            # print to jump to the next line after only printing ...... without jumping to next line
            print()

        # Load the screenshot as an image
        img_screenshot = cv2.imread("screenshot.png", cv2.IMREAD_COLOR)

        # Preprocess the screenshot and crop it to the focus areas
        img_screenshot_cropped = screenshot.preprocess_screenshot(
            img_screenshot, image_file_coords
        )

        # Check if any of the image files match the screenshot
        max_val = 0
        max_image_file = None
        max_coords = None
        for image_file, (focus_area, coords) in image_file_coords.items():
            # Get the preprocessed template image and cropped screenshot image
            img_template = template_images[image_file]
            img_screenshot_focus_area = img_screenshot_cropped[focus_area]

            # Check if the cropped screenshot and template image match using the find_template function
            result = cv2.matchTemplate(
                img_screenshot_focus_area, img_template, cv2.TM_CCOEFF_NORMED
            )
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

            # If not ingame reset timer
            if is_ingame(max_image_file):
                if not game_entered:
                    start_time = time.time()
                    game_entered = True
            else:
                start_time = time.time()
                game_entered = False

            if max_image_file == "./images/max_number_of_games_played.png":
                # Turn screen off
                os.system("adb shell input keyevent 26")
                print("Max number of games played. Exit program.")
                sys.exit(1)

        time.sleep(2)
