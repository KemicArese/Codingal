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

# Initialize pynput keyboard controller
keyboard = Controller()

# MediaPipe Initialization
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Pycaw Initialization (Volume)
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    min_vol, max_vol, _ = volume.GetVolumeRange()
except Exception as e:
    print(f"[Init Error] Pycaw not available: {e}")
    raise SystemExit

# Global state for minimizing to prevent rapid-fire minimization
minimize_debounce = False
playpause_debounce = False

# Function to check if a specific finger is up
def is_finger_up(hand_landmarks, finger_tip, finger_pip, h):
    tip_y = hand_landmarks.landmark[finger_tip].y * h
    pip_y = hand_landmarks.landmark[finger_pip].y * h
    return tip_y < pip_y

# OpenCV Video Capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("[Init Error] Cannot open webcam")
    raise SystemExit

while True:
    success, frame = cap.read()
    if not success:
        print("[Frame Error] Cannot read frame from webcam")
        break
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    cv2.putText(frame, "Right Hand: Volume / Minimize", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(frame, "Left Hand: Brightness / Play-Pause", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    if result.multi_hand_landmarks:
        handed_list = result.multi_handedness or []
        for idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
            hand_label = "Unknown"
            if idx < len(handed_list):
                hand_label = handed_list[idx].classification[0].label

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            thumb_pos = (int(thumb_tip.x * w), int(thumb_tip.y * h))
            index_pos = (int(index_tip.x * w), int(index_tip.y * h))

            cv2.circle(frame, thumb_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.circle(frame, index_pos, 10, (255, 0, 0), cv2.FILLED)
            cv2.line(frame, thumb_pos, index_pos, (255, 0, 0), 3)

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
                cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(frame, (50, vol_bar_y), (85, 400), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'Volume: {vol_percent} %', (40, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

                # --- Minimize Window (Pinky Up) ---
                is_pinky_up = is_finger_up(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, h)

                if is_pinky_up:
                    cv2.putText(frame, 'MINIMIZE GESTURE', (w - 300, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    if not minimize_debounce:
                        try:
                            active_window = gw.getActiveWindow()
                            if active_window is not None:
                                active_window.minimize()
                                minimize_debounce = True
                                cv2.putText(frame, 'WINDOW MINIMIZED!', (w - 350, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
                        except Exception as e:
                            print(f"[Error Minimizing Window] {e}")
                elif minimize_debounce:
                    minimize_debounce = False


            elif hand_label == "Left":
                # --- Brightness Control (Thumb-Index Distance) ---
                brightness = np.interp(distance, [dist_min, dist_max], [0, 100])
                try:
                    sbc.set_brightness(int(brightness))
                except Exception as e:
                    print(f"[Error Adjusting Brightness] {e}")

                bright_bar_y = int(np.interp(distance, [dist_min, dist_max], [400, 150]))
                cv2.rectangle(frame, (550, 150), (585, 400), (255, 255, 0), 3)
                cv2.rectangle(frame, (550, bright_bar_y), (585, 400), (255, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'Brightness: {int(brightness)} %', (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

                # --- Play/Pause (Middle Finger Up) ---
                is_middle_up = is_finger_up(hand_landmarks, mp_hands.HandLandmark.MIDDLE_FINGER_TIP, mp_hands.HandLandmark.MIDDLE_FINGER_PIP, h)
                is_ring_down = not is_finger_up(hand_landmarks, mp_hands.HandLandmark.RING_FINGER_TIP, mp_hands.HandLandmark.RING_FINGER_PIP, h)
                is_pinky_down = not is_finger_up(hand_landmarks, mp_hands.HandLandmark.PINKY_TIP, mp_hands.HandLandmark.PINKY_PIP, h)

                is_play_pause_gesture = is_middle_up and is_ring_down and is_pinky_down

                if is_play_pause_gesture:
                    cv2.putText(frame, 'PLAY/PAUSE GESTURE', (200, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    if not playpause_debounce:
                        try:
                            keyboard.press(Key.media_play_pause)
                            keyboard.release(Key.media_play_pause)
                            playpause_debounce = True
                            cv2.putText(frame, 'PLAY/PAUSE TOGGLED!', (150, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 255), 3)
                        except Exception as e:
                            print(f"[Error Toggling Play/Pause] {e}")
                elif playpause_debounce:
                    playpause_debounce = False

    cv2.imshow("Volume and Brightness Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()