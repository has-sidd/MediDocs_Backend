import cv2
import numpy as np

def find_header_footer(image_path):
    # Load the image
    img = cv2.imread(image_path, 0)  # Read as grayscale

    # Apply edge detection
    edges = cv2.Canny(img, 100, 200)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the highest and lowest contour points
    min_y = img.shape[0]
    max_y = 0
    for contour in contours:
        for point in contour:
            y = point[0][1]
            if y < min_y:
                min_y = y
            if y > max_y:
                max_y = y

    # Calculate header and footer heights
    header_height = min_y
    footer_height = img.shape[0] - max_y

    return header_height, footer_height



def remove_header_footer(image_path, header_height, footer_height):
    # Load the image
    img = cv2.imread(image_path)

    # Get the dimensions of the image
    height, width, channels = img.shape

    # Define the regions to be removed (header and footer)
    header_region = img[0:header_height, 0:width]
    footer_region = img[height-footer_height:height, 0:width]

    # Set the regions to black
    header_region[:] = 0
    footer_region[:] = 0

    # Save the modified image
    cv2.imwrite("image_no_header_footer.jpg", img)

    print("Header and footer removed successfully!")

# Example usage
image_path = "NIBD_CBC_3.jpg"  # Replace with the path of your image

header_height, footer_height = find_header_footer(image_path)
print("Header height:", header_height)
print("Footer height:", footer_height)
remove_header_footer(image_path, header_height, footer_height)