import cv2

from src.find_image_result import FindImageResult


def show_image(img, top_left, bottom_right):
    # Draw rectangle and Show the result
    cv2.rectangle(img, top_left, bottom_right, (0, 255, 0), 2)
    cv2.imshow("Result", img)
    cv2.waitKey(0)


def convert_to_greyscale(img_to_convert):
    return cv2.cvtColor(img_to_convert, cv2.COLOR_BGR2GRAY)


def find_image(img_large, img_small) -> FindImageResult | None:
    if img_large is None:
        print("Image large is none")
        return

    if img_small is None:
        print("Image small is none")
        return

    # Convert the images to grayscale
    gray_large = convert_to_greyscale(img_large)
    gray_small = convert_to_greyscale(img_small)

    # Find the dimensions of the smaller image
    h, w = gray_small.shape

    # Perform template matching to find the position of the smaller image
    res = cv2.matchTemplate(gray_large, gray_small, cv2.TM_CCOEFF_NORMED)

    # Get the minimum and maximum values in the result
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

    # Calculate the center of the matching area
    x = max_loc[0] + w // 2
    y = max_loc[1] + h // 2

    # # For testing: Show image
    # top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # show_image(img_large, top_left, bottom_right)

    # Return the maximum value and the center of the matching area
    return FindImageResult(max_val, (x, y))
