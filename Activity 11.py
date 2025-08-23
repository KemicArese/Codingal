import cv2
import numpy as np
import matplotlib.pyplot as plt

def display_img(title, image):
    plt.figure(figsize=(8, 8))
    if len(image.shape) == 2:
        plt.imshow(image, cmap='gray')
    else:
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def interactive_edge_detection(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Could not read the image.")
        return
    
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    display_img("Original Grayscale Image", gray_image)

    print({
        "Select an option",
        "1. Sobel Edge Detection",
        "2. Canny Edge Detection",
        "3. Laplacian Edge Detection",
        "4. Gaussian Smoothing",
        "5. Median Filtering",
        "6. Exit"
    })

    choice = input("Enter your choice (1-6): ")
    if choice == "1":
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=5)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=5)
        sobel = cv2.magnitude(sobel_x, sobel_y)
        display_img("Sobel Edge Detection", sobel)
    
    elif choice == "2":
        edges = cv2.Canny(gray_image, 100, 200)
        display_img("Canny Edge Detection", edges)
    
    elif choice == "3":
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F)
        display_img("Laplacian Edge Detection", laplacian)
    
    elif choice == "4":
        gaussian = cv2.GaussianBlur(gray_image, (5, 5), 0)
        display_img("Gaussian Smoothing", gaussian)
    
    elif choice == "5":
        median = cv2.medianBlur(gray_image, 5)
        display_img("Median Filtering", median)
    
    elif choice == "6":
        print("Exiting...")
        return
    
    else:
        print("Invalid choice.")
        return
    

if __name__ == "__main__":
    interactive_edge_detection('download (13).jpeg')