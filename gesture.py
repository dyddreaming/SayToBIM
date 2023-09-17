import cv2
import mediapipe as mp
import time
import bpy
import requests
import json

url = 'http://127.0.0.1:8080/hand_data'

def calculate_zoom_factor(hand_landmarks, baseline_distance, threshold):
    thumb_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.THUMB_TIP]
    index_finger_tip = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP]

    thumb_x = thumb_tip.x
    index_finger_x = index_finger_tip.x

    distance = abs(thumb_x - index_finger_x)

    if distance > baseline_distance + threshold:
        zoom_factor = 1.05
    elif distance < baseline_distance - threshold:
        zoom_factor = 0.95
    else:
        zoom_factor = 1.0

    return distance, zoom_factor

def detect_zoom_gesture():
    mp_drawing = mp.solutions.drawing_utils
    mp_hands = mp.solutions.hands

    cap = cv2.VideoCapture(0)
    baseline_distance = None
    threshold = 0.02
    last_time = time.time()
    last_distance = None
    zoom_factor = 1.0

    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.5) as hands:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("无法读取摄像头")
                break

            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    if baseline_distance is None:
                        baseline_distance, _ = calculate_zoom_factor(hand_landmarks, 0, threshold)

                    distance, zoom_factor = calculate_zoom_factor(hand_landmarks, baseline_distance, threshold)
                    print("缩放倍数:", zoom_factor)
                    if zoom_factor == 1.05:
                        status = 1
                    elif zoom_factor == 0.95:
                        status = 0
                    else:
                        status = -1
                    print(status)
                    hand_data = {
                        "缩放倍数": zoom_factor,
                        "状态": status
                    }
                    #time.sleep(2)
                    headers = {'Content-type': 'application/json'}
                    response = requests.post(url, data=json.dumps(hand_data), headers=headers)
                    
                    # 打印响应状态码和内容
                    print("Response Status:", response.status_code)
                    print("Response Content:", response.text)

                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS)

                    current_time = time.time()
                    time_diff = current_time - last_time
                    if time_diff <= 1.5 and last_distance:
                        if distance > last_distance:
                            zoom_factor = 1.05
                        elif distance < last_distance:
                            zoom_factor = 0.95
                    last_distance = distance
                    last_time = current_time

            cv2.imshow('Hand Gestures', frame)

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

            # 应用缩放倍数
            frame = cv2.resize(frame, (0, 0), fx=zoom_factor, fy=zoom_factor)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_zoom_gesture()