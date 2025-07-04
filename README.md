# 🖐️ Rock Paper Scissors - Hand Gesture Recognition Game

A fun real-time Rock, Paper, Scissors game using your webcam! Built with Python, OpenCV, and MediaPipe, the game detects your hand gestures and lets you play against a computer that makes randomized moves. I made this out of boredom because I remembered I know Python.

---

## 🎮 Features

- Detects hand gestures using computer vision (MediaPipe)
- Recognizes Rock ✊, Paper ✋, and Scissors ✌️
- Computer plays a random move **only once** per new valid gesture (there are some secret gestures as well)
- Displays who wins each round in real-time

---

## 🧠 How it Works

1. Uses MediaPipe to track your hand landmarks
2. Determines gesture by analyzing which fingers are up
3. Compares your move with a random computer move
4. Declares winner based on traditional RPS rules

### Note: To ensure your gesture is recognized when playing Scissors, please raise your thumb along with your fingers.

---

## 🛠️ Requirements

- Python 3.7+
- OpenCV
- MediaPipe

### Install dependencies:
```bash
pip install opencv-python mediapipe
```

---

## 🚀 Running the Game

The title of the file which contains the game is "tracking_mod.py". To run it, please use the command below or use the "Run" button in your IDE.

```bash
python tracking_mod.py
```
