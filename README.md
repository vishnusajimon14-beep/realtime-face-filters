# 😎 Snapchat-Style Face Filters with MediaPipe

A real-time face filter application built with Python, OpenCV, and MediaPipe. Apply fun AR filters like glasses, crowns, and dog effects directly on your webcam feed — just like Snapchat!

---

## ✨ Features

- 🟢 **Face Mesh Detection** — Visualize 468 facial landmarks in real time
- 🕶️ **Glasses Filter** — Auto-scales and rotates glasses to match head tilt
- 👑 **Crown Filter** — Places a crown on top of your head
- 🐶 **Dog Filter** — Adds dog ears, nose, and a tongue that appears when you open your mouth
- 👥 **Multi-face Support** — Detects and filters up to 2 faces simultaneously
- ⌨️ **Keyboard Switching** — Instantly switch between filters using number keys

---

## 📁 Project Structure

```
snapchat-filter/
│
├── main.py              # Entry point — webcam loop & filter switching
├── face_mesh.py         # MediaPipe face landmark detector
├── landmark.py          # Extracts key facial points from landmarks
├── geometry.py          # Calculates eye distance, midpoint, and head angle
├── filters.py           # All filter rendering logic (glasses, crown, dog)
├── face_landmarker.task # MediaPipe face landmarker model file
│
└── assets/
    ├── glasses.png      # Glasses image (RGBA with transparency)
    ├── crown.png        # Crown image (RGBA with transparency)
    └── dog.png          # Dog filter image (RGBA with transparency)
```

---

## 🛠️ Requirements

- Python 3.8+
- OpenCV
- MediaPipe

Install dependencies:

```bash
pip install opencv-python mediapipe
```

---

## 🚀 Getting Started

1. **Clone the repository**

```bash
git clone https://github.com/your-username/snapchat-filter.git
cd snapchat-filter
```

2. **Add your asset images** to the `assets/` folder:
   - `glasses.png` — PNG with transparent background
   - `crown.png` — PNG with transparent background
   - `dog.png` — PNG with transparent background (combined ears + nose + tongue layout)

3. **Update asset paths** in `main.py` to point to your assets folder.

4. **Run the app**

```bash
python main.py
```

---

## ⌨️ Controls

| Key | Action |
|-----|--------|
| `0` | Show face mesh |
| `1` | Glasses filter |
| `2` | Crown filter |
| `3` | Dog filter |
| `q` | Quit |

---

## 🧠 How It Works

```
Webcam Frame
     │
     ▼
FaceMeshDetector (MediaPipe)
     │  Detects 468 facial landmarks
     ▼
LandmarkExtractor
     │  Picks key points: eyes, nose, mouth, forehead, chin
     ▼
FaceGeometry
     │  Calculates: eye distance, midpoint, head angle
     ▼
Filters (OpenCV Alpha Blending)
     │  Scales, rotates, and overlays filter image
     ▼
Display (cv2.imshow)
```

### Key Landmark Indices Used

| Point | Index |
|-------|-------|
| Left Eye | 33 |
| Right Eye | 263 |
| Nose | 4 |
| Mouth Upper | 13 |
| Mouth Lower | 14 |
| Chin | 152 |
| Forehead | 10 |

---

## 🐶 Dog Filter Details

The dog filter PNG is split into three sections:
- **Top 35%** → Dog ears (positioned above forehead)
- **35–55%** → Dog nose (positioned over nose)
- **55–100%** → Dog tongue (appears only when mouth is open)

The tongue visibility is triggered when the distance between the upper and lower lip exceeds 25% of the eye distance.

---

## 📸 Asset Requirements

All filter images must be **PNG with an alpha (transparency) channel** so they blend naturally onto the face. You can download free assets from:
- [Freepik](https://www.freepik.com)
- [PNGWing](https://www.pngwing.com)
- [StickPNG](https://www.stickpng.com)

---

## 🤝 Contributing

Pull requests are welcome! Feel free to add new filters or improve existing ones.

1. Fork the repo
2. Create a new branch: `git checkout -b feature/new-filter`
3. Commit your changes: `git commit -m "Add new filter"`
4. Push and open a pull request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🙏 Acknowledgements

- [MediaPipe](https://developers.google.com/mediapipe) — Face landmark detection
- [OpenCV](https://opencv.org/) — Image processing and rendering
