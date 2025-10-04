import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc
from pynput.keyboard import Key, Controller
import pygetwindow as gw

# --- Global Filter Variables and Functions ---
FILTER_LIST = ['original', 'red_tint', 'green_tint', 'blue_tint', 'sobel', 'canny', 'laplacian', 'gaussian', 'median']
current_filter_index = 0
current_filter_type = FILTER_LIST[current_filter_index]
filter_debounce_y = 0

def apply_filter(image, filter_type):
    filtered_image = image.copy()
    if filter_type == 'red_tint':
        filtered_image[:, :, 1] = 0
        filtered_image[:, :, 0] = 0
    elif filter_type == 'green_tint':
        # Increase green channel intensity, but keep other channels
        green_boost = 100  # You can adjust this value or make it dynamic
        filtered_image[:, :, 1] = np.clip(filtered_image[:, :, 1] + green_boost, 0, 255)
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

# --- Initialization from First Code ---
keyboard = Controller()
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min_vol, max_vol, _ = volume.GetVolumeRange()
except Exception as e:
    print(f"[Init Error] Pycaw not available: {e}")
    raise SystemExit

minimize_debounce = False
playpause_debounce = False

def is_finger_up(hand_landmarks, finger_tip, finger_pip, h):
    tip_y = hand_landmarks.landmark[finger_tip].y * h
    pip_y = hand_landmarks.landmark[finger_pip].y * h
    return tip_y < pip_y

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[Init Error] Cannot open webcam")
    raise SystemExit

while True:
    success, frame = cap.read()
    if not success:
        print("[Frame Error] Cannot read frame from webcam")
        break
    
    # Flip for natural viewing
    frame_flipped = cv2.flip(frame, 1)

    # Use original frame for hand detection
    rgb_frame = cv2.cvtColor(frame_flipped, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    # Apply filter for display only
    filtered_frame = apply_filter(frame_flipped, current_filter_type)
    
    # Display current control and filter status
    cv2.putText(filtered_frame, "Right: Volume / Minimize", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(filtered_frame, "Left: Brightness / Play-Pause / Filter Cycle", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(filtered_frame, f"Filter: {current_filter_type.replace('_', ' ').title()}", (filtered_frame.shape[1] - 300, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    if result.multi_hand_landmarks:
        handed_list = result.multi_handedness or []
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            hand_label = "Unknown"
            if idx < len(handed_list):
                hand_label = handed_list[idx].classification[0].label

            mp_draw.draw_landmarks(filtered_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = filtered_frame.shape
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_pos = (int(index_tip.x * w), int(index_tip.y * h))
            wrist_pos = (int(wrist.x * w), int(wrist.y * h))

            cv2.circle(filtered_frame, thumb_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(filtered_frame, index_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(filtered_frame, thumb_pos, index_pos, (255, 0, 0), 3)

            distance = hypot(index_pos[0] - thumb_pos[0], index_pos[1] - thumb_pos[1])
            dist_min, dist_max = 30, 200

            if hand_label == "Right":
                # --- Volume Control (Thumb-Index Distance) ---
                vol_db = np.interp(distance, [dist_min, dist_max], [min_vol, max_vol])
                try:
                    volume.SetMasterVolumeLevel(vol_db, None)
                except Exception as e:
                    print(f"[Error Adjusting Volume] {e}")

                vol_percent = int(np.interp(distance, [dist_min, dist_max], [0, 100]))
                vol_bar_y = int(np.interp(distance, [dist_min, dist_max], [400, 150]))
                cv2.rectangle(filtered_frame, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(filtered_frame, (50, vol_bar_y), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(filtered_frame, f'Volume: {vol_percent} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                # --- Minimize Window (Pinky Up) ---
                is_pinky_up = is_finger_up(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, h)

                if is_pinky_up:
                    cv2.putText(filtered_frame, 'MINIMIZE GESTURE', (w - 300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if not minimize_debounce:
                        try:
                            active_window = gw.getActiveWindow()
                            if active_window is not None:
                                active_window.minimize()
                                minimize_debounce = True
                                cv2.putText(filtered_frame, 'WINDOW MINIMIZED!', (w - 350, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                        except Exception as e:
                            print(f"[Error Minimizing Window] {e}")
                elif minimize_debounce:
                    minimize_debounce = False


            elif hand_label == "Left":
                # --- Brightness Control (Thumb-Index Distance) ---
                brightness = np.interp(distance, [dist_min, dist_max], [0, 100])
                brightness = np.interp(distance, [dist_min, dist_max], [0, 100])
                try:
                    sbc.set_brightness(int(brightness))
                except Exception as e:
                    print(f"[Error Adjusting Brightness] {e}")

                bright_bar_y = int(np.interp(distance, [dist_min, dist_max], [400, 150]))
                cv2.rectangle(filtered_frame, (550, 150), (585, 400), (255, 255, 0), 3)
                cv2.rectangle(filtered_frame, (550, bright_bar_y), (585, 400), (255, 255, 0), cv2.FILLED)
                cv2.putText(filtered_frame, f'Brightness: {int(brightness)} %', (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

                # --- Filter Cycling (Index Finger Y-Axis) ---
                
                # Use Y-position of Index Finger Tip to cycle filters
                index_tip_y = index_pos[1]
                
                # Check for a quick upward movement (index_tip_y significantly smaller than debounce y)
                if filter_debounce_y != 0 and index_tip_y < filter_debounce_y - 30: # Upward Movement
                    current_filter_index = (current_filter_index + 1) % len(FILTER_LIST)
                    current_filter_type = FILTER_LIST[current_filter_index]
                    cv2.putText(filtered_frame, 'FILTER CHANGE UP', (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    filter_debounce_y = 0 # Reset debounce to prevent immediate re-trigger
                    
                # Check for a quick downward movement (index_tip_y significantly larger than debounce y)
                elif filter_debounce_y != 0 and index_tip_y > filter_debounce_y + 30: # Downward Movement
                    current_filter_index = (current_filter_index - 1) % len(FILTER_LIST)
                    current_filter_type = FILTER_LIST[current_filter_index]
                    cv2.putText(filtered_frame, 'FILTER CHANGE DOWN', (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    filter_debounce_y = 0 # Reset debounce
                
                # Update debounce only when the finger is relatively steady to get a reference point
                if filter_debounce_y == 0 or abs(index_tip_y - filter_debounce_y) < 10:
                    filter_debounce_y = index_tip_y


                # --- Play/Pause (Middle Finger Up) ---
                is_middle_up = is_finger_up(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, h)
                is_ring_down = not is_finger_up(hand_landmarks, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP, h)
                is_pinky_down = not is_finger_up(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, h)

                is_play_pause_gesture = is_middle_up and is_ring_down and is_pinky_down

                if is_play_pause_gesture:
                    cv2.putText(filtered_frame, 'PLAY/PAUSE GESTURE', (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    if not playpause_debounce:
                        try:
                            keyboard.press(Key.media_play_pause)
                            keyboard.release(Key.media_play_pause)
                            playpause_debounce = True
                            cv2.putText(filtered_frame, 'PLAY/PAUSE TOGGLED!', (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 3)
                        except Exception as e:
                            print(f"[Error Toggling Play/Pause] {e}")
                elif playpause_debounce:
                    playpause_debounce = False


    cv2.imshow("Volume, Brightness, and Filter Control", filtered_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()