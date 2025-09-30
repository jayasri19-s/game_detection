import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Start webcam
cap = cv2.VideoCapture(0)

# Function to detect fingers up
def finger_up(landmarks, tip, dip):
    return landmarks[tip].y < landmarks[dip].y

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, c = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            # Fingers: Thumb=4, Index=8, Middle=12, Ring=16, Pinky=20
            index_up = finger_up(landmarks, 8, 6)
            middle_up = finger_up(landmarks, 12, 10)
            thumb_up = finger_up(landmarks, 4, 3)

            # Example Game Controls:
            # Jump (Space key) → Index finger up
            if index_up and not middle_up:
                pyautogui.press('space')
                cv2.putText(frame, "Jump", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            # Shoot (S key) → Index + Middle fingers up
            if index_up and middle_up:
                pyautogui.press('s')
                cv2.putText(frame, "Shoot", (20, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

            # Pause (P key) → Thumb + Index
            if thumb_up and index_up:
                pyautogui.press('p')
                cv2.putText(frame, "Pause", (20, 150),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.imshow("Hand Game Controller", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
