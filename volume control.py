import cv2
import mediapipe as mp
import numpy as np
from math import hypot
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc

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

    cv2.putText(frame, "Gesture: Right = Volume, Left = Brightness", (20, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

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

            elif hand_label == "Left":
                brightness = np.interp(distance, [dist_min, dist_max], [0, 100])

                try:
                    sbc.set_brightness(int(brightness))

                except Exception as e:
                    print(f"[Error Adjusting Brightness] {e}")

                bright_bar_y = int(np.interp(distance, [dist_min, dist_max], [400, 150]))
                cv2.rectangle(frame, (550, 150), (585, 400), (255, 255, 0), 3)
                cv2.rectangle(frame, (550, bright_bar_y), (585, 400), (255, 255, 0), cv2.FILLED)
                cv2.putText(frame, f'Brightness: {int(brightness)} %', (500, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

                wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
                wrist_pos = (int(wrist.x * w), int(wrist.y * h))
                cv2.putText(frame, f'Wrist Y: {wrist_pos[1]}', (wrist_pos[0] + 20, wrist_pos[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
    cv2.imshow("Volume and Brightness Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release
cv2.destroyAllWindows