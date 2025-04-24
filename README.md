# Drowsiness_Detection_Project


---
## 💤 Drowsiness Detection System

A real-time computer vision-based drowsiness detection system that uses facial landmarks to monitor eye movements and alert when signs of drowsiness are detected. This project leverages OpenCV and dlib for face and eye detection and serves as a safety application primarily aimed at preventing accidents caused by driver fatigue.

---

### 📌 Features

- Real-time eye aspect ratio (EAR) calculation
- Sound alert on drowsiness detection
- Webcam feed processing
- Visual feedback with facial landmarks
- Simple and efficient logic for monitoring eye closure duration

---

### 🧠 Technologies Used

- Python
- OpenCV
- dlib (for facial landmark detection)
- imutils
- scipy
- playsound

---

### 📁 File Structure

```
├── Drowsiness_Detection.ipynb   # Jupyter notebook with complete implementation
├── shape_predictor_68_face_landmarks.dat   # Pre-trained dlib model (required)
├── alarm.wav                    # Sound file to alert drowsiness (required)
└── README.md                    # Project documentation
```

---

### ⚙️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/drowsiness-detection.git
   cd drowsiness-detection
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Download the [shape_predictor_68_face_landmarks.dat](http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2) file and place it in the project directory.

---

### 🚀 How to Run

```bash
python drowsiness_detection.py
```

Or run the Jupyter notebook cell-by-cell for interactive understanding.

---

### ⚠️ Important Notes

- Ensure your webcam is functional.
- Place the `alarm.wav` sound file in the working directory.
- Adjust the EAR threshold and frame count if needed for better accuracy.

---

### 🙌 Acknowledgments

- Inspired by research on fatigue detection systems for road safety.
- Uses dlib's 68-point facial landmark predictor.

---

Credit - Md Aftab.
gmail-aftabrahi20089@gmail.com
