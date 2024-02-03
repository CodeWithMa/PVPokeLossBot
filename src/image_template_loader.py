import cv2
import logging
import os


def load_image_templates() -> dict[str, cv2.Mat]:
    image_dir = "./images"
    template_images = {}
    images = os.listdir(image_dir)
    for image in images:
        if image.endswith(".png"):
            img_template = cv2.imread(os.path.join(image_dir, image), cv2.IMREAD_COLOR)
            template_images[image] = img_template
    logging.info(f"Loaded {len(template_images)} image templates.")
    return template_images
