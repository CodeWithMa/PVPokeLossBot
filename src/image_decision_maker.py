import logging
import cv2
import os

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
    for image_file, img_template in template_images.items():
        result = image_service.find_image(img_screenshot, img_template)
        if result:
            if result.val > 0.90:
                find_image_results.append((image_file, result))

    logging.debug(find_image_results)
    return analyze_results_and_return_action_with_priority(find_image_results)


def analyze_results_and_return_action_with_priority(
    find_image_results: list[tuple[str, FindImageResult]]
) -> GameAction:
    if len(find_image_results) == 0:
        logging.debug("No image matches.")
        return GameAction()

    priority_list = [
        "max_number_of_games_played_text.",
        "reward_",
        "start_button_text",
        "select_master",
        "select_hypa",
        # TODO: Add other images here
    ]

    for priority_file in priority_list:
        for result in find_image_results:
            image_file = result[0]
            find_image_result = result[1]
            if image_file.startswith(priority_file):
                return analyze_results_and_return_action(image_file, find_image_result)

    # Handle case where image is not in priority_list
    # Just use the best matching image
    max_image_file, max_result = max(find_image_results, key=lambda x: x[1].val)
    return analyze_results_and_return_action(max_image_file, max_result)


def analyze_results_and_return_action(
    image_file: str, find_image_result: FindImageResult
) -> GameAction:
    logging.info(f"Image {image_file} matches with {find_image_result.val * 100}%")

    if image_file.startswith("max_number_of_games_played_text."):
        return GameAction(action=GameActions.exit_program)

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
