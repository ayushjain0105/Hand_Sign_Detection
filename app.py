import cv2
import mediapipe as mp
import pickle
import numpy as np
import os
APP_DIR = os.path.dirname(os.path.abspath(__file__))
model_PATH = os.path.join(APP_DIR, "model.p")
cap1 = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.3)

model_dict = pickle.load(open(model_PATH, "rb"))
model = model_dict["model"]
label_dict={0:'A',1:'B',2:'C',3:'D',4:'E',5:'F',6:'G',7:'H',8:'I',9:'J',10:'K',11:'L',12:'M',13:'N',14:'O',15:'P',16:'Q',17:'R',18:'S',19:'T',20:'U',21:'V',22:'W',23:'X',24:'Y',25:'Z'}
while True:
    ret, frame = cap1.read()
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame, 
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(), 
                mp_drawing_styles.get_default_hand_connections_style()
            )

            data_aux = [coord for landmark in hand_landmarks.landmark for coord in (landmark.x, landmark.y)]
            
            prediction = model.predict_proba([np.asarray(data_aux)])  # Change this line
            predicted_index = np.argmax(prediction[0])
            predicted_label = label_dict[predicted_index]
            accuracy = prediction[0][predicted_index]
            # Draw bounding box
            h, w, _ = frame.shape
            min_x = min(landmark.x for landmark in hand_landmarks.landmark) * w
            max_x = max(landmark.x for landmark in hand_landmarks.landmark) * w
            min_y = min(landmark.y for landmark in hand_landmarks.landmark) * h
            max_y = max(landmark.y for landmark in hand_landmarks.landmark) * h
            cv2.rectangle(frame, (int(min_x), int(min_y)), (int(max_x), int(max_y)), (0, 255, 0), 2)

            # Display label and accuracy
            accuracy_text = f'{accuracy * 100:.2f}%'
            label_text = f'Label: {predicted_label}, Accuracy: {accuracy_text}'
            cv2.putText(frame, label_text, (10, h - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(label_text)
    cv2.imshow("frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Add a condition to break the loop
        break

cap1.release()
cv2.destroyAllWindows()