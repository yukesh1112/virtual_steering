import cv2
import mediapipe as mp
import time
import threading
from keyinput import press_key, release_key

# Mediapipe setup
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Font for text display
font = cv2.FONT_HERSHEY_SIMPLEX

# Capture video from webcam
cap = cv2.VideoCapture(0)

# Thread-safe variables
current_frame = None
frame_available = False

def capture_frames():
    global current_frame, frame_available
    while cap.isOpened():
        success, frame = cap.read()
        if success:
            current_frame = cv2.resize(frame, (640, 480))  # Reduce resolution for performance
            frame_available = True
        time.sleep(0.01)  # Limit frame rate to reduce CPU usage

# Start frame capture in a separate thread
frame_thread = threading.Thread(target=capture_frames)
frame_thread.start()

# Initialize Mediapipe Hands model
with mp_hands.Hands(
        model_complexity=0,  # Set lower complexity for faster performance
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as hands:
    
    while cap.isOpened():
        if frame_available:
            image = current_frame.copy()
            frame_available = False  # Mark frame as processed
            
            # Prepare the image for Mediapipe processing
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Detect hand landmarks
            results = hands.process(image)
            
            imageHeight, imageWidth, _ = image.shape
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            co = []
            
            # If hands detected
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Collect wrist coordinates
                    for point in mp_hands.HandLandmark:
                        if str(point) == "HandLandmark.WRIST":
                            normalizedLandmark = hand_landmarks.landmark[point]
                            pixelCoordinatesLandmark = mp_drawing._normalized_to_pixel_coordinates(
                                normalizedLandmark.x, normalizedLandmark.y, imageWidth, imageHeight)
                            if pixelCoordinatesLandmark:
                                co.append(list(pixelCoordinatesLandmark))
                    
            # Logic for controlling key inputs
            if len(co) == 2:
                # Compute hand movement for control logic
                xm, ym = (co[0][0] + co[1][0]) / 2, (co[0][1] + co[1][1]) / 2
                radius = 150

                try:
                    m = (co[1][1] - co[0][1]) / (co[1][0] - co[0][0]) if (co[1][0] - co[0][0]) != 0 else 0
                except ZeroDivisionError:
                    continue
                
                # Logic to handle keyboard presses and movement direction
                if co[0][0] > co[1][0] and co[0][1] > co[1][1] and co[0][1] - co[1][1] > 65:
                    # Turn left
                    release_key('s')
                    release_key('d')
                    press_key('a')
                    cv2.putText(image, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                elif co[1][0] > co[0][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                    # Turn left
                    release_key('s')
                    release_key('d')
                    press_key('a')
                    cv2.putText(image, "Turn left", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                elif co[0][0] > co[1][0] and co[1][1] > co[0][1] and co[1][1] - co[0][1] > 65:
                    # Turn right
                    release_key('s')
                    release_key('a')
                    press_key('d')
                    cv2.putText(image, "Turn right", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
                else:
                    # Keep straight
                    release_key('s')
                    release_key('a')
                    release_key('d')
                    press_key('w')
                    cv2.putText(image, "keep straight", (50, 50), font, 0.8, (0, 255, 0), 2, cv2.LINE_AA)
            
            elif len(co) == 1:
                # Keeping back
                release_key('a')
                release_key('d')
                release_key('w')
                press_key('s')
                cv2.putText(image, "keeping back", (50, 50), font, 1.0, (0, 255, 0), 2, cv2.LINE_AA)
            
            # Display the image
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
        
        # Break loop on 'q' key
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Cleanup resources
cap.release()
cv2.destroyAllWindows()
