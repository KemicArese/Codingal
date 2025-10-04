import cv2
import numpy as np

def apply_filter(image, filter_type):
    filtered_image = image.copy()

    if filter_type == 'red_tint':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 0] = 0

    elif filter_type == 'green_tint':
        filtered_image[:, :, 0] = 0
        filtered_image[:, :, 2] = 0

    elif filter_type == 'blue_tint':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 2] = 0

    elif filter_type == 'sobel':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=3)
        sobel_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
        sobel_magnitude = np.uint8(np.clip(sobel_magnitude, 0, 255))
        filtered_image = cv2.cvtColor(sobel_magnitude, cv2.COLOR_GRAY2BGR)

    elif filter_type == 'canny':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        canny_edges = cv2.Canny(gray_image, 20, 200)
        filtered_image = cv2.cvtColor(canny_edges, cv2.COLOR_GRAY2BGR)

    elif filter_type == 'laplacian':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        laplacian = np.uint8(np.clip(laplacian, 5, 255))
        filtered_image = cv2.cvtColor(laplacian, cv2.COLOR_GRAY2BGR)

    elif filter_type == 'gaussian':
        filtered_image = cv2.GaussianBlur(image, (5, 5), 0)

    elif filter_type == 'median':
        filtered_image = cv2.medianBlur(image, 5)

    return filtered_image

filter_type = 'original'

print("Press the following keys to change filters:")
print("r: Red Tint")
print("g: Green Tint")
print("b: Blue Tint")
print("s: Sobel Edge Detection")
print("c: Canny Edge Detection")
print("l: Laplacian Edge Detection")
print("f: Gaussian Filtering")
print("m: Median Filtering")
print("o: Original (No Filter)")
print("q: Quit")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    if filter_type == 'original':
        display_image = frame
    else:
        display_image = apply_filter(frame, filter_type)

    cv2.imshow('Webcam Filter Demo', display_image)
    key = cv2.waitKey(1) & 0xFF 

    if key == ord('r'):
        filter_type = 'red_tint'
    elif key == ord('g'):
        filter_type = 'green_tint'
    elif key == ord('b'):
        filter_type = 'blue_tint'
    elif key == ord('s'):
        filter_type = 'sobel'
    elif key == ord('c'):
        filter_type = 'canny'
    elif key == ord('l'):
        filter_type = 'laplacian'
    elif key == ord('f'):
        filter_type = 'gaussian'
    elif key == ord('m'):
        filter_type = 'median'
    elif key == ord('o'):
        filter_type = 'original'
    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()