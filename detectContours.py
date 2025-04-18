import matplotlib.pyplot as plt
import cv2
import numpy as np

# Load the image
image_path = "fractures-matelles.png"
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Use Canny edge detection to detect edges
edges = cv2.Canny(blurred, 50, 150)

# Use Hough Line Transform to detect lines
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=80, minLineLength=50, maxLineGap=10)

# Create a copy of the original image to draw lines
line_image = image.copy()

# Draw the detected lines
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line[0]
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 2)

# Convert BGR to RGB for displaying with matplotlib
line_image_rgb = cv2.cvtColor(line_image, cv2.COLOR_BGR2RGB)

# Show the image with detected lines
plt.figure(figsize=(12, 8))
plt.imshow(line_image_rgb)
plt.title("Detected Linear Features (Fractures/Faults)")
plt.axis("off")
plt.show()
