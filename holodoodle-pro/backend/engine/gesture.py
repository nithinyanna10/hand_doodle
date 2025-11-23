import cv2
import mediapipe as mp
import numpy as np

class GestureRecognizer:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
    
    def get_landmarks(self, frame):
        """Get hand landmarks from frame"""
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)
        if results.multi_hand_landmarks:
            return results.multi_hand_landmarks[0]
        return None
    
    def detect_gesture(self, landmarks):
        """Detect gesture from landmarks"""
        if not landmarks:
            return None
        
        # Get key points
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
        
        thumb_ip = landmarks.landmark[3]
        index_pip = landmarks.landmark[6]
        middle_pip = landmarks.landmark[10]
        ring_pip = landmarks.landmark[14]
        pinky_pip = landmarks.landmark[18]
        
        # Peace sign (✌️) - index and middle up, others down
        if (index_tip.y < index_pip.y and 
            middle_tip.y < middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y):
            return "peace"
        
        # Thumbs up (👍) - thumb up, others down
        if (thumb_tip.y < thumb_ip.y and
            index_tip.y > index_pip.y and
            middle_tip.y > middle_pip.y):
            return "thumbs_up"
        
        # Pinch (👌) - thumb and index close
        thumb_index_dist = np.sqrt(
            (thumb_tip.x - index_tip.x)**2 + 
            (thumb_tip.y - index_tip.y)**2
        )
        if thumb_index_dist < 0.05:
            return "pinch"
        
        # Fist (✊) - all fingers down
        if (thumb_tip.y > thumb_ip.y and
            index_tip.y > index_pip.y and
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y and
            pinky_tip.y > pinky_pip.y):
            return "fist"
        
        # Rock (🤘) - index and pinky up, middle and ring down
        if (index_tip.y < index_pip.y and
            pinky_tip.y < pinky_pip.y and
            middle_tip.y > middle_pip.y and
            ring_tip.y > ring_pip.y):
            return "rock"
        
        return None
    
    def get_finger_tip(self, landmarks, finger_index=8):
        """Get finger tip position (default: index finger)"""
        if not landmarks:
            return None, None
        tip = landmarks.landmark[finger_index]
        return tip.x, tip.y

