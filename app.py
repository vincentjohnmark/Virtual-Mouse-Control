import cv2
import mediapipe as mp
import pyautogui
pyautogui.FAILSAFE = False
import numpy as np
import time
import threading
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pynput.mouse import Button, Controller
import math

mouse = Controller()
screen_width, screen_height = pyautogui.size()

mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.95,
    min_tracking_confidence=0.95,
    max_num_hands=1
)

def is_thumb_open(landmarks):
    return landmarks[4][0] > landmarks[3][0]

def are_ring_pinky_closed(landmarks):
    return landmarks[16][1] > landmarks[14][1] and landmarks[20][1] > landmarks[18][1]

def is_index_finger_bent(landmarks):
    return landmarks[8][1] > landmarks[6][1]

def is_middle_finger_bent(landmarks):
    return landmarks[12][1] > landmarks[10][1]

def move_mouse(x, y):
    if x is not None and y is not None:
        x = np.clip(x * screen_width * 2, 0, screen_width)
        y = np.clip(y * screen_height * 2, 0, screen_height)
        pyautogui.moveTo(int(x), int(y), duration=0.00001)

def execute_action(action, frame):
    actions = {
        "left_click": lambda: mouse.click(Button.left),
        "right_click": lambda: mouse.click(Button.right),
        "double_click": lambda: pyautogui.doubleClick()
    }
    if action in actions:
        actions[action]()
        cv2.putText(frame, action.replace('_', ' ').title(), (50, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)

def detect_gesture(frame, landmarks):
    if len(landmarks) < 21:
        return
   
    index_tip_x, index_tip_y = landmarks[8][0], landmarks[8][1]
    if not is_thumb_open(landmarks):
        move_mouse(index_tip_x, index_tip_y)
    elif is_thumb_open(landmarks) and are_ring_pinky_closed(landmarks):
        if is_index_finger_bent(landmarks) and not is_middle_finger_bent(landmarks):
            execute_action("left_click", frame)
        elif is_middle_finger_bent(landmarks) and not is_index_finger_bent(landmarks):
            execute_action("right_click", frame)
        elif is_index_finger_bent(landmarks) and is_middle_finger_bent(landmarks):
            execute_action("double_click", frame)

def handle_mouse_control():
    draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 60)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen_height)
    prev_time = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            processed = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
           
            landmarks = [(lm.x, lm.y) for lm in processed.multi_hand_landmarks[0].landmark] if processed.multi_hand_landmarks else []
            if landmarks:
                draw.draw_landmarks(frame, processed.multi_hand_landmarks[0], mpHands.HAND_CONNECTIONS)
           
            detect_gesture(frame, landmarks)
           
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time)
            prev_time = curr_time
            cv2.putText(frame, f'FPS: {int(fps)}', (20, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
           
            cv2.imshow('Hand Gesture Control - Mouse Mode', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def start_application():
    root = tk.Tk()
    root.title("Gesture Control Application")
    root.geometry("800x600")
    root.configure(bg="#121212")
   
    ttk.Button(root, text="Mouse Control", command=lambda: threading.Thread(target=handle_mouse_control).start()).pack(pady=10)
    root.mainloop()

if __name__ == '__main__':
    start_application()