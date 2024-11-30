import cv2
import numpy as np
import os

# Input and output folder paths
input_folder = "input_images"
output_folder = "output_images"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Define the background color range (example: white background)
lower_bound = np.array([0, 0, 200])   # Adjust to your background color
upper_bound = np.array([180, 25, 255])  # Adjust to your background color

# Process each image in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        # Load the image
        image_path = os.path.join(input_folder, filename)
        image = cv2.imread(image_path)

        # Convert to HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Create a mask for the background
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Invert the mask to focus on the character
        mask_inv = cv2.bitwise_not(mask)

        # Extract the character using the inverted mask
        character = cv2.bitwise_and(image, image, mask=mask_inv)

        # Save the processed image
        output_path = os.path.join(output_folder, filename)
        cv2.imwrite(output_path, character)

        print(f"Processed and saved: {output_path}")