# 🎨 Hand Doodle Camera

Real-time hand gesture doodle camera with multiple brush effects using MediaPipe Hands and OpenCV.

## ✨ Features

- **Neon Brush** - Glowing purple/pink lines with TikTok aesthetic
- **Sparkle Brush** - Magical spark dots around your finger
- **Fire Brush** - Orange-red flame strokes like fire bending

## 📦 Installation

```bash
pip install -r requirements.txt
```

## 🚀 Usage

```bash
python doodle.py
```

## 🎮 Controls

| Key | Action |
|-----|--------|
| `m` | Switch brush (neon → sparkle → fire) |
| `c` | Clear doodles |
| `q` | Quit |

## 🖐️ How It Works

- Uses MediaPipe Hands to detect hand landmarks
- Tracks index finger tip (landmark 8) for drawing
- Three different brush modes with unique visual effects
- Real-time blending of webcam feed with drawing canvas

