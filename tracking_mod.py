import cv2
import mediapipe as mp
import time
import random


class HandDetector:
    def __init__(self, mode=False, max_hands=2, det_confidence=0.5,
                 track_con=0.5):
        self.results = None
        self.mode = mode
        self.maxHands = max_hands
        self.detConfidence = det_confidence
        self.trackCon = track_con

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.mode,
                                        max_num_hands=self.maxHands,
                                        min_detection_confidence=
                                        self.detConfidence,
                                        min_tracking_confidence=self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands(self, img, draw=True):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img, hand_num=0, draw=False):

        lm_list = []
        if self.results.multi_hand_landmarks:
            my_hand = self.results.multi_hand_landmarks[hand_num]
            for id_num, lm in enumerate(my_hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id_num, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 10, (255, 0, 255),
                               cv2.FILLED)
        return lm_list

    def count_fingers(self, lm_list):
        tip_ids = [4, 8, 12, 16, 20]
        pip_ids = [2, 6, 10, 14, 18]

        fingers = []

        thumb_open = lm_list[tip_ids[0]][1] < lm_list[pip_ids[0]][1] - 15
        fingers.append(1 if thumb_open else 0)

        for tip, pip in zip(tip_ids[1:], pip_ids[1:]):
            fingers.append(1 if lm_list[tip][2] < lm_list[pip][2] - 15 else 0)

        return fingers

    def play_rps(self, lm_list):
        fingers = self.count_fingers(lm_list)

        if (fingers[1] == 1 and fingers[2] == 1 and
                sum(fingers) == 2):
            return "SCISSORS"

        elif fingers[0] == 1 and sum(fingers) == 1:
            return "THANK YOU, I TRY"

        elif sum(fingers[1:]) == 0:
            return "ROCK"

        elif sum(fingers) >= 4:
            return "PAPER"

        elif fingers[2] == 1 and sum(fingers) == 1:
            return "THAT'S NOT VERY NICE"

        return "INVALID MOVE"


def main():
    prev_time = 0
    curr_time = 0
    cap = cv2.VideoCapture(0)
    detector = HandDetector()

    prev_gesture = None
    computer_play = random.choice(["ROCK", "PAPER", "SCISSORS"])

    winning_pairs = {"ROCK": "SCISSORS", "SCISSORS": "PAPER", "PAPER": "ROCK"}

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        lm_list = detector.find_position(img)
        if len(lm_list) > 0:
            gesture = detector.play_rps(lm_list)
            cv2.putText(img, f"Player: {gesture}", (10, 90),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)
            if gesture != "INVALID MOVE" and gesture != prev_gesture:
                computer_play = random.choice(["ROCK", "PAPER", "SCISSORS"])
                prev_gesture = gesture

                if gesture == computer_play:
                    result_text = "DRAW!"
                elif winning_pairs.get(gesture) == computer_play:
                    result_text = "YOU WIN!"
                else:
                    result_text = "YOU LOSE!"

            cv2.putText(img, f"Computer: {computer_play}", (10, 120),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)
            if prev_gesture:
                cv2.putText(img, result_text, (10, 140),
                            cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)
        else:
            prev_gesture = None

        curr_time = time.time()
        fps = 1 / (curr_time - prev_time)
        prev_time = curr_time

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 3,
                    (255, 0, 255), 3)

        cv2.imshow("Rock, Paper, Scissors!", img)
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
