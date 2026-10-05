<div align="center">

# 🛡️ DRISHTI (दृष्टि)
### Ministry AI Vision Vigilance & Real-Time Face Attendance Core
**Automated Computer Vision Compliance, Biometric Fraud Defense & Cryptographic Audit Infrastructure**

[![Live Web Application](https://img.shields.io/badge/🌐_Live_Deployment-Render_Cloud-00C7B7?style=for-the-badge)](https://drishti-4sg0.onrender.com)
[![Python Version](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-YuNet_%26_SFace-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![PostgreSQL](https://img.shields.io/badge/Supabase-PostgreSQL_15-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)](https://supabase.com/)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![DPDP Act 2023](https://img.shields.io/badge/Compliance-DPDP_Act_2023-orange?style=for-the-badge)](#-dpdp-act-2023-privacy-compliance)

---

### 🌐 **Live Web Application URL**: [https://drishti-4sg0.onrender.com](https://drishti-4sg0.onrender.com)
*(Interactive Command Portal with Live AI Video Stream, Trainee Enrollment, and Real-Time Vigilance Dashboard)*

</div>

---

## 📌 Problem Statement Details & Metadata

| Field | Details |
| :--- | :--- |
| **Problem Title** | Development of an Automated AI-Based Vision Vigilance and Attendance Tracking System for Government Skilling Centres |
| **Problem Statement ID** | `SIH-26245` / `SIH-PS-22` *(Placeholder: Update with exact ID if needed)* |
| **Ministry / Organization** | **Ministry of Skill Development & Entrepreneurship (MSDE)**, Government of India |
| **Target Programs** | Pradhan Mantri Kaushal Vikas Yojana (**PMKVY**), **DDU-GKY**, National Apprenticeship Promotion Scheme (**NAPS**) |
| **Category** | **Software** |
| **Theme / Domain** | Smart Education & Vocational Skilling / AI Computer Vision & Governance Vigilance |
| **Primary Objective** | Eliminate systemic ghost trainees, biometric punch-and-leave fraud, instructor absenteeism, and unverified machinery idling through real-time edge-to-cloud AI compliance. |

---

## 🛑 The Core Problem: Systemic Fraud in Skilling Schemes

Government-funded vocational training programs disburse public grants per enrolled and trained candidate. However, traditional monitoring mechanisms suffer from critical structural vulnerabilities:

```
┌───────────────────────────┐      ┌───────────────────────────┐      ┌───────────────────────────┐
│   GHOST CANDIDATE FRAUD   │      │  "PUNCH-AND-LEAVE" ATTACK │      │ EQUIPMENT MISREPRESENTATION│
│ Trainees enrolled only on │      │ Trainees punch biometric  │      │ Training machinery listed │
│ paper; physical classrooms│ ───► │ at 9 AM and depart within │ ───► │ on paper (BOM) remains    │
│ remain empty.             │      │ 15 mins. Headcount=0.     │      │ boxed, broken, or idle.   │
└───────────────────────────┘      └───────────────────────────┘      └───────────────────────────┘
```

1. **Ghost Trainees & Identity Forgery**: Trainees exist on registers but never attend practical classes.
2. **Biometric "Punch-and-Leave" Fraud**: Candidates register their morning Aadhaar thumbprint (AEBAS) and immediately depart; afternoon sessions operate at $<25\%$ capacity.
3. **Equipment Idling & BOM Misrepresentation**: Sanctioned Bill of Materials (BOM) machinery (e.g. computer terminals, CNC simulators, sewing rigs) are shown during one-off inspections but never used in practical training.
4. **Audit Vulnerability & Collusion**: Manual, scheduled physical inspections suffer from inspector collusion, advance tips, and post-hoc ledger alterations.

---

## 💡 Our Solution: DRISHTI Architecture & Main USPs

**Drishti** provides an autonomous, multi-tier compliance system that bridges edge CCTV sensors directly to national vigilance command centres with cryptographic immutability.

```
                           ┌─────────────────────────────────────────┐
                           │      DRISHTI MULTI-TIER PIPELINE        │
                           └─────────────────────────────────────────┘
        EDGE INGESTION                   AI RECOGNITION CORE                 CLOUD VIGILANCE CORE
  ┌─────────────────────────┐        ┌─────────────────────────┐        ┌─────────────────────────┐
  │ • CCTV / RTSP / Webcams │        │ • YuNet Face Detection  │        │ • FastAPI Backend Core  │
  │ • Privacy Face Blurring │ ─────► │ • SFace 128-D Embedding │ ─────► │ • Supabase PostgreSQL   │
  │ • Feed Tamper Watchdog  │        │ • Cosine Matching       │        │ • SHA-256 Chained Ledger│
  │ • 72-hr SQLite Buffer   │        │ • 4-hr Dwell Curve Gen  │        │ • SIS Risk Scoring & AI │
  └─────────────────────────┘        └─────────────────────────┘        └─────────────────────────┘
```

### 🌟 Key Unique Selling Propositions (USPs):

- 👁️ **High-Speed ONNX Vision Stack (YuNet + SFace)**:
  - **YuNet**: Detects faces, bounding boxes, brightness, blur scores, and 5 facial landmarks (eyes, nose, mouth corners) in $\le 18\text{ ms}$ on CPU.
  - **SFace**: Extracts 128-dimensional L2-normalized feature vectors; verifies identities via cosine similarity ($\ge 0.55$) without bulky GPU overhead.
- 📈 **Continuous 4-Hour Presence Dwell Curves**:
  - Replaces single-point biometric punches with continuous 5-minute sampling curves, instantly detecting the sudden drop in attendance characteristic of **Punch-and-Leave fraud**.
- ⛓️ **Cryptographic SHA-256 Tamper-Proof Alert Ledger**:
  - Every detected violation, feed tampering, or attendance mismatch is sealed into a hash-chained block ($\text{Hash}_n = \text{SHA256}(\text{Block}_n + \text{Hash}_{n-1})$). Verified via one-click cryptographic mathematical audit (`/api/ledger/verify`).
- 🛡️ **DPDP Act 2023 Legal Privacy Compliance**:
  - Edge nodes irreversibly apply Gaussian face blurring on general public feeds. Biometric reference templates are stored exclusively as 128-D encrypted vector representations (Fernet symmetric cryptography)—never raw facial photos.
- ⚡ **72-Hour Offline Edge Resilience**:
  - Rural training centres with intermittent broadband buffer signed telemetry in a local SQLite store-and-forward queue, automatically syncing upon network recovery.
- 🎯 **Skilling Integrity Score (SIS) & Inspector Dispatch**:
  - Calculates an objective composite rating (0–100) per centre. Red-alert centres ($\text{SIS} < 65$) automatically populate the State Vigilance Inspector's priority physical audit queue.
- ⚔️ **Built-in Adversarial Red-Team Simulator**:
  - Benchmark console with 6 standard fraud attack vectors (Lens Occlusion, Video Loop Replay, Punch-and-Leave, Idle Equipment Prop, Absent Trainer, Silence-as-Alarm) to verify real-time defense.

---

## 📐 System Architecture & Dataflow Diagrams

### 1. High-Level Multi-Tier Architecture

```mermaid
flowchart TD
    subgraph Tier1["Tier 1: Edge Layer (Local Training Centre)"]
        Cam["CCTV / RTSP / Browser Webcam"] --> Ingest["Frame Ingestion & Quality Assessor"]
        Ingest --> Watchdog["Feed Tamper Watchdog (Blackout/Loop)"]
        Ingest --> Blur["Privacy Face Obfuscator (DPDP 2023)"]
        Ingest --> OfflineDB["72-Hour SQLite Offline Buffer"]
    end

    subgraph Tier2["Tier 2: AI Computer Vision & Analytics Pipeline"]
        Blur --> YuNet["YuNet: Face Detection + 5-Landmark Alignment"]
        YuNet --> SFace["SFace: 128-D Feature Embedding Extraction"]
        SFace --> Matcher["Cosine Similarity Matcher (Threshold: 0.55)"]
        Matcher --> Dwell["Continuous Dwell Curve & BOM Equipment Analyzer"]
    end

    subgraph Tier3["Tier 3: Cloud Command & Cryptographic Core"]
        Matcher --> FastAPI["FastAPI Cloud Backend & WebSocket / MJPEG"]
        FastAPI --> Supabase[("Supabase PostgreSQL (Profiles, Embeddings, Attendance)")]
        FastAPI --> Ledger["SHA-256 Hash-Chained Alert Ledger"]
        FastAPI --> SIS["Skilling Integrity Score (SIS) Engine"]
        FastAPI --> AuditQueue["Risk-Weighted Physical Audit Dispatch Queue"]
    end

    subgraph Tier4["Tier 4: Presentation & Vigilance Dashboard"]
        FastAPI --> WebUI["Bilingual Command Dashboard (EN / हिंदी)"]
        WebUI --> Inspector["State Vigilance Inspector Dispatch (Mobile & Desktop)"]
    end

    OfflineDB -.->|Auto-sync on reconnect| FastAPI
```

---

### 2. End-to-End Real-Time Execution Sequence

```mermaid
sequenceDiagram
    autonumber
    actor Trainee as Trainee / Camera Feed
    participant Edge as Edge Ingestion & Watchdog
    participant AI as YuNet & SFace AI Core
    participant Cloud as FastAPI Backend Server
    participant DB as Supabase PostgreSQL
    actor Officer as Command Dashboard UI

    Trainee->>Edge: Video Stream / Frame Capture (Webcam / RTSP)
    Edge->>Edge: Validate Feed Integrity (SSIM & Luminance)
    Edge->>AI: Raw Video Frame
    AI->>AI: Detect Faces & 5 Landmarks (YuNet)
    AI->>AI: Crop, Align & Extract 128-D Vector (SFace)
    AI->>DB: Compare against Enrolled Biometric Vectors
    DB-->>AI: Matched Identity (Name, ID, Confidence)
    AI->>Cloud: Record Attendance Check-in & Stream Annotated MJPEG
    Cloud->>DB: INSERT AttendanceRecord (Session, Student, Timestamp)
    Cloud->>Officer: 2.0s Live Roster Polling Update & Green HUD Overlay
```

---

### 3. Database Entity-Relationship (ER) Schema

```
┌─────────────────────────────────┐
│            students             │
├─────────────────────────────────┤
│ PK  student_id   VARCHAR(64)    │◄────────┐
│     name         VARCHAR(128)   │         │
│     batch        VARCHAR(64)    │         │
│     created_at   DATETIME       │         │
└────────────────┬────────────────┘         │
                 │ 1:N                      │ 1:N
                 ▼                          │
┌─────────────────────────────────┐         │
│        face_embeddings          │         │
├─────────────────────────────────┤         │
│ PK  id           SERIAL         │         │
│ FK  student_id   VARCHAR(64)    │         │
│     embedding    JSON (128-D)   │         │
│     created_at   DATETIME       │         │
└─────────────────────────────────┘         │
                                            │
┌─────────────────────────────────┐         │
│       attendance_sessions       │         │
├─────────────────────────────────┤         │
│ PK  session_id   VARCHAR(64)    │◄──┐     │
│     classroom    VARCHAR(64)    │   │     │
│     start_time   DATETIME       │   │ 1:N │
│     end_time     DATETIME       │   │     │
└────────────────┬────────────────┘   │     │
                 │ 1:N                │     │
                 ▼                    │     │
┌─────────────────────────────────┐   │     │
│       attendance_records        │   │     │
├─────────────────────────────────┤   │     │
│ PK  id           SERIAL         │   │     │
│ FK  session_id   VARCHAR(64)    │───┘     │
│ FK  student_id   VARCHAR(64)    │─────────┘
│     timestamp    DATETIME       │
│     status       VARCHAR(32)    │
└─────────────────────────────────┘
```

---

## 💻 Technology Stack

| Layer | Technology | Purpose & Implementation |
| :--- | :--- | :--- |
| **Frontend & UI** | **HTML5, CSS3, Vanilla JS, Chart.js** | Cyber-Gov Command Center, live MJPEG HUD video canvas, responsive mobile drawer navigation, bilingual i18n (English/Hindi). |
| **AI / Computer Vision** | **OpenCV DNN, YuNet, SFace, YOLOv8** | Lightweight ONNX neural networks for 5-landmark face alignment, 128-D vector extraction, person/equipment detection, and dwell tracking. |
| **Backend & API** | **Python 3.11, FastAPI, Uvicorn (ASGI)** | High-performance asynchronous REST endpoints, non-blocking multi-threaded camera ingestion, real-time polling loops. |
| **Database Tier** | **Supabase (PostgreSQL 15), SQLite** | Cloud PostgreSQL with connection pooler for persistent attendance and embeddings; self-healing local SQLite fallback. |
| **Security & Privacy** | **SHA-256 Ledger, Fernet Encryption** | Cryptographic hash-chained alert ledger for tamper-proof auditing; symmetric Fernet encryption for biometric vectors. |
| **DevOps & Cloud** | **Docker, Render, GitHub Actions, cron-job.org** | Linux containerization (`python:3.11-slim`), automatic cloud CI/CD deployment, 24/7 keep-alive uptime monitoring. |

---

## 📂 Repository Structure & Module Breakdown

```bash
sihps22/
├── ai_modules/                 # AI Vision Ingestion & Streaming Core
│   ├── camera_manager.py       # Multi-source threaded ingestion (Webcam/RTSP/File/Browser)
│   ├── face_detector.py        # YuNet face & 5-landmark detection wrapper
│   ├── face_recognizer.py      # SFace 128-D vector extraction & cosine matcher
│   ├── enrollment.py           # Multi-shot reference embedding aggregation
│   ├── model_downloader.py     # Automatic download of YuNet & SFace ONNX models
│   └── pipeline.py             # Live MJPEG streaming, landmark HUD renderer, & DB check-in
├── cloud/                      # Central Cloud Command & Vigilance Services
│   ├── app.py                  # Main FastAPI REST API & static server
│   ├── crosscheck.py           # Cross-checks physical presence vs reported AEBAS
│   ├── ledger.py               # SHA-256 Hash-Chained Alert Ledger implementation
│   ├── scorer.py               # Skilling Integrity Score (SIS) scoring algorithm
│   └── correlation.py          # Cross-centre collusion & multi-centre trainer detection
├── dashboard/                  # Bilingual Responsive Web Command Interface
│   ├── index.html              # Single-page multi-tab command centre UI
│   ├── app.js                  # Client camera streaming, 2s polling, & dynamic charting
│   ├── styles.css              # Cyber-Gov dark/light responsive design system
│   └── i18n.js                 # English ↔ Hindi localization dictionary
├── detector/                   # Dedicated Modular Face & Attendance Package
│   ├── face_detector.py        # YuNet with IoU tracking & quality checks (blur/brightness)
│   ├── recognizer.py           # SFace OpenCV wrapper
│   ├── recognition.py          # Temporal multi-frame identity confirmation service
│   ├── attendance.py           # SQLite attendance sessions, classrooms & audit store
│   ├── student_store.py        # Enrolled student profiles & metadata store
│   └── protected_store.py      # Fernet encrypted biometric vector storage (DPDP 2023)
├── edge/                       # Edge Vigilance & Ingestion Watchdogs
│   ├── feed_integrity.py       # Watchdog for blackout, freeze, and loop replay attacks
│   ├── dwell.py                # 4-Hour continuous presence curve accumulator
│   ├── equipment.py            # BOM sanctioned equipment spatial interaction assessor
│   └── privacy.py              # DPDP 2023 Gaussian privacy face obfuscator
├── models/                     # ONNX Neural Network Model Weights (auto-downloaded)
├── redteam/                    # Adversarial Attack Simulation Benchmark
│   ├── scenarios.py            # 6 Evasion attack vectors (R1 to R6)
│   └── benchmark.py            # Automated red-team penetration test runner
├── database.py                 # Resilient SQLAlchemy engine (Supabase PostgreSQL + SQLite)
├── main.py                     # Local standalone startup script with background simulations
├── Dockerfile                  # Production container configuration
├── Procfile                    # Cloud web process entrypoint
├── requirements.txt            # Production Python dependencies
├── srs.md                      # IEEE 830-compliant Software Requirements Specification
└── video.md                    # Ready-to-record YouTube demo walkthrough script
```

---

## ⚡ Quick Start & Local Setup

### 1. Prerequisites
- **Python 3.11+** installed
- **Git** installed
- A standard USB webcam or laptop integrated camera

### 2. Clone the Repository
```bash
git clone https://github.com/Mannjain26/Drishti.git
cd Drishti
```

### 3. Create a Virtual Environment & Install Dependencies
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Environment Variables (Optional)
Create a `.env` file in the root directory:
```env
# Cloud Supabase PostgreSQL URL (Leave empty to use automatic local SQLite fallback)
SUPABASE_DB_URL=postgresql://postgres.qnelcmteiuqeyugaemyn:Mannjain%4012345@aws-0-ap-south-1.pooler.supabase.com:6543/postgres

# Port Configuration
PORT=8000
```

### 5. Launch the Server
```bash
python main.py
```
Open **[http://localhost:8000](http://localhost:8000)** in your browser!

---

## 🐳 Docker Container Deployment

You can build and run Drishti inside an isolated Docker container with one command:

```bash
# Build Docker image
docker build -t drishti-ai .

# Run container on port 8000
docker run -p 8000:8000 --env-file .env drishti-ai
```

---

## 📡 REST API Documentation

Once the server is running, explore interactive OpenAPI/Swagger docs at **`http://localhost:8000/docs`**.

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/camera/connect` | Connects a video source (`device: 0`, `rtsp://...`, or `file: path.mp4`). |
| `POST` | `/api/camera/disconnect` | Disconnects the active camera stream. |
| `POST` | `/api/camera/frame` | Uploads canvas frames from browser client webcam for cloud recognition. |
| `GET` | `/api/camera/stream` | Live annotated MJPEG video stream with landmark HUD overlay. |
| `POST` | `/api/students/enroll` | Enrolls a trainee with 1–3 facial photos and generates average 128-D vector. |
| `GET` | `/api/students` | Returns list of all enrolled trainees. |
| `DELETE`| `/api/students/{id}` | Deletes a student profile and their biometric embeddings. |
| `GET` | `/api/attendance/status`| Live 2-second polling endpoint returning currently recognized trainees. |
| `GET` | `/api/attendance/history`| Retrieves persistent attendance timestamps from PostgreSQL. |
| `GET` | `/api/ledger/verify` | Cryptographically audits all SHA-256 blocks from Genesis to tip. |
| `POST` | `/api/redteam/run` | Executes automated adversarial penetration benchmark (R1–R6). |

---

## 👥 Team & Hackathon Information

- **Team Name**: *[Insert Your Team Name / e.g., Team Drishti]*
- **Team Lead**: **Mann Jain** ([@Mannjain26](https://github.com/Mannjain26))
- **Team Members**: *[Member 1, Member 2, Member 3, Member 4, Member 5]*
- **Hackathon**: Smart India Hackathon (SIH) 2026
- **Problem Statement**: `SIH-26245` — Ministry of Skill Development & Entrepreneurship (MSDE)

---

## 📄 License & Compliance

- **Legal Compliance**: Aligned with the **Digital Personal Data Protection (DPDP) Act of India, 2023**.
- **Documentation Standard**: Conforms to **IEEE Standard 830-1998** for Software Requirements Specifications (see [srs.md](file:///c:/Users/mannj/Downloads/sihps22/sihps22/srs.md)).
- **License**: MIT License. Open-source for public governance and academic evaluation.
