import cv2
import time
import pyautogui
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils

scroll_speed = 300
scroll_delay = 1
cam_width, cam_height = 940, 680

def detect_gesture(landmarks, handedness):
    fingers = []
    tips = [mp_hands.HandLandmark.THUMB_TIP, mp_hands.HandLandmark.INDEX_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.PINKY_TIP]

    for tip in tips[1:]:  # index to pinky
        if landmarks[tip].y < landmarks[tip - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    thumb_tip = landmarks[mp_hands.HandLandmark.THUMB_TIP]
    thumb_ip = landmarks[mp_hands.HandLandmark.THUMB_IP]
    if (handedness.classification[0].label == "Right" and thumb_tip.x < thumb_ip.x) or (handedness.classification[0].label == "Left" and thumb_tip.x > thumb_ip.x):
        fingers.append(1)
    else:
        fingers.append(0)

    if sum(fingers) == 5:
        return "scroll_up"
    elif sum(fingers) == 0:
        return "scroll_down"
    else:
        return "none"

cap = cv2.VideoCapture(0)
cap.set(3, cam_width)
cap.set(4, cam_height)
last_scroll = p_time = 0

print("Gesture Scroll Control Active\nOpen palm to scroll up\nClose fist to scroll down\nPress 'q' to quit")

while cap.isOpened():
    success, image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)
    gesture, handedness = "none", "unknown"

    if results.multi_hand_landmarks:
        for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            gesture = detect_gesture(hand_landmarks.landmark, hand_handedness)
            handedness = hand_handedness.classification[0].label

        if (time.time() - last_scroll) > scroll_delay:
            if gesture == "scroll_up":
                pyautogui.scroll(scroll_speed)
            elif gesture == "scroll_down":
                pyautogui.scroll(-scroll_speed)
            last_scroll = time.time()

    fps = 1 / (time.time() - p_time) if (time.time() - p_time) > 0 else 0
    p_time = time.time()
    cv2.putText(image, f'FPS: {int(fps)} | Handedness: {handedness} | Gesture: {gesture}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    cv2.imshow('Gesture Scroll Control', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
