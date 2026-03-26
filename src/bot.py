import sys
import time
import logging
import hashlib

from src import constants
from src import screenshot
from src.adb_commands import send_adb_tap, turn_screen_off
from src.game_action import GameActions
from src.image_decision_maker import find_images_over_threshold
from src.image_template_loader import load_image_templates

last_hash = None

def hash_image(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def run(skip_adb_check=False):
    global last_hash 
    time_to_stay_in_game = 3
    start_time = time.time()
    template_images = load_image_templates()

    game_entered = False
    waiting_for_device = False

    while True:
        # Capture screenshot
        if not screenshot.capture_screenshot(constants.SCREENSHOT_FILE_NAME):
            if waiting_for_device:
                print(".", end="", flush=True)
            else:
                logging.info("Error capturing screenshot. Waiting until phone is connected.")
                waiting_for_device = True
            time.sleep(5)
            continue

        if waiting_for_device:
            waiting_for_device = False
            new_hash = hash_image(constants.SCREENSHOT_FILE_NAME)
            if new_hash == last_hash:
                time.sleep(2.5)
                continue
            last_hash = new_hash

        # Frame-skip: skip processing if screenshot hasn't changed
        new_hash = hash_image(constants.SCREENSHOT_FILE_NAME)
        logging.debug(f"Screenshot hash: {new_hash}")
        if new_hash == last_hash:
            time.sleep(2.5)
            continue
        last_hash = new_hash

        # --- NEW LOGIC: Pick best match with y > 296, or second best if top is not valid ---
        logging.info("Running image matching...")

        # Get all matches above threshold (assuming this returns sorted list of (img_name, FindImageResult))
        matches = find_images_over_threshold(template_images, constants.SCREENSHOT_FILE_NAME)
        logging.info(f"Found images over threshold: {matches}")

        tapped = False
        for img_name, result in matches:
            if result.coords[1] > 296:
                # Use GameAction decision for delay
                from src.image_decision_maker import analyze_results_and_return_action
                action = analyze_results_and_return_action(img_name, result)
                if getattr(action, "delay_before_tap", 0.0) > 0:
                    logging.info(f"Waiting {action.delay_before_tap} seconds before tapping for '{img_name}'...")
                    time.sleep(action.delay_before_tap)
                logging.info(f"Tapping {img_name} at {result.coords} (confidence {result.val*100:.2f}%)")
                send_adb_tap(result.coords[0], result.coords[1])
                tapped = True
                break  # only tap the best match with y > 296

        if not tapped and matches:
            # log a warning if no valid taps found
            logging.info(f"No matches with y > 296 found; skipping tap.")

        # Exit logic if needed
        # (implement your exit logic here as before)
        # Example:
        # if some_exit_condition:
        #     turn_screen_off()
        #     logging.info("Max number of games played. Exit program.")
        #     sys.exit()

        time.sleep(1.5)
