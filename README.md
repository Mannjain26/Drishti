# Drishti — Ministry Vigilance & Real-Time AI Face Attendance

**Drishti** is an AI-powered vigilance, compliance, and attendance tracking command platform built for skilling and vocational training centres (PMKVY & DDU-GKY).

---

## 🚀 Key Features

- **Real-Time AI Face Recognition**: YuNet ONNX face detection + SFace 128-D embedding extraction with cosine distance verification.
- **Multi-Camera Support**: Live Webcams (`cv2.VideoCapture(0)`), RTSP IP Camera feeds, and video files.
- **Cloud Database (Supabase)**: Persistent PostgreSQL cloud storage for student profiles, 128-D vector embeddings, and real-time attendance logs.
- **Continuous Presence & Dwell Curves**: Automated detection of "punch-and-leave" biometric fraud and headcount collapse.
- **Tamper-Evident SHA-256 Alert Ledger**: Cryptographically immutable audit log.
- **Live Interactive Command Dashboard**: Bilingual (English & Hindi) dashboard with 2-second auto-polling.

---

## 🛠️ Tech Stack

- **Backend**: FastAPI, Uvicorn, OpenCV (YuNet + SFace ONNX), SQLAlchemy, NumPy
- **Database**: Supabase (PostgreSQL) / SQLite
- **Frontend**: Vanilla HTML5, CSS3, JavaScript, Chart.js

---

## ⚙️ Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the root directory:
```env
SUPABASE_DB_URL=postgresql://postgres:[PASSWORD]@[HOST]:5432/postgres
PORT=8000
```

### 3. Run Application
```bash
python main.py
```
Open **`http://localhost:8000`** in your browser.

---

## 🐳 Docker Deployment
```bash
docker build -t drishti-app .
docker run -p 8000:8000 --env-file .env drishti-app
```
