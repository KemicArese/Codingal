import cv2
import numpy as np
import sys

def run_gesture_control_demo():

    # --- Setup Camera Capture ---
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open video stream.")
        print("Please ensure your webcam is connected and try changing 'cv2.VideoCapture(0)' to (1) or (2).")
        sys.exit(1)

    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    print("\n--- CV Skin Gesture Control Demo Started ---")
    print("GOAL: Track skin tone and classify a basic hand shape.")
    print("1. Place your hand in front of the camera.")
    print("2. The status will attempt to read 'Pointing' (vertical shape) or 'Hand' (squarish shape).")
    print("3. Press 'q' to exit the application.")
    print("----------------------------------\n")

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Error: Failed to grab frame.")
            break

        frame = cv2.flip(frame, 1)
        
        height, width, _ = frame.shape

        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv_frame, lower_skin, upper_skin)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)
        mask = cv2.GaussianBlur(mask, (5, 5), 0) 

        
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        
        gesture_status = "DETECTING..."
        tracking_point = None

        if contours:
            # Find the largest contour
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)

            # Filter out small noise
            min_area_threshold = 3000 # Increased threshold for hands to avoid tracking faces/distant objects
            if area > min_area_threshold:

                # Calculate bounding rectangle and center
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Find the center (centroid) of the object using image moments
                M = cv2.moments(largest_contour)
                if M["m00"] != 0:
                    center_x = int(M["m10"] / M["m00"])
                    center_y = int(M["m01"] / M["m00"])
                    tracking_point = (center_x, center_y)

                    # --- 6. Simple Gesture Classification (Aspect Ratio) ---
                    aspect_ratio = w / h
                    
                    if aspect_ratio < 0.8: # Tall and narrow (e.g., finger pointing up or sideways)
                        gesture_status = "POINTING"
                        status_color = (255, 0, 0) # Blue
                    elif aspect_ratio > 1.2: # Wide and short (less common, maybe sideways pointing)
                        gesture_status = "SIDE SWIPE"
                        status_color = (0, 255, 255) # Yellow
                    else: # Roughly square (e.g., open palm or closed fist)
                        gesture_status = "OPEN HAND"
                        status_color = (0, 255, 0) # Green
                        
                    # --- 7. Real-time Interaction: Visualization ---
                    
                    # Draw the bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), status_color, 2)

                    # Draw a large circle at the tracking point
                    cv2.circle(frame, tracking_point, 15, status_color, -1)
                    
                    # Display the classified gesture status
                    cv2.putText(frame, gesture_status, (center_x + 20, center_y + 5),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2)
                    
        # Always display the current status in the corner
        cv2.putText(frame, f"Gesture: {gesture_status}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

        # --- Display Windows ---
        cv2.imshow('Gesture Control (Webcam Feed)', frame)
        cv2.imshow('Detection Mask (Experimentation)', mask) 

        # Exit the loop if the 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # --- Cleanup ---
    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    run_gesture_control_demo()
