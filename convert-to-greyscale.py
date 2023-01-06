import os
import cv2

input_dir = 'images'

# Loop through all the files in the input directory
for file in os.listdir(input_dir):
    # Check if the file is a png file
    if file.endswith('.png'):
        # Load the image
        img = cv2.imread(os.path.join(input_dir, file))

        print(f'Converting image: {file}')
        # Convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Save the grayscale image
        cv2.imwrite(os.path.join(input_dir, file), gray)

print('Done!')
