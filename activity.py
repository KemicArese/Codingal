import cv2
import numpy as np

def apply_color_filter(img, filter):
    if filter == "red_tint":
        img[:, :, 2] = np.clip(img[:, :, 2] * 1.5, 0, 255)
    elif filter == "green_tint":
        img[:, :, 1] = np.clip(img[:, :, 1] * 1.5, 0, 255)
    elif filter == "blue_tint":
        img[:, :, 0] = np.clip(img[:, :, 0] * 1.5, 0, 255)
    else:
        print("Invalid filter")
    return img

img_path = 'assets/example.png'
img = cv2.imread(img_path)

if img is None:
    print("Error: Could not read the image.")
    exit()
else:
    filter_type = 'original'

    print("Select a filter to apply:")
    print("r - Red Tint")
    print("g - Green Tint")
    print("b - Blue Tint")
    print("i - Increase Red Intensity")
    print("d - Decrease Red Intensity")
    print("o - Original")
    print("q - Quit")
    while True:
        filtered_img = apply_color_filter(img, filter_type)
        cv2.imshow('Filtered Image', filtered_img)
        key = cv2.waitKey(0) & 0xFF

        if key == ord('r'):
            filter_type = 'red_tint'
        elif key == ord('g'):
            filter_type = 'green_tint'
        elif key == ord('b'):
            filter_type = 'blue_tint'
        elif key == ord('i'):
            filter_type = 'increase_red_intensity'
        elif key == ord('d'):
            filter_type = 'decrease_red_intensity'
        elif key == ord('o'):
            filter_type = 'original'
        elif key == ord('q'):
            break
        else:
            print("Invalid key pressed.")

    cv2.destroyAllWindows()