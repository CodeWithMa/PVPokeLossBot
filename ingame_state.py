import os
import sys
import time
import cv2
import logging
from datetime import datetime

import image_service
import screenshot


def set_up_logging_configuration():
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def send_adb_tap(x, y):
    adb_command = f"adb shell input tap {x} {y}"
    error_code = os.system(adb_command)
    return error_code == 0


def is_ingame(image_file):
    return (
        image_file == "ingame_opponent_3_pokemon_left.png"
        or image_file == "ingame_opponent_2_pokemon_left.png"
        or image_file == "ingame_opponent_1_pokemon_left.png"
        or image_file == "enemy_charge_attack.png"
    )


def load_image_templates():
    image_dir = "./images"
    template_images = {}
    for image_file in os.listdir(image_dir):
        if image_file.endswith(".png"):
            img_template = cv2.imread(
                os.path.join(image_dir, image_file), cv2.IMREAD_COLOR
            )
            template_images[image_file] = img_template
    return template_images


def run():
    set_up_logging_configuration()

    # Time the bot will stay in game until it forfeits
    time_to_stay_in_game = 5

    # Start the timer until bot forfeits the game
    start_time = time.time()

    template_images = load_image_templates()

    game_entered = False
    waiting_for_device = False

    while True:
        # Capture a screenshot and save it to a file
        if not screenshot.capture_screenshot("screenshot.png"):
            if waiting_for_device:
                print(".", end="", flush=True)
            else:
                logging.info(
                    "Error capturing screenshot. Waiting until phone is connected."
                )
                waiting_for_device = True

            # sys.exit(1)
            time.sleep(5)
            continue

        if waiting_for_device:
            waiting_for_device = False
            # print to jump to the next line after only printing ...... without jumping to next line
            print()

        # Check if the timer has run out
        elapsed_time = time.time() - start_time
        if game_entered and elapsed_time > time_to_stay_in_game:
            logging.info("Timer has run out. Forfeit the game.")
            send_adb_tap(75, 460)
            time.sleep(1)
            send_adb_tap(429, 1254)
            time.sleep(1)

        # Load the screenshot as an image
        img_screenshot = cv2.imread("screenshot.png", cv2.IMREAD_COLOR)

        # Check if any of the image files match the screenshot
        max_val = 0
        max_image_file = None
        max_coords = None
        for image_file, img_template in template_images.items():
            val, coords = image_service.find_image(img_screenshot, img_template)

            # Update the maximum value and corresponding image file and coordinates if necessary
            if val > max_val:
                max_val = val
                max_image_file = image_file
                max_coords = coords

        # Check if the maximum value is above a certain threshold
        if max_val > 0.95:
            logging.info(f"Image {max_image_file} matches with {max_val * 100}%")

            # If not ingame reset timer
            if is_ingame(max_image_file):
                if not game_entered:
                    start_time = time.time()
                    game_entered = True

                # Send tap to attack
                send_adb_tap(500, 1400)
            else:
                start_time = time.time()
                game_entered = False

                # Send an ADB command to tap on the corresponding coordinates
                send_adb_tap(max_coords[0], max_coords[1])

            if max_image_file.startswith("max_number_of_games_played_text."):
                # Turn screen off
                os.system("adb shell input keyevent 26")
                logging.info("Max number of games played. Exit program.")
                sys.exit(1)

        time.sleep(2)
