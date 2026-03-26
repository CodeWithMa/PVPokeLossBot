import logging
import cv2
import os
import threading

from src import constants
from src import image_service
from src.find_image_result import FindImageResult
from src.game_action import GameAction, GameActions


def is_ingame(image_file: str) -> bool:
    return image_file.startswith("ingame_") or image_file == "enemy_charge_attack.png"


def is_screen_to_attack(image_file: str) -> bool:
    return image_file.startswith("ingame_")


def make_decision(template_images: dict[str, cv2.Mat], image_name: str) -> GameAction:
    # Check if the image file exists
    if not os.path.exists(image_name):
        logging.error(f"Image file {image_name} does not exist.")
        raise FileNotFoundError

    # Load the screenshot as an image
    img_screenshot = cv2.imread(image_name, cv2.IMREAD_COLOR)

    # Check if any of the image files match the screenshot
    find_image_results: list[tuple[str, FindImageResult]] = []

    # Compare each image in its own thread
    def compare_image(image_file, img_screenshot, img_template):
        result = image_service.find_image(img_screenshot, img_template)
        if result:
            logging.debug(f"Image {image_file} matches with {result.val * 100}%")
            if image_file.startswith("forfeit"):
                template_h, template_w = img_template.shape[:2]
                match_w = getattr(result, "width", None)
                match_h = getattr(result, "height", None)
                if match_w is not None and match_h is not None and (match_w == template_w and match_h == template_h) and result.val > 0.90:
                        find_image_results.append((image_file, result))
                else:
                    if result.val > 0.90:
                        find_image_results.append((image_file, result))
                        
    threads = []
    for image_file, img_template in template_images.items():
        thread = threading.Thread(target=compare_image, args=(image_file, img_screenshot, img_template))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    logging.debug("Found images over threshold:")
    logging.debug(find_image_results)
    return analyze_results_and_return_action_with_priority(find_image_results)

    #priority option
def analyze_results_and_return_action_with_priority(
    find_image_results: list[tuple[str, FindImageResult]]
) -> GameAction:
    if len(find_image_results) == 0:
        logging.debug("No image matches.")
        return GameAction()

    priority_list = [
        "max_number_of_games_played_text",
        "reward_",
        "start_",
        "select_master",
        "select_hypa",
        "start_button_yes",
        "welcome_to_gbl_button_text",
        "Yes",
        # TODO: Add other images here
    ]

    # For each prefix (in order), find the highest-confidence match for that prefix and return it immediately
    for priority_prefix in priority_list:
        matches = [r for r in find_image_results if r[0].startswith(priority_prefix)]
        if matches:
            # Pick highest confidence among matches
            best_file, best_result = max(matches, key=lambda x: x[1].val)
            logging.info(f"Priority match found: {best_file} with confidence {best_result.val}")
            return analyze_results_and_return_action(best_file, best_result)

    # PATCH: Only consider matches with y > 296
    filtered_results = [r for r in find_image_results if r[1].coords[1] > 296]
    if filtered_results:
        max_image_file, max_result = max(filtered_results, key=lambda x: x[1].val)
        return analyze_results_and_return_action(max_image_file, max_result)
    else:
        logging.info("No matches with y > 296 found; skipping tap.")
        return GameAction()  # No action

    #image analyze
def analyze_results_and_return_action(
    image_file: str, find_image_result: FindImageResult
) -> GameAction:
    logging.info(f"Image {image_file} matches with {find_image_result.val * 100}%")

    if image_file.startswith("max_number_of_games_played_text"):
        return GameAction(action=GameActions.exit_program)
    
    # Add: Forfeit match logic
    if image_file.startswith("forfeit"):  # Change to your forfeit template prefix
        return GameAction(
            action=GameActions.tap_position,
            position=find_image_result.coords,
            delay_before_tap=5.0  # Wait 5 seconds before tapping
        )

    # If ingame return is_ingame with true
    if is_ingame(image_file):

        # Send tap to attack
        position_to_tap = find_image_result.coords
        if is_screen_to_attack(image_file):
            position_to_tap = constants.ATTACK_TAP_POSITION

        return GameAction(
            action=GameActions.tap_position,
            position=position_to_tap,
            is_ingame=True,
        )
    else:
        # Send an ADB command to tap on the corresponding coordinates
        return GameAction(
            action=GameActions.tap_position,
            position=find_image_result.coords,
        )

    #threshold for image match
def find_images_over_threshold(template_images: dict[str, cv2.Mat], screenshot_file: str, threshold: float = 0.90) -> list[tuple[str, FindImageResult]]:
    """
    Finds all template images that match the screenshot above the given threshold.
    Returns a sorted list of (img_name, FindImageResult), highest confidence first.
    Also logs the match value for every template image.
    """
    if not os.path.exists(screenshot_file):
        logging.error(f"Screenshot file {screenshot_file} does not exist.")
        return []

    img_screenshot = cv2.imread(screenshot_file, cv2.IMREAD_COLOR)
    results = []
    for img_name, img_template in template_images.items():
        result = image_service.find_image(img_screenshot, img_template)
        if result:
            logging.info(f"Template '{img_name}': match confidence {result.val:.4f}")
            if result.val > threshold:
                results.append((img_name, result))

    # Sort by confidence descending
    results.sort(key=lambda x: x[1].val, reverse=True)
    return results
