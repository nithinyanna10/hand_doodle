# 🎨 HoloDoodle Pro

**Real-time AI Hand Gesture Doodle Camera with Advanced Visual Effects**

A full-stack application featuring 6 unique brush effects, shader effects, particle physics, gesture controls, and a beautiful React UI.

## ✨ Features

### 🖌️ Brush Effects
- **Neon Glow** - HDR-like bloom with triple-layer glow
- **Lightning** - Electric bolts with branches and sparks
- **Fire** - Hot core with ember smoke particles
- **Galaxy** - Cosmic dust with stars and nebula trails
- **Energy Whirl** - Distortion and ripple field effects

### 🎨 Shader Effects
- Chromatic aberration (RGB split)
- Glitch distortion
- Ripple pulse on brush change
- VHS noise

### 🧨 Particle Physics
- Gravity simulation
- Fade effects
- Velocity-based movement
- Explosion particles on gestures

### 🖐️ Gesture Controls
- ✌️ **Peace** - Next brush
- 👍 **Thumbs Up** - Toggle glow mode
- 👌 **Pinch** - Start/stop drawing
- ✊ **Fist** - Clear canvas
- 🤘 **Rock** - Glitch mode

### 🎛️ React UI Dashboard
- Live webcam feed
- Brush picker carousel
- Settings sliders
- FPS meter
- Real-time controls

## 📁 Project Structure

```
holodoodle-pro/
├── frontend/          # React + Vite
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── styles/
│   └── package.json
├── backend/           # FastAPI + WebSocket
│   ├── app.py
│   ├── engine/
│   │   ├── brushes/
│   │   ├── particles/
│   │   ├── shaders/
│   │   ├── utils/
│   │   └── gesture.py
│   └── requirements.txt
└── README.md
```

## 🚀 Installation

### Backend Setup

```bash
cd holodoodle-pro/backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend Setup

```bash
cd holodoodle-pro/frontend
npm install
```

## 🎮 Usage

### Start Backend

```bash
cd holodoodle-pro/backend
source venv/bin/activate
python app.py
```

Backend runs on `http://localhost:8000`

### Start Frontend

```bash
cd holodoodle-pro/frontend
npm run dev
```

Frontend runs on `http://localhost:3000`

## 🎯 Controls

### Gesture Controls (No Keyboard!)
- ✌️ Peace sign → Switch brush
- 👍 Thumbs up → Toggle glow
- 👌 Pinch → Start/stop drawing
- ✊ Fist → Clear canvas
- 🤘 Rock sign → Glitch mode

### UI Controls
- Brush picker → Click to change brush
- Toggles → Enable/disable effects
- Sliders → Adjust particle intensity

## 🛠️ Tech Stack

- **Backend**: FastAPI, WebSocket, OpenCV, MediaPipe
- **Frontend**: React, Vite, Framer Motion, Lucide Icons
- **Effects**: Custom shaders, particle physics, gesture recognition

## 📝 License

MIT

