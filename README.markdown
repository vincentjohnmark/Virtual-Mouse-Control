# 🖱️ Virtual Mouse Control Using Hand Gestures

A Python-based virtual mouse application that uses hand gestures captured via webcam to simulate mouse movement and clicks. Built using **MediaPipe**, **OpenCV**, **Tkinter**, and **Pynput**.

## ✨ Features

- 🖐️ Control mouse cursor using index finger movement
- 👆 Thumb + finger gestures for:
  - Left click
  - Right click
  - Double click
- 🪟 GUI interface built with Tkinter
- 🎥 Real-time hand tracking via webcam

## 🔧 Technologies Used

- **Python 3.10+**
- **MediaPipe** for hand tracking
- **OpenCV** for video capture and rendering
- **Pynput** for mouse control
- **Tkinter** for GUI
- **Pillow** for image handling (optional)

## 🧪 How to Run

1. **Create a virtual environment (optional)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app**:
   ```bash
   python app.py
   ```

## 📁 File Structure

```
Virtual-Mouse-Control/
├── app.py
├── image.jpg  # Optional background image
├── requirements.txt
└── README.md
```

⚠️ **Note**: Ensure `image.jpg` exists in the same directory as `app.py`, or remove the image loading section in the code if you don’t need a background image.

## 📄 License
MIT License