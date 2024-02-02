import logging
import cv2

from src import image_service
from src.game_action import GameAction, GameActions


def is_ingame(image_file: str) -> bool:
    return image_file.startswith("ingame_") or image_file == "enemy_charge_attack.png"


def make_decision(template_images: dict[str, cv2.Mat], image_name: str) -> GameAction:
    # Load the screenshot as an image
    img_screenshot = cv2.imread(image_name, cv2.IMREAD_COLOR)

    # Check if any of the image files match the screenshot
    max_val = 0
    max_image_file: str = ""
    max_coords = None
    for image_file, img_template in template_images.items():
        result = image_service.find_image(img_screenshot, img_template)
        if result:
            val, coords = result
        else:
            # handle case where find_image returns None
            val, coords = 0, None

        # Update the maximum value and corresponding image file and coordinates if necessary
        if val > max_val:
            max_val = val
            max_image_file = image_file
            max_coords = coords

    # Check if the maximum value is above a certain threshold
    if max_val > 0.90:
        logging.info(f"Image {max_image_file} matches with {max_val * 100}%")

        if max_image_file.startswith("max_number_of_games_played_text."):
            return GameAction(action=GameActions.exit_program)

        # If not ingame reset timer
        if is_ingame(max_image_file):
            # Send tap to attack
            return GameAction(action=GameActions.tap_position, position=(500, 1400), is_ingame=True)
        else:
            # Send an ADB command to tap on the corresponding coordinates
            return GameAction(action=GameActions.tap_position, position=max_coords)

    return GameAction()
